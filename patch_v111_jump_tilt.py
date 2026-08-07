from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls={
"Prototipo V1.10:":"Prototipo V1.11:",
"Recuperador de password de Soquetin · V1.10":"Recuperador de password de Soquetin · V1.11",
"    const visualRoot=new THREE.Group(); playerRoot.add(visualRoot);\n\n\n    // Simple fallback while the GLB loads (or if it ever fails).\n":"    const visualRoot=new THREE.Group(); playerRoot.add(visualRoot);\n    // Separate tilt pivot so squash/stretch remains independent from rocking.\n    const tiltRoot=new THREE.Group(); visualRoot.add(tiltRoot);\n\n    // Simple fallback while the GLB loads (or if it ever fails).\n",
"    body.castShadow=true; body.receiveShadow=true; body.position.y=.56; visualRoot.add(body);":"    body.castShadow=true; body.receiveShadow=true; body.position.y=.56; tiltRoot.add(body);",
"      visualRoot.remove(body);\n      visualRoot.add(model);":"      tiltRoot.remove(body);\n      tiltRoot.add(model);",
"      autoHopTimer:0, squash:0, dead:false, respawnTimer:0, deathSinkVy:0, deathSmokeTimer:0,\n      spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false":"      autoHopTimer:0, squash:0, dead:false, respawnTimer:0, deathSinkVy:0, deathSmokeTimer:0,\n      animPhase:'idle', animTime:0, animLaunchVy:2.35, tiltDeg:0, tiltPivotY:0, animStartTilt:0, animStartPivot:0,\n      spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false",
"      P.grounded=false; P.bigJumpUsed=true; P.squash=1;":"      P.grounded=false; P.bigJumpUsed=true; P.squash=1;\n      beginJumpTilt(4.03);",
"          P.grounded=false; P.autoHopTimer=0; P.squash=.52;":"          P.grounded=false; P.autoHopTimer=0; P.squash=.52;\n          beginJumpTilt(2.35);",
"        if(!P.grounded && P.vel.y<-1.2) P.squash=.38;\n        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;":"        if(!P.grounded && P.vel.y<-1.2){\n          P.squash=.38;\n          beginLandingTilt();\n        }\n        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;",
"      visualRoot.scale.set(sxz,sy,sxz);\n      playerRoot.position.copy(P.pos); playerRoot.rotation.y=P.yaw;":"      visualRoot.scale.set(sxz,sy,sxz);\n      updateJumpTilt(dt);\n      playerRoot.position.copy(P.pos); playerRoot.rotation.y=P.yaw;",
"      P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.bigJumpUsed=false; P.squash=.4;\n      P.deathSinkVy=0; P.deathSmokeTimer=0;":"      P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.bigJumpUsed=false; P.squash=.4;\n      P.deathSinkVy=0; P.deathSmokeTimer=0;\n      P.animPhase='idle'; P.animTime=0; P.tiltDeg=0; P.tiltPivotY=0;\n      applyCharacterTilt(0,0);"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing token: {a}')
    s=s.replace(a,b,1)

needle="""    function tryBigJump(){\n"""
insert="""    // ------------------------------------------------------------\n    // WHOLE-BODY JUMP ROCKING\n    // Forward lean = -10 deg around the feet. On descent, the pivot travels\n    // to the head while the body passes through neutral, then the feet swing\n    // forward to +20 deg around the head. Collider/physics remain untouched.\n    function applyCharacterTilt(deg,pivotY){\n      P.tiltDeg=deg; P.tiltPivotY=pivotY;\n      const a=THREE.MathUtils.degToRad(deg);\n      tiltRoot.rotation.x=a;\n      // Rotate around local pivot p=(0,pivotY,0): translation is p - R*p.\n      tiltRoot.position.set(0,pivotY*(1-Math.cos(a)),-pivotY*Math.sin(a));\n    }\n    function beginJumpTilt(launchVy){\n      P.animPhase='takeoff';\n      P.animTime=0;\n      P.animLaunchVy=Math.max(.1,launchVy);\n      P.animStartTilt=P.tiltDeg;\n      P.animStartPivot=P.tiltPivotY;\n    }\n    function beginLandingTilt(){\n      P.animPhase='land';\n      P.animTime=0;\n      P.animStartTilt=P.tiltDeg;\n      P.animStartPivot=P.tiltPivotY;\n    }\n    function updateJumpTilt(dt){\n      if(P.dead) return;\n      const H=CHARACTER_VISUAL_HEIGHT;\n      if(P.animPhase==='takeoff'){\n        P.animTime+=dt;\n        const t=THREE.MathUtils.smoothstep(THREE.MathUtils.clamp(P.animTime/.12,0,1),0,1);\n        applyCharacterTilt(THREE.MathUtils.lerp(P.animStartTilt,-10,t),THREE.MathUtils.lerp(P.animStartPivot,0,t));\n        if(P.animTime>=.12) P.animPhase='rise';\n      } else if(P.animPhase==='rise'){\n        applyCharacterTilt(-10,0);\n        if(P.vel.y<=0){ P.animPhase='fall'; P.animTime=0; }\n      } else if(P.animPhase==='fall'){\n        const f=THREE.MathUtils.clamp((-P.vel.y)/P.animLaunchVy,0,1);\n        if(f<.34){\n          const u=THREE.MathUtils.smoothstep(f/.34,0,1);\n          applyCharacterTilt(THREE.MathUtils.lerp(-10,0,u),H*u);\n        } else {\n          const u=THREE.MathUtils.smoothstep((f-.34)/.66,0,1);\n          applyCharacterTilt(THREE.MathUtils.lerp(0,20,u),H);\n        }\n      } else if(P.animPhase==='land'){\n        P.animTime+=dt;\n        const t=THREE.MathUtils.smoothstep(THREE.MathUtils.clamp(P.animTime/.12,0,1),0,1);\n        applyCharacterTilt(THREE.MathUtils.lerp(P.animStartTilt,-10,t),THREE.MathUtils.lerp(P.animStartPivot,0,t));\n        if(P.animTime>=.12){ P.animPhase='settle'; P.animTime=0; }\n      } else if(P.animPhase==='settle'){\n        P.animTime+=dt;\n        const t=THREE.MathUtils.smoothstep(THREE.MathUtils.clamp(P.animTime/.16,0,1),0,1);\n        applyCharacterTilt(THREE.MathUtils.lerp(-10,0,t),0);\n        if(P.animTime>=.16){ P.animPhase='idle'; applyCharacterTilt(0,0); }\n      } else if(P.grounded){\n        applyCharacterTilt(0,0);\n      }\n    }\n\n    function tryBigJump(){\n"""
if needle not in s:
    raise SystemExit('tryBigJump needle missing')
s=s.replace(needle,insert,1)

p.write_text(s,encoding='utf-8')
print('patched V1.11 jump tilt')
