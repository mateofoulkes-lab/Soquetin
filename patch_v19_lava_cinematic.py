from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls={
"Prototipo V1.8:":"Prototipo V1.9:",
"Recuperador de password de Soquetin · V1.8":"Recuperador de password de Soquetin · V1.9",
"new THREE.PlaneGeometry(21.0,Math.abs(Z_PIT_NORTH-Z_PIT_SOUTH)+.6,1,1)":"new THREE.PlaneGeometry(126.0,(Math.abs(Z_PIT_NORTH-Z_PIT_SOUTH)+.6)*6,1,1)",
"    const smokeGeo=new THREE.SphereGeometry(.075,7,5);":"    const smokeGeo=new THREE.SphereGeometry(.12,8,6);",
"      const mat=new THREE.MeshBasicMaterial({color:0x111111,transparent:true,opacity:.42,depthWrite:false});":"      const mat=new THREE.MeshBasicMaterial({color:0x0b0b0b,transparent:true,opacity:.68,depthWrite:false});",
"        P.pos.x+(Math.random()-.5)*.28,":"        P.pos.x+(Math.random()-.5)*.42,",
"        P.pos.y+.48+Math.random()*.38,":"        P.pos.y+.35+Math.random()*.55,",
"        P.pos.z+(Math.random()-.5)*.28":"        P.pos.z+(Math.random()-.5)*.42",
"      const k=.65+Math.random()*.75;":"      const k=.85+Math.random()*1.15;",
"      smokeParticles.push({mesh:puff,age:0,life:.65+Math.random()*.45,vx:(Math.random()-.5)*.10,vz:(Math.random()-.5)*.10,vy:.22+Math.random()*.16});":"      smokeParticles.push({mesh:puff,age:0,life:1.0+Math.random()*.65,vx:(Math.random()-.5)*.16,vz:(Math.random()-.5)*.16,vy:.34+Math.random()*.24});",
"        p.mesh.material.opacity=.42*(1-q);":"        p.mesh.material.opacity=.68*(1-q);",
"        p.mesh.scale.multiplyScalar(1+dt*.8);":"        p.mesh.scale.multiplyScalar(1+dt*1.15);",
"      P.deathSinkVy=Math.min(-.12,P.vel.y*.5);":"      // Fixed slow sink: over 1.5 s the model descends about one full visual height.\n      P.deathSinkVy=-(CHARACTER_VISUAL_HEIGHT/1.5)*.98;",
"          P.deathSmokeTimer=.13+Math.random()*.08;":"          P.deathSmokeTimer=.045+Math.random()*.035;"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing token: {a}')
    s=s.replace(a,b,1)

# Freeze camera at the exact instant of lava contact.
needle="""    function die(){\n      if(P.dead)return;\n      P.dead=true;\n      P.respawnTimer=1.5;\n"""
replace="""    const deathCameraPos=new THREE.Vector3();\n    const deathCameraQuat=new THREE.Quaternion();\n\n    function die(){\n      if(P.dead)return;\n      deathCameraPos.copy(camera.position);\n      deathCameraQuat.copy(camera.quaternion);\n      P.dead=true;\n      P.respawnTimer=1.5;\n"""
if needle not in s: raise SystemExit('die needle missing')
s=s.replace(needle,replace,1)

needle2="""    function updateCamera(dt){\n      const target=tmpV.set(P.pos.x,P.pos.y+1.05,P.pos.z);\n"""
replace2="""    function updateCamera(dt){\n      if(P.dead){\n        camera.position.copy(deathCameraPos);\n        camera.quaternion.copy(deathCameraQuat);\n        return;\n      }\n      const target=tmpV.set(P.pos.x,P.pos.y+1.05,P.pos.z);\n"""
if needle2 not in s: raise SystemExit('camera needle missing')
s=s.replace(needle2,replace2,1)

p.write_text(s,encoding='utf-8')
print('patched V1.9 lava cinematic')
