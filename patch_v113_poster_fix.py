from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('Prototipo V1.12:','Prototipo V1.13:',1)
s=s.replace('Recuperador de password de Soquetin · V1.12','Recuperador de password de Soquetin · V1.13',1)

# Posters must display their raster artwork exactly, independent from dungeon lighting.
s=s.replace("const mat=new THREE.MeshStandardMaterial({map:tex,roughness:.65});","const mat=new THREE.MeshBasicMaterial({map:tex,toneMapped:false,side:THREE.DoubleSide});")

old="""    renderer.domElement.addEventListener('pointerdown',e=>{\n      if(posterOverlayOpen || !nearbyPoster)return;\n      const r=renderer.domElement.getBoundingClientRect();\n      const ndc=new THREE.Vector2(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);\n      raycaster.setFromCamera(ndc,camera);\n      const hit=raycaster.intersectObjects(posters,false)[0];\n      if(hit && hit.object===nearbyPoster){ e.preventDefault(); openPoster(hit.object); }\n    });\n"""
new="""    // Capture poster taps BEFORE the mobile joystick zones can consume them.\n    document.addEventListener('pointerdown',e=>{\n      if(posterOverlayOpen || !nearbyPoster)return;\n      const r=renderer.domElement.getBoundingClientRect();\n      if(e.clientX<r.left || e.clientX>r.right || e.clientY<r.top || e.clientY>r.bottom)return;\n      const ndc=new THREE.Vector2(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);\n      raycaster.setFromCamera(ndc,camera);\n      const hit=raycaster.intersectObjects(posters,false)[0];\n      if(hit && hit.object===nearbyPoster){\n        e.preventDefault();\n        e.stopPropagation();\n        openPoster(hit.object);\n      }\n    },true);\n"""
if old not in s:
    raise SystemExit('poster pointer handler not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('patched V1.13 poster visibility/touch')
