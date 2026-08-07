from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('Prototipo V1.17:','Prototipo V1.18:',1)
s=s.replace('Recuperador de password de Soquetin · V1.17','Recuperador de password de Soquetin · V1.18',1)

s=s.replace("#mobileControls { display:none; position:absolute; inset:0; pointer-events:none; }\n    .stickZone { position:absolute; bottom:16px; width:44vw; height:42vh; pointer-events:auto; touch-action:none; }",
            "#mobileControls { display:none; position:fixed; inset:0; pointer-events:none; z-index:6; }\n    body.poster-open #mobileControls { z-index:80; }\n    .stickZone { position:absolute; bottom:30px; width:44vw; height:42vh; pointer-events:auto; touch-action:none; }",1)

s=s.replace("      posterOverlay.style.display='flex';\n      posterPrompt.style.display='none';",
            "      posterOverlay.style.display='flex';\n      document.body.classList.add('poster-open');\n      posterPrompt.style.display='none';",1)

s=s.replace("      posterOverlay.style.display='none';\n      posterOverlayImg.removeAttribute('src');",
            "      posterOverlay.style.display='none';\n      document.body.classList.remove('poster-open');\n      posterOverlayImg.removeAttribute('src');",1)

old_front="""    // Screen-space poster hit testing: robust on mobile and independent from 3D raycasts.\n    function pointerInsidePoster(poster,clientX,clientY){\n"""
new_front="""    // Only the geometric front (+Z in the poster's local space) can be enlarged.\n    const posterFrontNormal=new THREE.Vector3();\n    const posterToCamera=new THREE.Vector3();\n    const posterWorldPos=new THREE.Vector3();\n    const posterNormalMatrix=new THREE.Matrix3();\n    function isPosterFrontFacing(poster){\n      poster.updateWorldMatrix(true,false);\n      poster.getWorldPosition(posterWorldPos);\n      posterNormalMatrix.getNormalMatrix(poster.matrixWorld);\n      posterFrontNormal.set(0,0,1).applyMatrix3(posterNormalMatrix).normalize();\n      posterToCamera.copy(camera.position).sub(posterWorldPos).normalize();\n      return posterFrontNormal.dot(posterToCamera)>0.02;\n    }\n\n    // Screen-space poster hit testing: robust on mobile and independent from 3D raycasts.\n    function pointerInsidePoster(poster,clientX,clientY){\n"""
if old_front not in s: raise SystemExit('front insertion anchor not found')
s=s.replace(old_front,new_front,1)

s=s.replace("        if(d<=20.25 && d<bestD && pointerInsidePoster(poster,e.clientX,e.clientY)){",
            "        if(d<=20.25 && d<bestD && isPosterFrontFacing(poster) && pointerInsidePoster(poster,e.clientX,e.clientY)){",1)

old_mobile="""    const mobile={moveX:0,moveY:0,lookX:0,lookY:0};\n    function setupStick(zoneId,baseId,mode){\n"""
new_mobile="""    const mobileControlsEl=document.getElementById('mobileControls');\n    // Move mobile controls out of #hud so they can sit above an enlarged poster without lifting the whole HUD.\n    document.body.appendChild(mobileControlsEl);\n    const mobile={moveX:0,moveY:0,lookX:0,lookY:0};\n    function setupStick(zoneId,baseId,mode){\n"""
if old_mobile not in s: raise SystemExit('mobile anchor not found')
s=s.replace(old_mobile,new_mobile,1)

old_pd="""      zone.addEventListener('pointerdown',e=>{\n        if(pointer!==null) return; pointer=e.pointerId; zone.setPointerCapture(pointer);\n        sx=e.clientX; sy=e.clientY; base.style.left=sx+'px'; base.style.top=sy+'px'; base.style.display='block';\n      });\n"""
new_pd="""      zone.addEventListener('pointerdown',e=>{\n        if(posterOverlayOpen) closePoster();\n        if(pointer!==null) return; pointer=e.pointerId; zone.setPointerCapture(pointer);\n        sx=e.clientX; sy=e.clientY;\n        const zr=zone.getBoundingClientRect();\n        // Base lives inside the zone: convert viewport coordinates to zone-local coordinates.\n        // This fixes the old double-offset that could push the joystick below the screen.\n        const localX=THREE.MathUtils.clamp(e.clientX-zr.left,66,zr.width-66);\n        const localY=THREE.MathUtils.clamp(e.clientY-zr.top,66,zr.height-66);\n        base.style.left=localX+'px'; base.style.top=localY+'px'; base.style.display='block';\n      });\n"""
if old_pd not in s: raise SystemExit('stick pointerdown not found')
s=s.replace(old_pd,new_pd,1)

s=s.replace("    document.getElementById('jumpBtn').addEventListener('pointerdown',e=>{e.preventDefault();tryBigJump();});",
            "    document.getElementById('jumpBtn').addEventListener('pointerdown',e=>{e.preventDefault();if(posterOverlayOpen) closePoster();tryBigJump();});",1)

# Right look zone is also a control; touching it should close an enlarged poster via setupStick above.

p.write_text(s,encoding='utf-8')
print('patched V1.18')
