#!/usr/bin/env python3
"""Independent COCO mask AP calculator for compressed RLE prediction JSON files.

Zero dependency beyond NumPy. Implements 101-point interpolated AP at IoU
0.50:0.05:0.95, greedy per-image score-ordered matching, maxDets 100,
using exact intersections of column-major COCO compressed RLE mask intervals.
Not the official pycocotools evaluator. The file paths and reported scores are input from the caller.
"""
from __future__ import annotations
import json, os, hashlib, sys, time, math
from pathlib import Path
from collections import defaultdict
import numpy as np

IOT=np.linspace(.5,.95,10)
REC=np.linspace(0,1,101)


def filehash(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for buf in iter(lambda:f.read(1024*1024),b''):h.update(buf)
    return h.hexdigest()


def decode_compressed_rle(compressed, height, width):
    """Decode COCO maskApi signed/delta variable-length RLE into 1-run intervals."""
    if isinstance(compressed,list):
        counts=compressed
    else:
        c=compressed.decode('ascii') if isinstance(compressed,bytes) else compressed
        counts=[]; pos=0
        while pos<len(c):
            shift=0;value=0
            while True:
                z=ord(c[pos])-48;pos+=1
                value|=(z&31)<<shift
                shift+=5
                if not (z&32):
                    if z&16: value|=-1<<shift
                    break
            if len(counts)>2: value+=counts[-2]
            counts.append(value)
    if any(v<0 for v in counts) or sum(counts)!=height*width:
        raise ValueError('Invalid COCO RLE: negative run or wrong mask area')
    ends=np.cumsum(np.array(counts, dtype=np.int64))
    starts=np.r_[0, ends[:-1]]
    # Starts and ends are 0-indexed linear intervals (column-major)
    foreground_starts=starts[1::2]
    foreground_ends=ends[1::2]
    area=int(sum(counts[1::2]))
    return foreground_starts, foreground_ends, area


def get_iou(interval_a,interval_b,area_a,area_b):
    aa,bb=interval_a;cc,dd=interval_b
    i=j=0;inter=0
    la=len(aa);lb=len(cc)
    while i<la and j<lb:
        lo=aa[i] if aa[i]>cc[j] else cc[j]
        hi=bb[i] if bb[i]<dd[j] else dd[j]
        if hi>lo: inter+=int(hi-lo)
        if bb[i]<dd[j]:i+=1
        else:j+=1
    union=area_a+area_b-inter
    return inter/union if union else 0.0


def rle_bbox(starts, ends,h):
    """Simple exact axis-aligned tight bbox in COCO's column-major pixels."""
    if not len(starts):return (0,-1,0,-1)
    x1=int(np.min(starts//h));x2=int(np.max((ends-1)//h))
    ylo=10**10;yhi=-1
    for st,en in zip(starts,ends):
        a=int(st%h);b=int((en-1)%h)
        if st//h!=(en-1)//h:
            return (x1,x2,0,h-1)
        ylo=min(ylo,a);yhi=max(yhi,b)
    return (x1,x2,ylo,yhi)


def prepare_mask(ann):
    sz=ann['segmentation']['size'];h,w=int(sz[0]),int(sz[1])
    s,e,area=decode_compressed_rle(ann['segmentation']['counts'],h,w)
    bb=rle_bbox(s,e,h)
    return {'id':ann.get('id'), 'image_id':ann['image_id'],'score':float(ann.get('score',1.0)), 'int':(s,e),'area':area,'bbox':bb,'size':(h,w),'iscrowd':ann.get('iscrowd',0)}


def can_overlap(a,b):
    x1,x2,y1,y2=a['bbox'];z1,z2,w1,w2=b['bbox']
    return not (x2<z1 or z2<x1 or y2<w1 or w2<y1)


def match_image(gt, pred):
    """Return (descending scores, 10xD matching flags) for all areas and maxDets=100."""
    p=sorted(pred,key=lambda x:-x['score'])[:100]
    g=gt
    scores=np.array([d['score'] for d in p],dtype=np.float64)
    D=len(p);G=len(g)
    ious=np.zeros((D,G),dtype=np.float64)
    if D and G:
        for d,row in enumerate(p):
            for i,gr in enumerate(g):
                if row['size']!=gr['size']: raise ValueError('mask size inconsistency')
                if can_overlap(row,gr):
                    ious[d,i]=get_iou(row['int'],gr['int'],row['area'],gr['area'])
    dtmatches=np.zeros((10,D),dtype=bool)
    for t,thr in enumerate(IOT):
        matched=np.zeros(G,dtype=bool)
        for d in range(D):
            best=-1;bestiou=min(float(thr),1-1e-10)
            for i in range(G):
                if matched[i]:continue
                if ious[d,i]<bestiou:continue
                best=i;bestiou=ious[d,i]
            if best>=0:matched[best]=True;dtmatches[t,d]=True
    return scores,dtmatches


def ap_score(img_matches, image_ids):
    subset=[img_matches[i] for i in image_ids]
    scores=np.concatenate([item[0] for item in subset])
    marks=np.concatenate([item[1] for item in subset],axis=1)
    gts=sum(item[2] for item in subset)
    if gts<=0:raise ValueError('No GT in requested subset')
    si=np.argsort(-scores,kind='mergesort');marks=marks[:,si]
    ap=[]
    for t in range(10):
        tp=np.cumsum(marks[t],dtype=np.float64)
        fp=np.cumsum(~marks[t],dtype=np.float64)
        recall=tp/gts
        precision=tp/(tp+fp+np.spacing(1))
        precision=np.maximum.accumulate(precision[::-1])[::-1]
        idx=np.searchsorted(recall,REC,side='left')
        interp=np.zeros(len(REC),dtype=np.float64)
        valid=idx<len(precision)
        interp[valid]=precision[idx[valid]]
        ap.append(float(np.mean(interp)))
    return {'AP50_95':float(np.mean(ap)),'AP50':ap[0], 'AP75':ap[5], 'per_IoU':ap,'num_GT':gts,'num_detections_after_max100':len(si)}


def verify_inputs(gt_raw, preds, image_ids):
    image_set=set(image_ids)
    if len(image_set)!=len(image_ids):raise ValueError('Duplicate GT image IDs')
    if len({x['id'] for x in gt_raw['annotations']})!=len(gt_raw['annotations']):
        raise ValueError('Duplicate GT annotation IDs')
    if any(x['category_id']!=1 or x.get('iscrowd',0) for x in gt_raw['annotations']):
        raise ValueError('This verifier currently supports one non-crowd COCO category')
    if any(x['image_id'] not in image_set or x['category_id']!=1 or not math.isfinite(float(x['score'])) for x in preds):
        raise ValueError('Invalid prediction image/category/score')


def audit(gt_path, manifest_path, reference_path, out):
    rawgt=json.loads(gt_path.read_text(encoding='utf-8'))
    image_ids=[im['id'] for im in rawgt['images']]
    gt_by_img=defaultdict(list)
    for ann in rawgt['annotations']:
        prepared=prepare_mask(ann)
        if 'area' in ann and abs(ann['area']-prepared['area'])>1e-4:
            raise ValueError('GT encoded segmentation area does not match area field')
        gt_by_img[ann['image_id']].append(prepared)
    dates=defaultdict(list)
    for im in rawgt['images']:
        # Specific to FaroPigSeg: filenames begin YYYY-MM-DD.
        date=im['file_name'][:10]
        if len(date)!=10 or date[4]!='-' or date[7]!='-':raise ValueError('No YYYY-MM-DD date prefix')
        dates[date].append(im['id'])
    items=json.loads(manifest_path.read_text(encoding='utf-8'))['runs']
    if len(items)!=len({(x['model'],int(x['seed'])) for x in items}):raise ValueError('Duplicate model/seed')
    reference=json.loads(reference_path.read_text(encoding='utf-8')) if reference_path else None
    reference_global={(x['Model'],int(x['Seed'])):x for x in reference['global']} if reference else {}
    reference_date={(x['Model'],int(x['Seed']),x['Date']):x for x in reference['per_date']} if reference else {}
    global_rows=[];date_rows=[];differences=[]
    for run in items:
        model=run['model'];seed=int(run['seed']);filename=run['predictions']
        path=Path(filename)
        if not path.is_absolute():path=(manifest_path.parent/path).resolve()
        print('Recomputing',model,seed,'from',path.name,flush=True)
        data=json.loads(path.read_text(encoding='utf-8'))
        verify_inputs(rawgt,data,image_ids)
        predictions=defaultdict(list)
        for detection in data:predictions[detection['image_id']].append(prepare_mask(detection))
        image_matches={}
        for imageid in image_ids:
            scores,matched=match_image(gt_by_img[imageid],predictions.get(imageid,[]))
            image_matches[imageid]=(scores,matched,len(gt_by_img[imageid]))
        result=ap_score(image_matches,image_ids)
        row={'Model':model,'Seed':seed,**{key:result[key] for key in ['AP50_95','AP50','AP75']},'num_predictions':len(data),'prediction_sha256':filehash(path)}
        if reference:
            ref=reference_global[(model,seed)]
            row['maximum_absolute_delta']=max(abs(result[z]-ref['Mask_'+z]) for z in ('AP50_95','AP50','AP75'))
            differences.extend(result[z]-ref['Mask_'+z] for z in ('AP50_95','AP50','AP75'))
        global_rows.append(row)
        for date,date_ids in sorted(dates.items()):
            dr=ap_score(image_matches,date_ids)
            entry={'Model':model,'Seed':seed,'Date':date,'Images':len(date_ids),**{key:dr[key] for key in ['AP50_95','AP50','AP75']}}
            date_rows.append(entry)
            if reference:
                ref=reference_date[(model,seed,date)]
                if ref['Images']!=len(date_ids):raise ValueError('Date image counts differ')
                differences.extend(dr[z]-ref['Mask_'+z] for z in ('AP50_95','AP50','AP75'))
        print('  AP@[.50:.95]:',format(result['AP50_95'],'.12f'),flush=True)
    maxdiff=max((abs(d) for d in differences), default=None)
    report={'status':'PASS' if maxdiff is None or maxdiff<1e-9 else 'FAIL','implementation':'Independent NumPy mask-RLE evaluator; not official pycocotools','official_pycocotools_evaluation':False,'gt_file_sha256':filehash(gt_path),'reference_file_sha256':filehash(reference_path) if reference_path else None,'gt_image_count':len(rawgt['images']),'gt_instances':len(rawgt['annotations']),'date_groups':len(dates),'run_count':len(global_rows),'date_run_count':len(date_rows),'checked_scalar_metrics':len(differences),'max_absolute_delta':maxdiff,'global':global_rows,'per_date':date_rows}
    out.mkdir(parents=True,exist_ok=True)
    (out/'independent_coco_recomputed.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    import csv
    for name,table,cols in [('global',global_rows,['Model','Seed','AP50_95','AP50','AP75','num_predictions','prediction_sha256','maximum_absolute_delta']),('by_date',date_rows,['Model','Seed','Date','Images','AP50_95','AP50','AP75'])]:
        with (out/f'independent_{name}.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(table)
    print('Summary:',report['status'],'comparisons',len(differences),'max abs delta',maxdiff,flush=True)
    if report['status']!='PASS':raise SystemExit(1)
    return report


def self_test():
    # Three synthetic masks with uncompressed COCO RLE (avoids reliance on source data).
    h=3;w=3
    a={'image_id':1,'score':1.0,'segmentation':{'size':[h,w],'counts':[0,2,7]}}
    b={'image_id':1,'score':0.9,'segmentation':{'size':[h,w],'counts':[0,2,7]}}
    c={'image_id':1,'score':0.7,'segmentation':{'size':[h,w],'counts':[3,2,4]}}
    m=prepare_mask(a);n=prepare_mask(b);z=prepare_mask(c)
    assert m['area']==2 and get_iou(m['int'],n['int'],m['area'],n['area'])==1
    assert get_iou(m['int'],z['int'],m['area'],z['area'])==0
    scores,matched=match_image([m],[n,z]);sc=ap_score({1:(scores,matched,1)},[1])
    assert abs(sc['AP50_95']-1)<1e-12 and abs(sc['AP50']-1)<1e-12
    print('PASS synthetic compressed-RLE compatible mask overlap and COCO interpolated AP controls')


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ground-truth',type=Path,help='COCO test ground truth JSON')
    p.add_argument('--prediction-map',type=Path,help='Local JSON of runs; see docs/INDEPENDENT_COCO_AUDIT.md')
    p.add_argument('--reference',type=Path,default=None,help='Optional saved Experiment 33 report to compare, never for metric computation')
    p.add_argument('--out',type=Path,default=Path('outputs/independent_coco'))
    p.add_argument('--self-test',action='store_true')
    args=p.parse_args()
    if args.self_test:return self_test()
    if not args.ground_truth or not args.prediction_map:p.error('--ground-truth and --prediction-map are required')
    audit(args.ground_truth,args.prediction_map,args.reference,args.out)

if __name__=='__main__':main()
