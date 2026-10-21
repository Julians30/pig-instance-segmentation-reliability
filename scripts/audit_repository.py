#!/usr/bin/env python3
"""Static, offline verification of frozen split, notebook sources and result records.

This is NOT a CUDA training or COCO mask AP reproduction.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math
import re
import statistics
import sys

ROOT=Path(__file__).resolve().parents[1]
FILE_HASHES={
'particion_fecha_manifest.json':'27ba2e77c188d360bc5d6cbac2a2e2bf0ec929448ae082e49e583e222ad48cd3',
'data_fecha_original.yaml':'9a223b47038c661303c1d12a35cbdcb212ed51529c8c773c4c9c66998706d1d9',
'train.txt':'17b343f693a62714ebe0d1629b30ec8daff9c7081a1f4234f90ab11107921281',
'val.txt':'6368e3c82d001e33035cdb46ea6c7882ad599d22a06d885a22d8177549619e9d',
'test.txt':'0d31f2b3bc931c6f08c96544df8fdb1f91c3b6bea5da4624917e94da97e01c05',
}


def run():
    errors=[]
    def ck(condition,message):
        if not condition:errors.append(message)
    splits=ROOT/'data'/'partitions'
    assignments=json.loads((splits/'particion_fecha_manifest.json').read_text(encoding='utf-8'))['asignaciones_fecha']
    ck(len(assignments)==25,'Expected 25 acquisition dates')
    seen=set()
    for group,expected,dates in [('train',949,16),('val',196,4),('test',373,5)]:
        lines=[l for l in (splits/f'{group}.txt').read_text(encoding='utf-8').splitlines() if l.strip()]
        ck(len(lines)==expected,f'{group}: expected {expected} images, got {len(lines)}')
        grp_dates=set()
        for line in lines:
            m=re.search(r'(20\d{2}-\d{2}-\d{2})',Path(line).name)
            ck(bool(m),f'No acquisition date in {line}')
            if not m:continue
            d=m.group(1);grp_dates.add(d)
            ck(assignments.get(d)==group,f'Date group leakage or missing allocation: {d} in {group}')
            ck(line not in seen,f'Duplicate image path across splits: {line}')
            seen.add(line)
        ck(len(grp_dates)==dates,f'{group}: expected {dates} dates, got {len(grp_dates)}')
    for name,expected in FILE_HASHES.items():
        actual=hashlib.sha256((splits/name).read_bytes()).hexdigest()
        ck(actual==expected,f'Original split fingerprint mismatch: {name}')
    provenance=json.loads((ROOT/'docs'/'NOTEBOOK_PROVENANCE.json').read_text(encoding='utf-8'))
    ck(len(provenance)==34,'Expected 34 cleaned notebooks')
    published=list((ROOT/'notebooks').rglob('*.ipynb'))
    ck(len(published)==34,f'Expected 34 .ipynb files, got {len(published)}')
    for item in provenance:
        p=ROOT/item['github_path']
        ck(p.exists(),f'Missing notebook {p}')
        if not p.exists():continue
        x=json.loads(p.read_text(encoding='utf-8'))
        ck(x.get('nbformat')==4,f'Unexpected notebook format: {p}')
        for i,c in enumerate(x.get('cells',[])):
            if c.get('cell_type')=='code':
                ck(not c.get('outputs'),f'Nonempty captured output in {p}, cell {i}')
                ck(c.get('execution_count') is None,f'Execution counter in {p}, cell {i}')
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        ck(actual==item['release_sha256'],f'Notebook content drift from published provenance: {p}')
    report=json.loads((ROOT/'results'/'reports'/'CERDOS_33_Informe_Final.json').read_text(encoding='utf-8'))
    rows=report['global']; per=report['per_date']
    ck(len(rows)==9,f'Expected 9 global metrics, got {len(rows)}')
    ck(len(per)==45,f'Expected 45 model-seed-date entries, got {len(per)}')
    seedgroups={}
    for r in rows:
        seedgroups.setdefault(r['Model'],set()).add(int(r['Seed']))
        ck(r['Images']==373 and r['GT_instances']==4648,'Unexpected GT/test dimensions')
        ck(0<=r['Mask_AP50_95']<=1,'Invalid COCO AP entry')
    ck(len(seedgroups)==3 and all(seeds=={2026,2027,2028} for seeds in seedgroups.values()),f'Incomplete 3x3 seed coverage: {seedgroups}')
    protocol=json.loads((ROOT/'results'/'reports'/'CERDOS_33_Protocolo.json').read_text(encoding='utf-8'))
    ck(protocol['test_txt_sha256']==FILE_HASHES['test.txt'],'Test file provenance disagrees with COCO report')
    ck(protocol['manifest_sha256']==FILE_HASHES['particion_fecha_manifest.json'],'Manifest provenance disagrees with COCO report')
    for name,expected in [('YOLO11n-seg',0.8633),('YOLO26n-seg',0.8474),('Mask R-CNN',0.7947)]:
        vals=[r['Mask_AP50_95'] for r in rows if r['Model']==name]
        ck(len(vals)==3 and abs(statistics.mean(vals)-expected)<0.00007,f'Unexpected AP summary for {name}')
    if errors:
        print('REPOSITORY AUDIT FAILED:',len(errors),'problem(s)')
        for e in errors: print('  ERROR:',e)
        return 1
    print('PASS: 34 notebooks, zero stored outputs, 25 disjoint dates, 1,518 split images, original SHA-256, 9 COCO runs, 45 per-date entries')
    print('NOTE: Static provenance only; no full training, prediction reconstruction or independent COCOeval performed.')
    return 0
if __name__=='__main__':sys.exit(run())
