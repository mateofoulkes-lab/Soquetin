from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls={
"Prototipo V1.7:":"Prototipo V1.8:",
"Recuperador de password de Soquetin · V1.7":"Recuperador de password de Soquetin · V1.8",
"    <div id=\"respawn\">🔥</div>\n":"",
"      autoHopTimer:0, squash:0, dead:false, respawnTimer:0,\n":"      autoHopTimer:0, squash:0, dead:false, respawnTimer:0, deathSinkVy:0, deathSmokeTimer:0,\n"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing token: {a}')
    s=s.replace(a,b,1)

# Record the adjusted GLB material state so the lava burn can animate and restore cleanly.
needle="""            if('roughness' in m && Number.isFinite(m.roughness)) m.roughness=Math.min(1,m.roughness+.05);\n            m.needsUpdate=true;\n            return m;\n"""
replace="""            if('roughness' in m && Number.isFinite(m.roughness)) m.roughness=Math.min(1,m.roughness+.05);\n            if(m.color) m.userData.soquetinBaseColor=m.color.clone();\n            if(m.emissive){\n              m.userData.soquetinBaseEmissive=m.emissive.clone();\n              m.userData.soquetinBaseEmissiveIntensity=m.emissiveIntensity ?? 0;\n            }\n            m.needsUpdate=true;\n            return m;\n"""
if needle not in s: raise SystemExit('material needle missing')
s=s.replace(needle,replace,1)

# Insert smoke/burn helpers before die().
needle2="""    function die(){\n      if(P.dead)return;\n      P.dead=true; P.respawnTimer=.5; P.vel.set(0,0,0); lavaSound();\n      const el=document.getElementById('respawn'); el.style.opacity='1';\n    }\n    function respawn(){\n      P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.bigJumpUsed=false; P.squash=.4;\n      document.getElementById('respawn').style.opacity='0';\n    }\n"""
replace2="""    // Lava death FX: the character sinks, chars dark and releases a little black smoke.\n    const smokeParticles=[];\n    const smokeGeo=new THREE.SphereGeometry(.075,7,5);\n    function setSoquetinBurn(amount){\n      const t=THREE.MathUtils.clamp(amount,0,1);\n      const dark=new THREE.Color(0x171717);\n      visualRoot.traverse(obj=>{\n        if(!obj.isMesh || !obj.material) return;\n        const mats=Array.isArray(obj.material)?obj.material:[obj.material];\n        for(const m of mats){\n          if(!m) continue;\n          if(m.color && m.userData.soquetinBaseColor){\n            m.color.copy(m.userData.soquetinBaseColor).lerp(dark,t*.92);\n          }\n          if(m.emissive && m.userData.soquetinBaseEmissive){\n            m.emissive.copy(m.userData.soquetinBaseEmissive).lerp(dark,t);\n            m.emissiveIntensity=(m.userData.soquetinBaseEmissiveIntensity??0)*(1-t);\n          }\n        }\n      });\n    }\n    function spawnDeathSmoke(){\n      const mat=new THREE.MeshBasicMaterial({color:0x111111,transparent:true,opacity:.42,depthWrite:false});\n      const puff=new THREE.Mesh(smokeGeo,mat);\n      puff.position.set(\n        P.pos.x+(Math.random()-.5)*.28,\n        P.pos.y+.48+Math.random()*.38,\n        P.pos.z+(Math.random()-.5)*.28\n      );\n      const k=.65+Math.random()*.75;\n      puff.scale.setScalar(k);\n      scene.add(puff);\n      smokeParticles.push({mesh:puff,age:0,life:.65+Math.random()*.45,vx:(Math.random()-.5)*.10,vz:(Math.random()-.5)*.10,vy:.22+Math.random()*.16});\n    }\n    function updateDeathSmoke(dt){\n      for(let i=smokeParticles.length-1;i>=0;i--){\n        const p=smokeParticles[i];\n        p.age+=dt;\n        p.mesh.position.x+=p.vx*dt;\n        p.mesh.position.y+=p.vy*dt;\n        p.mesh.position.z+=p.vz*dt;\n        const q=p.age/p.life;\n        p.mesh.material.opacity=.42*(1-q);\n        p.mesh.scale.multiplyScalar(1+dt*.8);\n        if(q>=1){\n          scene.remove(p.mesh);\n          p.mesh.material.dispose();\n          smokeParticles.splice(i,1);\n        }\n      }\n    }\n    function clearDeathSmoke(){\n      for(const p of smokeParticles){ scene.remove(p.mesh); p.mesh.material.dispose(); }\n      smokeParticles.length=0;\n    }\n\n    function die(){\n      if(P.dead)return;\n      P.dead=true;\n      P.respawnTimer=1.5;\n      P.deathSinkVy=Math.min(-.12,P.vel.y*.5);\n      P.deathSmokeTimer=0;\n      P.vel.x=0; P.vel.z=0; P.vel.y=0;\n      P.grounded=false;\n      lavaSound();\n    }\n    function respawn(){\n      P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.bigJumpUsed=false; P.squash=.4;\n      P.deathSinkVy=0; P.deathSmokeTimer=0;\n      setSoquetinBurn(0);\n      clearDeathSmoke();\n    }\n"""
if needle2 not in s: raise SystemExit('death block missing')
s=s.replace(needle2,replace2,1)

# Replace dead-state update with 1.5s physical sink/burn/smoke animation.
needle3="""      if(P.dead){\n        P.respawnTimer-=dt; if(P.respawnTimer<=0)respawn();\n        return;\n      }\n"""
replace3="""      if(P.dead){\n        P.respawnTimer-=dt;\n        const deathProgress=1-THREE.MathUtils.clamp(P.respawnTimer/1.5,0,1);\n        P.pos.y+=P.deathSinkVy*dt;\n        setSoquetinBurn(THREE.MathUtils.smoothstep(deathProgress,0,.72));\n        P.deathSmokeTimer-=dt;\n        if(P.deathSmokeTimer<=0 && deathProgress>.08){\n          spawnDeathSmoke();\n          P.deathSmokeTimer=.13+Math.random()*.08;\n        }\n        playerRoot.position.copy(P.pos);\n        playerRoot.rotation.y=P.yaw;\n        updateCharacterShadowLight();\n        if(P.respawnTimer<=0)respawn();\n        return;\n      }\n"""
if needle3 not in s: raise SystemExit('dead update block missing')
s=s.replace(needle3,replace3,1)

# Smoke must continue fading even after the death state update returns.
needle4="""      updateBreakTiles(dt);\n      updateLava(dt);\n      updateCamera(dt);\n"""
replace4="""      updateBreakTiles(dt);\n      updateLava(dt);\n      updateDeathSmoke(dt);\n      updateCamera(dt);\n"""
if needle4 not in s: raise SystemExit('animate block missing')
s=s.replace(needle4,replace4,1)

p.write_text(s,encoding='utf-8')
print('patched V1.8 lava death')
