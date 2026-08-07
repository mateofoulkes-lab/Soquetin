from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('Prototipo V1: exploración 3D, saltos, losetas falsas, columnas, lava y respawn. El personaje provisional es un cubo.','Prototipo V1.2: exploración 3D, saltos, losetas falsas, columnas, lava y respawn. Modelo Soquetin GLB provisional integrado.')
s=s.replace('Recuperador de password de Soquetin · V1</div>','Recuperador de password de Soquetin · V1.2</div>')
p.write_text(s,encoding='utf-8')
print('version patched')