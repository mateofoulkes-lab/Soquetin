from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
css="""    #buildInfo {\n      position:fixed; left:10px; bottom:9px; z-index:55; padding:6px 8px; border-radius:7px;\n      background:rgba(0,0,0,.42); border:1px solid rgba(255,255,255,.10); color:rgba(255,255,255,.72);\n      font:600 10px/1.25 ui-monospace,monospace; pointer-events:none; backdrop-filter:blur(4px);\n    }\n"""
s=s.replace(css,'',1)
s=s.replace('  <div id="buildInfo">V1.24 · proximidad cilíndrica de afiches</div>\n\n','',1)
p.write_text(s,encoding='utf-8')
print('removed on-screen build/version indicator')
