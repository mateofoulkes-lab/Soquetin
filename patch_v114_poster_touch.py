from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('Prototipo V1.13:','Prototipo V1.14:',1)
s=s.replace('Recuperador de password de Soquetin · V1.13','Recuperador de password de Soquetin · V1.14',1)
s=s.replace("poster03-protocolo.jpg","poster03-protocolo-v2.jpg")
old="""    // Capture poster taps BEFORE the mobile joystick zones can consume them.\n    document.addEventListener('pointerdown',e=>{\n      if(posterOverlayOpen || !nearbyPoster)return;\n      const r=renderer.domElement.getBoundingClientRect();\n      if(e.clientX<r.left || e.clientX>r.right || e.clientY<r.top || e.clientY>r.bottom)return;\n      const ndc=new THREE.Vector2(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);\n      raycaster.setFromCamera(ndc,camera);\n      const hit=raycaster.intersectObjects(posters,false)[0];\n      if(hit && hit.object===nearbyPoster){\n        e.preventDefault();\n        e.stopPropagation();\n        openPoster(hit.object);\n      }\n    },true);\n"""
new="""    // Screen-space poster hit testing: robust on mobile and independent from 3D raycasts.\n    function pointerInsidePoster(poster,clientX,clientY){\n      poster.updateWorldMatrix(true,false);\n      const r=renderer.domElement.getBoundingClientRect();\n      const w=poster.geometry.parameters.width, h=poster.geometry.parameters.height;\n      const corners=[\n        new THREE.Vector3(-w/2,-h/2,0), new THREE.Vector3(w/2,-h/2,0),\n        new THREE.Vector3(w/2,h/2,0), new THREE.Vector3(-w/2,h/2,0)\n      ];\n      let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity;\n      for(const c of corners){\n        c.applyMatrix4(poster.matrixWorld).project(camera);\n        const x=r.left+(c.x*.5+.5)*r.width;\n        const y=r.top+(-c.y*.5+.5)*r.height;\n        minX=Math.min(minX,x); maxX=Math.max(maxX,x);\n        minY=Math.min(minY,y); maxY=Math.max(maxY,y);\n      }\n      const pad=18;\n      return clientX>=minX-pad && clientX<=maxX+pad && clientY>=minY-pad && clientY<=maxY+pad;\n    }\n    document.addEventListener('pointerdown',e=>{\n      if(posterOverlayOpen || !nearbyPoster)return;\n      if(pointerInsidePoster(nearbyPoster,e.clientX,e.clientY)){\n        e.preventDefault();\n        e.stopPropagation();\n        openPoster(nearbyPoster);\n      }\n    },true);\n"""
if old not in s:
    raise SystemExit('V1.13 pointer handler not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('patched V1.14')
