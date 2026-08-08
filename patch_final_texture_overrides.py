from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

new_block=r'''    const SOQUETIN_TEXTURE_OVERRIDES = {
      "floor@0,-0.12,9#face2": {"scope":"face","repeatU":3.5,"repeatV":1.15,"offsetU":0,"offsetV":0,"rotation":0},
      "floor@0,-0.12,2.5#face2": {"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-1,"offsetV":-1,"rotation":0},
      "floor@7,-0.12,2.5#face2": {"scope":"face","repeatU":1.1,"repeatV":0.8,"offsetU":-0.82,"offsetV":0,"rotation":0},
      "lintel@7,3.7,-13.04#face0": {"scope":"face","repeatU":4.35,"repeatV":2,"offsetU":0,"offsetV":0,"rotation":0},
      "lintel@7,3.7,-13.04#face4": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":0,"offsetV":0.09,"rotation":0},
      "lintel@7,3.7,-13.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":0.07,"offsetV":-0.03,"rotation":0},
      "lintel@0,3.7,-13.04#face0": {"scope":"face","repeatU":0.1,"repeatV":2,"offsetU":0,"offsetV":0,"rotation":0},
      "lintel@0,3.7,-13.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.06,"offsetV":-0.04,"rotation":0},
      "lintel@-7,3.7,-13.04#face0": {"scope":"face","repeatU":1.75,"repeatV":2,"offsetU":0,"offsetV":0,"rotation":0},
      "lintel@-7,3.7,-13.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.07,"offsetV":-0.04,"rotation":0},
      "wall@-5.55,2.5,-20.04#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@-5.55,2.5,-20.04#object": {"scope":"object","repeatU":3.5,"repeatV":5.05,"offsetU":0.78,"offsetV":0,"rotation":0},
      "wall@5.55,2.5,-20.04#object": {"scope":"object","repeatU":2.85,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "lintel@0,3.7,-20.04#object": {"scope":"object","repeatU":0.35,"repeatV":2.65,"offsetU":-0.11,"offsetV":0.22,"rotation":0},
      "floor@0,-0.12,-16.54#object": {"scope":"object","repeatU":3.5,"repeatV":1.35,"offsetU":-7.06,"offsetV":0.33,"rotation":0},
      "floor@7,-0.12,-10.54#object": {"scope":"object","repeatU":1.15,"repeatV":0.75,"offsetU":0,"offsetV":1.63,"rotation":0},
      "floor@-7,-0.12,-10.54#object": {"scope":"object","repeatU":1.2,"repeatV":0.75,"offsetU":-1.12,"offsetV":0.03,"rotation":0},
      "lintel@0,3.7,-20.04#face5": {"scope":"face","repeatU":0.4,"repeatV":2.65,"offsetU":-0.02,"offsetV":0.22,"rotation":0},
      "wall@5.75,2.5,-24.04#face0": {"scope":"face","repeatU":2,"repeatV":2.6,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@5.75,2.5,-24.04#face1": {"scope":"face","repeatU":2,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@1,2.5,-28.04#face4": {"scope":"face","repeatU":3.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@-3.75,2.5,-24.04#face0": {"scope":"face","repeatU":2.55,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "floor@1,-0.12,-24.04#face2": {"scope":"face","repeatU":1.55,"repeatV":1.45,"offsetU":-0.14,"offsetV":0.01,"rotation":0},
      "wall@-3.5,2.5,-13.04#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@-3.5,2.5,-13.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
      "wall@3.5,2.5,-13.04#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@9.05,2.5,-13.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-0.07,"offsetV":0,"rotation":0},
      "wall@9.05,2.5,5#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0},
      "wall@3.5,2.5,5#face0": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-0.03,"offsetV":0,"rotation":0},
      "wall@-3.5,2.5,5#face0": {"scope":"face","repeatU":0.1,"repeatV":5,"offsetU":-0.07,"offsetV":0,"rotation":0},
      "wall@3.5,2.5,5#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":-1.77,"offsetV":0,"rotation":0},
      "wall@-3.5,2.5,5#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
      "lintel@0,3.7,-13.04#face4": {"scope":"face","repeatU":0.4,"repeatV":2.6,"offsetU":-0.74,"offsetV":-0.04,"rotation":0},
      "wall@3.5,2.5,-13.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0.92,"offsetV":0.75,"rotation":0},
      "lintel@-7,3.7,-13.04#face4": {"scope":"face","repeatU":0.55,"repeatV":2.6,"offsetU":-0.93,"offsetV":0.08,"rotation":0},
      "wall@5.55,2.5,-20.04#face1": {"scope":"face","repeatU":0.1,"repeatV":5.05,"offsetU":0,"offsetV":0,"rotation":0}
    };'''

pat=r'    const SOQUETIN_TEXTURE_OVERRIDES = \{.*?\n    \};'
s2,n=re.subn(pat,new_block,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'override block replacement count={n}')
p.write_text(s2,encoding='utf-8')
print('final texture overrides applied:', n)
