from pathlib import Path
import re, subprocess

p=Path('index.html')
current=p.read_text(encoding='utf-8')
old=subprocess.check_output(['git','show','5c5308cdb13d18ddb5e8c0324db32c7580aea5d9:index.html'], text=True)
pat=r'    const SOQUETIN_TEXTURE_OVERRIDES = \{.*?\n    \};'
m=re.search(pat,old,re.S)
if not m:
    raise SystemExit('stable texture block not found')
rolled,n=re.subn(pat,m.group(0),current,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'current texture block replacement count={n}')
p.write_text(rolled,encoding='utf-8')
print('restored previous stable texture override block')
