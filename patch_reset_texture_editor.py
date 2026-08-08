from pathlib import Path
import re

idxp=Path('index.html')
edp=Path('texture-editor.html')
idx=idxp.read_text(encoding='utf-8')
ed=edp.read_text(encoding='utf-8')

m=re.search(r'const SOQUETIN_TEXTURE_OVERRIDES\s*=\s*(\{.*?\n\s*\});', idx, re.S)
if not m:
    raise SystemExit('current game texture table not found')
current=m.group(1)

# Replace editor A baseline with the exact current game table.
start=ed.find('const TEXTURE_TABLE_A =')
end=ed.find('const TEXTURE_TABLE_B =', start)
if start<0 or end<0:
    raise SystemExit('A/B table anchors not found in texture-editor.html')
replacement='const TEXTURE_TABLE_A = '+current+';\n'
ed=ed[:start]+replacement+ed[end:]

# Force one-time localStorage reset to the new baseline.
vm=re.search(r"const AB_MIX_VERSION='(\d+)';", ed)
if vm:
    newver=str(int(vm.group(1))+1)
    ed=ed[:vm.start()]+f"const AB_MIX_VERSION='{newver}';"+ed[vm.end():]
else:
    raise SystemExit('AB_MIX_VERSION not found')

edp.write_text(ed,encoding='utf-8')
print('texture editor reset to current game textures as A baseline')
