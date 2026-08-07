from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('Prototipo V1.11:','Prototipo V1.12:',1)
s=s.replace('Recuperador de password de Soquetin · V1.11','Recuperador de password de Soquetin · V1.12',1)

# Fullscreen poster UI.
needle='''  </div>\n\n  <script type="module">'''
insert='''  </div>\n\n  <div id="posterPrompt" style="position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:18;display:none;padding:10px 16px;border-radius:10px;background:rgba(0,0,0,.68);border:1px solid rgba(255,255,255,.18);color:#fff;font:700 14px Inter,system-ui,sans-serif;pointer-events:none;backdrop-filter:blur(5px);white-space:nowrap">Toca la imagen o presiona F para ampliar...</div>\n  <div id="posterOverlay" style="position:fixed;inset:0;z-index:60;display:none;align-items:center;justify-content:center;padding:24px;background:rgba(0,0,0,.91);cursor:zoom-out">\n    <img id="posterOverlayImg" alt="Cartel ampliado" style="display:block;max-width:94vw;max-height:92vh;object-fit:contain;box-shadow:0 24px 90px rgba(0,0,0,.7);border:1px solid rgba(255,255,255,.16)">\n    <div style="position:absolute;right:18px;top:15px;color:#fff;font:600 12px Inter,system-ui,sans-serif;opacity:.72">F / ESC / toque para cerrar</div>\n  </div>\n\n  <script type="module">'''
if needle not in s: raise SystemExit('html UI needle missing')
s=s.replace(needle,insert,1)

start=s.index('    // ------------------------------------------------------------\n    // POSTERS / PLACEHOLDERS')
end=s.index('    // ------------------------------------------------------------\n    // LIGHTING', start)
new_posters='''    // ------------------------------------------------------------\n    // POSTERS / INTERACTIVE ARTWORK\n    // ------------------------------------------------------------\n    const posters=[];\n    function posterTexture(title,subtitle='PLACEHOLDER') {\n      return canvasTexture(512,(g,s)=>{\n        g.fillStyle='#d6cdb7'; g.fillRect(0,0,s,s);\n        g.strokeStyle='#191713'; g.lineWidth=18; g.strokeRect(9,9,s-18,s-18);\n        g.fillStyle='#1e1b17'; g.textAlign='center'; g.font='800 42px sans-serif';\n        const words=title.split(' '); let y=170;\n        for(const w of words){ g.fillText(w,s/2,y); y+=48; }\n        g.font='600 22px sans-serif'; g.fillStyle='#5b5143'; g.fillText(subtitle,s/2,390);\n      });\n    }\n    function registerPoster(mesh,source){\n      mesh.userData.posterSource=source;\n      posters.push(mesh);\n      return mesh;\n    }\n    function posterOnHorizontalWall(x,y,z,w,h,source,faceNorth=false,isExternal=false){\n      const tex=isExternal ? new THREE.TextureLoader().load(source,t=>{t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());}) : posterTexture(source);\n      const mat=new THREE.MeshStandardMaterial({map:tex,roughness:.65});\n      const p=new THREE.Mesh(new THREE.PlaneGeometry(w,h),mat);\n      p.position.set(x,y,z+(faceNorth?-.161:.161));\n      if(faceNorth) p.rotation.y=Math.PI;\n      scene.add(p);\n      const displaySource=isExternal ? source : tex.image.toDataURL('image/png');\n      return registerPoster(p,displaySource);\n    }\n    function posterOnRightWall(x,y,z,w,h,source,isExternal=false){\n      const tex=isExternal ? new THREE.TextureLoader().load(source,t=>{t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());}) : posterTexture(source,'PISTA FINAL');\n      const mat=new THREE.MeshStandardMaterial({map:tex,roughness:.65});\n      const p=new THREE.Mesh(new THREE.PlaneGeometry(w,h),mat);\n      p.position.set(x-.165,y,z); p.rotation.y=-Math.PI/2; scene.add(p);\n      const displaySource=isExternal ? source : tex.image.toDataURL('image/png');\n      return registerPoster(p,displaySource);\n    }\n\n    // All poster planes are 150% of their previous physical size.\n    posterOnHorizontalWall(-3.9,2.0,Z_CHALLENGE_SOUTH+.001,3.225,1.875,'IMAGEN 01',false,false);\n    posterOnHorizontalWall(3.9,2.0,Z_CHALLENGE_SOUTH+.001,3.225,1.875,'IMAGEN 02',false,false);\n    // Poster 03 uses the movement artwork. 3.75 / 2.175 matches its 1647:955 aspect ratio.\n    posterOnHorizontalWall(0,2.15,Z_START_FRONT-.001,3.75,2.175,'poster03-protocolo.svg',true,true);\n    posterOnHorizontalWall(-2.8,2.0,Z_COMMON_NORTH+.001,2.25,1.725,'PISTA',false,false);\n    posterOnRightWall(FINAL_RIGHT,2.15,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,3.30,2.175,'INSTAGRAM',false);\n\n'''
s=s[:start]+new_posters+s[end:]

# Input/overlay state before keyboard setup.
needle='''    const keys={};\n    let mouseLocked=false;\n    addEventListener('keydown',e=>{\n      keys[e.code]=true;\n      if(e.code==='Space'){ e.preventDefault(); tryBigJump(); }\n    });'''
replace='''    const keys={};\n    let mouseLocked=false;\n    const posterPrompt=document.getElementById('posterPrompt');\n    const posterOverlay=document.getElementById('posterOverlay');\n    const posterOverlayImg=document.getElementById('posterOverlayImg');\n    let nearbyPoster=null;\n    let posterOverlayOpen=false;\n\n    function openPoster(poster){\n      if(!poster || P.dead)return;\n      nearbyPoster=poster;\n      posterOverlayOpen=true;\n      posterOverlayImg.src=poster.userData.posterSource;\n      posterOverlay.style.display='flex';\n      posterPrompt.style.display='none';\n      document.exitPointerLock?.();\n      P.vel.x=0; P.vel.z=0;\n    }\n    function closePoster(){\n      if(!posterOverlayOpen)return;\n      posterOverlayOpen=false;\n      posterOverlay.style.display='none';\n      posterOverlayImg.removeAttribute('src');\n      if(matchMedia('(pointer:fine)').matches) setTimeout(()=>renderer.domElement.requestPointerLock?.(),80);\n    }\n    posterOverlay.addEventListener('pointerdown',e=>{e.preventDefault();closePoster();});\n\n    addEventListener('keydown',e=>{\n      if(e.code==='KeyF'){\n        e.preventDefault();\n        if(posterOverlayOpen) closePoster(); else if(nearbyPoster) openPoster(nearbyPoster);\n        return;\n      }\n      if(e.code==='Escape' && posterOverlayOpen){ e.preventDefault(); closePoster(); return; }\n      if(posterOverlayOpen)return;\n      keys[e.code]=true;\n      if(e.code==='Space'){ e.preventDefault(); tryBigJump(); }\n    });'''
if needle not in s: raise SystemExit('input needle missing')
s=s.replace(needle,replace,1)

# Prevent pointer lock while overlay is open.
s=s.replace("if(matchMedia('(pointer:fine)').matches && document.getElementById('startOverlay').style.display==='none')","if(matchMedia('(pointer:fine)').matches && !posterOverlayOpen && document.getElementById('startOverlay').style.display==='none')",1)

# Touch/click directly on a nearby poster.
needle="""    document.addEventListener('pointerlockchange',()=>mouseLocked=document.pointerLockElement===renderer.domElement);\n"""
insert="""    document.addEventListener('pointerlockchange',()=>mouseLocked=document.pointerLockElement===renderer.domElement);\n    renderer.domElement.addEventListener('pointerdown',e=>{\n      if(posterOverlayOpen || !nearbyPoster)return;\n      const r=renderer.domElement.getBoundingClientRect();\n      const ndc=new THREE.Vector2(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);\n      raycaster.setFromCamera(ndc,camera);\n      const hit=raycaster.intersectObjects(posters,false)[0];\n      if(hit && hit.object===nearbyPoster){ e.preventDefault(); openPoster(hit.object); }\n    });\n"""
if needle not in s: raise SystemExit('pointerlock needle missing')
s=s.replace(needle,insert,1)

# Freeze gameplay while reading.
needle='''    function updatePlayer(dt){\n      if(P.dead){'''
replace='''    function updatePlayer(dt){\n      if(posterOverlayOpen){\n        P.vel.x=0; P.vel.z=0;\n        return;\n      }\n      if(P.dead){'''
if needle not in s: raise SystemExit('updatePlayer needle missing')
s=s.replace(needle,replace,1)

# Proximity test: world-space poster center is enough because all posters are large and flat.
needle='''    // ------------------------------------------------------------\n    // CAMERA WITH WALL AVOIDANCE\n    // ------------------------------------------------------------'''
insert='''    function updatePosterInteraction(){\n      if(posterOverlayOpen || P.dead){ posterPrompt.style.display='none'; return; }\n      let best=null, bestD=Infinity;\n      for(const poster of posters){\n        const dx=poster.position.x-P.pos.x;\n        const dy=poster.position.y-(P.pos.y+.65);\n        const dz=poster.position.z-P.pos.z;\n        const d=dx*dx+dy*dy+dz*dz;\n        if(d<bestD){bestD=d;best=poster;}\n      }\n      nearbyPoster=(best && bestD<7.3) ? best : null; // about 2.7 m\n      posterPrompt.style.display=nearbyPoster?'block':'none';\n    }\n\n    // ------------------------------------------------------------\n    // CAMERA WITH WALL AVOIDANCE\n    // ------------------------------------------------------------'''
if needle not in s: raise SystemExit('camera header needle missing')
s=s.replace(needle,insert,1)

# Run interaction update each frame.
needle='''      updateDeathSmoke(dt);\n      updateCamera(dt);\n      renderer.render(scene,camera);'''
replace='''      updateDeathSmoke(dt);\n      updatePosterInteraction();\n      updateCamera(dt);\n      renderer.render(scene,camera);'''
if needle not in s: raise SystemExit('animate needle missing')
s=s.replace(needle,replace,1)

p.write_text(s,encoding='utf-8')
print('patched V1.12 posters')
