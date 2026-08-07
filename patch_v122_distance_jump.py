from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('V1.21 · interacción de afiches simplificada','V1.22 · distancia de afiches + salto',1)

# Poster prompt proximity: 1.5 m => squared distance 2.25.
s=s.replace("nearbyPoster=(best && bestD<20.25) ? best : null; // about 4.5 m","nearbyPoster=(best && bestD<2.25) ? best : null; // about 1.5 m",1)

# +10% vertical jump velocity, horizontal movement unchanged.
s=s.replace('P.vel.y=4.03;','P.vel.y=4.433;',1)
s=s.replace('beginJumpTilt(4.03);','beginJumpTilt(4.433);',1)
s=s.replace('P.vel.y=2.35;','P.vel.y=2.585;',1)
s=s.replace('beginJumpTilt(2.35);','beginJumpTilt(2.585);',1)

p.write_text(s,encoding='utf-8')
print('patched V1.22')
