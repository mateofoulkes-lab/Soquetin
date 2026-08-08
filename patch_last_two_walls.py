from pathlib import Path
import re

idxp=Path('index.html')
edp=Path('texture-editor.html')
idx=idxp.read_text(encoding='utf-8')
ed=edp.read_text(encoding='utf-8')

# 1) Manual lintel correction.
old='"lintel@-7,3.7,-13.04#face4": {"scope":"face","repeatU":0.55,"repeatV":2.6,"offsetU":-0.93,"offsetV":0.08,"rotation":0}'
new='"lintel@-7,3.7,-13.04#face4": {"scope":"face","repeatU":0.45,"repeatV":2.6,"offsetU":-0.96,"offsetV":0.08,"rotation":0}'
if old not in idx:
    raise SystemExit('lintel old value not found')
idx=idx.replace(old,new,1)

# 2) Add the two missing face overrides for the same wall.
anchor='"wall@9.05,2.5,-13.04#face4": {"scope":"face","repeatU":1,"repeatV":5.05,"offsetU":1.38,"offsetV":0,"rotation":0}'
addition=anchor+',\n  "wall@-9.05,2.5,-13.04#face4": {"scope":"face","repeatU":1.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},\n  "wall@-9.05,2.5,-13.04#face0": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0}'
if '"wall@-9.05,2.5,-13.04#face4"' not in idx:
    if anchor not in idx: raise SystemExit('wall insertion anchor not found')
    idx=idx.replace(anchor,addition,1)

idxp.write_text(idx,encoding='utf-8')

# 3) Make exact corrected game table the editor A/default baseline.
m=re.search(r'const SOQUETIN_TEXTURE_OVERRIDES\s*=\s*(\{.*?\n\s*\});', idx, re.S)
if not m: raise SystemExit('game texture table not found after patch')
current=m.group(1)
start=ed.find('const TEXTURE_TABLE_A =')
end=ed.find('const TEXTURE_TABLE_B =',start)
if start<0 or end<0: raise SystemExit('editor A/B anchors not found')
ed=ed[:start]+'const TEXTURE_TABLE_A = '+current+';\n'+ed[end:]
vm=re.search(r"const AB_MIX_VERSION='(\d+)';",ed)
if not vm: raise SystemExit('AB_MIX_VERSION not found')
newver=str(int(vm.group(1))+1)
ed=ed[:vm.start()]+f"const AB_MIX_VERSION='{newver}';"+ed[vm.end():]
edp.write_text(ed,encoding='utf-8')
print('last wall corrections applied and editor baseline synchronized')
