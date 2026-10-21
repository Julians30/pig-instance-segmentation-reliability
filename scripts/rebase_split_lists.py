#!/usr/bin/env python3
"""Reconstruct local split TXT files/YAML from the frozen, original author manifests.

No dataset files are downloaded, copied, or changed. The script only writes local
absolute image path lists and a YAML config under --out-dir (ignored by git).
"""
import argparse
from pathlib import Path
import json

SPLITS=("train","val","test")

def relative_from_author_path(raw):
    # The upstream physical train/val/test folder is independent of OUR date split.
    separator="/FaroPigSeg/"
    if separator not in raw.replace('\\','/'):
        raise ValueError(f'Image path has no frozen FaroPigSeg directory: {raw!r}')
    relative=raw.replace('\\','/').rsplit(separator,1)[1]
    if not relative or relative.startswith('/') or '..' in Path(relative).parts:
        raise ValueError(f'Unsafe image path: {raw!r}')
    return relative

def run(dataset_root, source_dir, out_dir, strict):
    dataset_root=dataset_root.expanduser().resolve()
    source_dir=source_dir.expanduser().resolve()
    out_dir=out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True,exist_ok=True)
    n={}
    for split in SPLITS:
        src=source_dir/f'{split}.txt'
        original=[x.strip() for x in src.read_text(encoding='utf-8').splitlines() if x.strip()]
        mapped=[]
        for x in original:
            relative=relative_from_author_path(x)
            candidate=dataset_root/relative
            if strict and not candidate.is_file():
                raise FileNotFoundError(f'{split}: {candidate} is not a file; verify extraction root')
            mapped.append(str(candidate))
        (out_dir/f'{split}.txt').write_text('\n'.join(mapped)+'\n',encoding='utf-8')
        n[split]=len(mapped)
    q=lambda value:json.dumps(str(value),ensure_ascii=False)
    yaml=f'path: {q(dataset_root)}\n'+''.join(f'{s}: {q(out_dir/(s+".txt"))}\n' for s in SPLITS)+ 'names:\n  0: cerdo\n'
    (out_dir/'data_fecha_local.yaml').write_text(yaml,encoding='utf-8')
    print('Local split generated:',out_dir, n)
    if n!={'train':949,'val':196,'test':373}:
        raise ValueError('Split counts differ from frozen source; inspect files')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset-root',type=Path,required=True)
    parser.add_argument('--source-dir',type=Path,default=Path(__file__).resolve().parents[1]/'data'/'partitions')
    parser.add_argument('--out-dir',type=Path,default=Path('outputs/local_split'))
    parser.add_argument('--strict',action='store_true',help='Require each upstream image to exist')
    args=parser.parse_args()
    run(args.dataset_root,args.source_dir,args.out_dir,args.strict)
if __name__=='__main__':main()
