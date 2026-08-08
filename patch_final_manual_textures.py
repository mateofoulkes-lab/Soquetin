from pathlib import Path
import re

idxp=Path('index.html')
edp=Path('texture-editor.html')
idx=idxp.read_text(encoding='utf-8')
ed=edp.read_text(encoding='utf-8')

new=r'''{
  "wall@0,2.5,13#face0": {"scope":"face","repeatU":18.65,"repeatV":17.55,"offsetU":3.36,"offsetV":3.18,"rotation":95},
  "floor@0,-0.12,9#face2": {"scope":"face","repeatU":3.5,"repeatV":1.15,"offsetU":0,"offsetV":0,"rotation":0},
  "floor@0,-0.12,9#face0": {"scope":"face","repeatU":9.3,"repeatV":22.65,"offsetU":-7.06,"offsetV":0.33,"rotation":0},
  "wall@0,2.5,13#face5": {"scope":"face","repeatU":7.05,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-10.5,2.5,-3.52#face0": {"scope":"face","repeatU":12.7,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-9.05,2.5,5#object": {"scope":"object","repeatU":1.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-9.05,2.5,5#face0": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-1.75,"offsetV":0,"rotation":0},
  "lintel@-7,3.7,5#face4": {"scope":"face","repeatU":0.4,"repeatV":2.6,"offsetU":0,"offsetV":-0.42,"rotation":0},
  "wall@-3.5,2.5,5#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":-0.07,"offsetV":0,"rotation":0},
  "wall@-3.5,2.5,5#object": {"scope":"object","repeatU":1.95,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
  "lintel@-7,3.7,5#face5": {"scope":"face","repeatU":0.4,"repeatV":2.6,"offsetU":0.01,"offsetV":0.08,"rotation":0},
  "floor@-7,-0.12,2.5#face2": {"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-0.81,"offsetV":0,"rotation":0},
  "floor@-7,-0.12,5#face2": {"scope":"face","repeatU":3.95,"repeatV":17.25,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@10.5,2.5,-3.52#object": {"scope":"object","repeatU":9.3,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@9.05,2.5,5#object": {"scope":"object","repeatU":0.8,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "lintel@7,3.7,5#object": {"scope":"object","repeatU":0.45,"repeatV":2.65,"offsetU":0.03,"offsetV":-0.03,"rotation":0},
  "wall@3.5,2.5,5#object": {"scope":"object","repeatU":2,"repeatV":5.05,"offsetU":-0.03,"offsetV":0,"rotation":0},
  "lintel@0,3.7,5#object": {"scope":"object","repeatU":0.4,"repeatV":2.6,"offsetU":0.03,"offsetV":0.08,"rotation":0},
  "wall@3.5,2.5,-4.02#object": {"scope":"object","repeatU":5.35,"repeatV":5.05,"offsetU":0.71,"offsetV":0,"rotation":0},
  "floor@0,-0.12,9#object": {"scope":"object","repeatU":3.65,"repeatV":1.4,"offsetU":-7.06,"offsetV":0.33,"rotation":0},
  "floor@0,-0.12,2.5#object": {"scope":"object","repeatU":1.1,"repeatV":0.8,"offsetU":-1.31,"offsetV":0.07,"rotation":0},
  "wall@-3.5,2.5,-4.02#object": {"scope":"object","repeatU":5.35,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@9.05,2.5,5#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "floor@7,-0.12,2.5#face2": {"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-0.82,"offsetV":0,"rotation":0},
  "floor@0,-0.12,2.5#face2": {"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-1,"offsetV":-1,"rotation":0},
  "wall@-3.5,2.5,5#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
  "wall@3.5,2.5,5#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-1.77,"offsetV":0,"rotation":0},
  "wall@3.5,2.5,5#face0": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-0.03,"offsetV":0,"rotation":0},
  "floor@7,-0.12,-10.54#object": {"scope":"object","repeatU":1.15,"repeatV":0.75,"offsetU":0,"offsetV":1.63,"rotation":0},
  "lintel@7,3.7,-13.04#face4": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":1.91,"offsetV":0.09,"rotation":0},
  "wall@3.5,2.5,-13.04#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@9.05,2.5,-13.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-0.07,"offsetV":0,"rotation":0},
  "floor@0,-0.12,-16.54#object": {"scope":"object","repeatU":3.5,"repeatV":1.35,"offsetU":-7.06,"offsetV":0.33,"rotation":0},
  "wall@5.55,2.5,-20.04#object": {"scope":"object","repeatU":2.85,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "lintel@7,3.7,-13.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":0.07,"offsetV":-0.03,"rotation":0},
  "lintel@0,3.7,-13.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.06,"offsetV":-0.04,"rotation":0},
  "lintel@-7,3.7,-13.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":0.2,"offsetV":-0.04,"rotation":0},
  "wall@-3.5,2.5,-13.04#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-3.5,2.5,-13.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
  "wall@3.5,2.5,-13.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
  "floor@-7,-0.12,-10.54#object": {"scope":"object","repeatU":1.2,"repeatV":0.75,"offsetU":-1.12,"offsetV":0.03,"rotation":0},
  "lintel@-7,3.7,-13.04#face4": {"scope":"face","repeatU":0.55,"repeatV":2.6,"offsetU":-0.93,"offsetV":0.08,"rotation":0},
  "lintel@0,3.7,-13.04#face4": {"scope":"face","repeatU":0.4,"repeatV":2.6,"offsetU":-0.74,"offsetV":-0.04,"rotation":0},
  "wall@-5.55,2.5,-20.04#object": {"scope":"object","repeatU":3.5,"repeatV":5.05,"offsetU":0.78,"offsetV":0,"rotation":0},
  "lintel@0,3.7,-20.04#object": {"scope":"object","repeatU":0.35,"repeatV":2.65,"offsetU":-0.11,"offsetV":0.22,"rotation":0},
  "floor@1,-0.12,-24.04#face2": {"scope":"face","repeatU":1.55,"repeatV":1.45,"offsetU":-0.14,"offsetV":0.01,"rotation":0},
  "wall@1,2.5,-28.04#face4": {"scope":"face","repeatU":3.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-3.75,2.5,-24.04#face0": {"scope":"face","repeatU":2.55,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@5.75,2.5,-24.04#face1": {"scope":"face","repeatU":2,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "lintel@0,3.7,-20.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.02,"offsetV":0.22,"rotation":0},
  "wall@5.55,2.5,-20.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-5.55,2.5,-20.04#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@-3.5,2.5,-13.04#face4": {"scope":"face","repeatU":2,"repeatV":5.05,"offsetU":0.21,"offsetV":0,"rotation":0},
  "wall@3.5,2.5,-13.04#face4": {"scope":"face","repeatU":2,"repeatV":5.05,"offsetU":-0.03,"offsetV":0,"rotation":0},
  "wall@3.5,2.5,-13.04#face5": {"scope":"face","repeatU":1.95,"repeatV":5.05,"offsetU":0.07,"offsetV":0,"rotation":0},
  "wall@-3.5,2.5,-13.04#face5": {"scope":"face","repeatU":2,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
  "wall@9.05,2.5,-13.04#face5": {"scope":"face","repeatU":0.95,"repeatV":5.05,"offsetU":0.21,"offsetV":0,"rotation":0},
  "wall@-9.05,2.5,-13.04#face5": {"scope":"face","repeatU":1.1,"repeatV":5.05,"offsetU":0.79,"offsetV":0,"rotation":0},
  "wall@9.05,2.5,-13.04#face4": {"scope":"face","repeatU":1,"repeatV":5.05,"offsetU":1.38,"offsetV":0,"rotation":0}
}'''

# Replace game table.
idx2,n=re.subn(r'    const SOQUETIN_TEXTURE_OVERRIDES = \{.*?\n    \};', '    const SOQUETIN_TEXTURE_OVERRIDES = '+new+';', idx, count=1, flags=re.S)
if n!=1: raise SystemExit(f'index table replacement count={n}')
idx=idx2

# Make same table the editor A baseline.
ed2,n=re.subn(r'const TEXTURE_TABLE_A = \{.*?\n    \};', 'const TEXTURE_TABLE_A = '+new+';', ed, count=1, flags=re.S)
if n!=1: raise SystemExit(f'editor A replacement count={n}')
ed=ed2

# Force one-time reset of mix storage to this new baseline.
ed=re.sub(r"const AB_MIX_VERSION='\d+';", "const AB_MIX_VERSION='4';", ed, count=1)

idxp.write_text(idx,encoding='utf-8')
edp.write_text(ed,encoding='utf-8')
print('manual texture corrections applied to game and editor A baseline')
