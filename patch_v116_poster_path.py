from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('Prototipo V1.15:','Prototipo V1.16:',1)
s=s.replace('Recuperador de password de Soquetin · V1.15','Recuperador de password de Soquetin · V1.16',1)
s=s.replace("poster03-protocolo-v3.jpg","poster03.jpg",1)
p.write_text(s,encoding='utf-8')
print('patched V1.16')
