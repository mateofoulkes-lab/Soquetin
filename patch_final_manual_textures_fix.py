from pathlib import Path
import re

src=Path('patch_final_manual_textures.py').read_text(encoding='utf-8')
m=re.search(r"new=r'''(\{.*?\})'''",src,re.S)
if not m: raise SystemExit('embedded final table not found')
new=m.group(1)

idxp=Path('index.html'); edp=Path('texture-editor.html')
idx=idxp.read_text(encoding='utf-8'); ed=edp.read_text(encoding='utf-8')

# Game: replace from declaration up to next helper function, independent of whitespace.
start=idx.index('    const SOQUETIN_TEXTURE_OVERRIDES = ')
end=idx.index('\n\n    function textureCoord',start)
idx=idx[:start]+'    const SOQUETIN_TEXTURE_OVERRIDES = '+new+';'+idx[end:]

# Editor: replace A exactly between A and B declarations.
start=ed.index('const TEXTURE_TABLE_A = ')
end=ed.index('\nconst TEXTURE_TABLE_B = ',start)
ed=ed[:start]+'const TEXTURE_TABLE_A = '+new+';'+ed[end:]

# New baseline => one-time localStorage migration.
ed=re.sub(r"const AB_MIX_VERSION='\d+';", "const AB_MIX_VERSION='4';", ed, count=1)

idxp.write_text(idx,encoding='utf-8')
edp.write_text(ed,encoding='utf-8')
print('final manual texture table applied robustly')
