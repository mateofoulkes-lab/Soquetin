from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('Prototipo V1.14:','Prototipo V1.15:',1)
s=s.replace('Recuperador de password de Soquetin · V1.14','Recuperador de password de Soquetin · V1.15',1)
s=s.replace('poster03-protocolo-v2.jpg','poster03-protocolo-v3.jpg',1)
s=s.replace("nearbyPoster=(best && bestD<7.3) ? best : null; // about 2.7 m","nearbyPoster=(best && bestD<20.25) ? best : null; // about 4.5 m",1)
old="""    document.addEventListener('pointerdown',e=>{\n      if(posterOverlayOpen || !nearbyPoster)return;\n      if(pointerInsidePoster(nearbyPoster,e.clientX,e.clientY)){\n        e.preventDefault();\n        e.stopPropagation();\n        openPoster(nearbyPoster);\n      }\n    },true);\n"""
new="""    document.addEventListener('pointerdown',e=>{\n      if(posterOverlayOpen || P.dead)return;\n      let hitPoster=null, bestD=Infinity;\n      for(const poster of posters){\n        const dx=poster.position.x-P.pos.x;\n        const dy=poster.position.y-(P.pos.y+.65);\n        const dz=poster.position.z-P.pos.z;\n        const d=dx*dx+dy*dy+dz*dz;\n        if(d<=20.25 && d<bestD && pointerInsidePoster(poster,e.clientX,e.clientY)){\n          hitPoster=poster; bestD=d;\n        }\n      }\n      if(hitPoster){\n        e.preventDefault();\n        e.stopImmediatePropagation();\n        openPoster(hitPoster);\n      }\n    },true);\n"""
if old not in s: raise SystemExit('pointer handler not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('patched V1.15')
