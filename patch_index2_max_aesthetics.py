from pathlib import Path
import re

p=Path('index2.html')
s=p.read_text(encoding='utf-8')

# ------------------------------------------------------------------
# 1) Lava: one stretched, aspect-aware procedural texture (no tiled repeat).
# ------------------------------------------------------------------
pat=re.compile(r"    const texLava=canvasTexture\(512,\(g,z\)=>\{.*?\n    \},2\.4,4\.2\);",re.S)
new=r'''    const lavaCanvas=document.createElement('canvas');
    lavaCanvas.width=1024; lavaCanvas.height=512;
    const lavaCtx=lavaCanvas.getContext('2d');
    {
      const w=lavaCanvas.width,h=lavaCanvas.height;
      const grad=lavaCtx.createLinearGradient(0,0,w,h);
      grad.addColorStop(0,'#6c0b00'); grad.addColorStop(.32,'#c92d04'); grad.addColorStop(.67,'#ff650b'); grad.addColorStop(1,'#ffb11b');
      lavaCtx.fillStyle=grad; lavaCtx.fillRect(0,0,w,h);
      // Long, non-periodic veins drawn across the whole atlas so the plane reads as one surface.
      for(let band=0;band<34;band++){
        const baseY=(band+.35+Math.random()*.3)*(h/34);
        lavaCtx.beginPath();
        for(let x=0;x<=w;x+=12){
          const y=baseY+Math.sin(x*.011+band*.71)*9+Math.sin(x*.027+band*1.9)*3+(Math.random()-.5)*1.4;
          if(x===0) lavaCtx.moveTo(x,y); else lavaCtx.lineTo(x,y);
        }
        lavaCtx.strokeStyle=`rgba(255,${95+Math.random()*105|0},5,${.12+Math.random()*.16})`;
        lavaCtx.lineWidth=2+Math.random()*8; lavaCtx.stroke();
      }
      for(let i=0;i<260;i++){
        const x=Math.random()*w,y=Math.random()*h,r=1+Math.random()*7;
        lavaCtx.fillStyle=`rgba(255,${70+Math.random()*120|0},0,${.05+Math.random()*.12})`;
        lavaCtx.beginPath(); lavaCtx.arc(x,y,r,0,Math.PI*2); lavaCtx.fill();
      }
    }
    const texLava=new THREE.CanvasTexture(lavaCanvas);
    texLava.colorSpace=THREE.SRGBColorSpace;
    texLava.wrapS=texLava.wrapT=THREE.ClampToEdgeWrapping;
    texLava.minFilter=THREE.LinearMipmapLinearFilter;
    texLava.magFilter=THREE.LinearFilter;
    texLava.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());'''
if not pat.search(s): raise SystemExit('lava texture block not found')
s=pat.sub(new,s,count=1)
s=s.replace("      texLava.offset.x=(lavaTime*.018)%1; texLava.offset.y=(lavaTime*.011)%1;\n",'',1)

# ------------------------------------------------------------------
# 2) Real coyote time + one-shot jump buffer (no key-repeat autojump).
# Preserve intentional big-jump interruption of automatic hops.
# ------------------------------------------------------------------
s=s.replace("spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false, jumpBuffer:0, coyoteTime:.11, idleTime:0",
            "spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false, jumpBuffer:0, coyoteTime:.11, idleTime:0, autoHopAir:false",1)

old="""    function tryBigJump(){
      // El salto grande puede interrumpir inmediatamente un saltito automatico.
      // Solo se permite uno hasta volver a tocar una superficie.
      if(P.dead || P.bigJumpUsed) return;
      const dir=inputVector();"""
new="""    function tryBigJump(){
      // Big jump is legal from real ground, during the short coyote window,
      // or while interrupting an intentional automatic hop. It is NOT a free air-jump.
      if(P.dead || P.bigJumpUsed) return false;
      const eligible=P.grounded || P.coyoteTime>0 || P.autoHopAir;
      if(!eligible) return false;
      const dir=inputVector();"""
if old not in s: raise SystemExit('tryBigJump header not found')
s=s.replace(old,new,1)
s=s.replace("      P.grounded=false; P.bigJumpUsed=true; P.squash=1;",
            "      P.grounded=false; P.bigJumpUsed=true; P.autoHopAir=false; P.coyoteTime=0; P.squash=1;",1)
s=s.replace("      playSfx('jump',.82);\n    }","      playSfx('jump',.82);\n      return true;\n    }",1)

# Keyboard repeat must not continually refresh the jump buffer.
s=s.replace("if(e.code==='Space'){ e.preventDefault(); P.jumpBuffer=.12; tryBigJump(); }",
            "if(e.code==='Space'){ e.preventDefault(); if(e.repeat)return; P.jumpBuffer=.12; if(tryBigJump())P.jumpBuffer=0; }",1)
s=s.replace("document.getElementById('jumpBtn').addEventListener('pointerdown',e=>{e.preventDefault();if(posterOverlayOpen) closePoster();P.jumpBuffer=.12;tryBigJump();});",
            "document.getElementById('jumpBtn').addEventListener('pointerdown',e=>{e.preventDefault();if(posterOverlayOpen) closePoster();P.jumpBuffer=.12;if(tryBigJump())P.jumpBuffer=0;});",1)

# Automatic hop is a special interruptible air state.
s=s.replace("          P.grounded=false; P.autoHopTimer=0; P.squash=.52;",
            "          P.grounded=false; P.autoHopAir=true; P.coyoteTime=0; P.autoHopTimer=0; P.squash=.52;",1)
# Landing on a real support ends auto-hop state, resets coyote, then consumes buffered press.
s=s.replace("        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;\n        P.coyoteTime=.11;\n        P.bigJumpUsed=false;\n        if(P.jumpBuffer>0){ P.jumpBuffer=0; tryBigJump(); }",
            "        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true; P.autoHopAir=false;\n        P.coyoteTime=.11;\n        P.bigJumpUsed=false;\n        if(P.jumpBuffer>0){ P.jumpBuffer=0; tryBigJump(); }",1)
# If previous patch layout differs, handle original landing line variant.
s=s.replace("        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;\n        P.coyoteTime=.11;\n        if(P.jumpBuffer>0 && !P.bigJumpUsed){ P.jumpBuffer=0; tryBigJump(); }",
            "        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true; P.autoHopAir=false;\n        P.coyoteTime=.11;\n        P.bigJumpUsed=false;\n        if(P.jumpBuffer>0){ P.jumpBuffer=0; tryBigJump(); }",1)
# Respawn state.
s=s.replace("P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.bigJumpUsed=false; P.squash=.4;",
            "P.dead=false; P.pos.copy(P.spawn); P.vel.set(0,0,0); P.grounded=true; P.autoHopTimer=0; P.bigJumpUsed=false; P.autoHopAir=false; P.coyoteTime=.11; P.jumpBuffer=0; P.squash=.4;",1)

# ------------------------------------------------------------------
# 3) Pure aesthetic madness: torches, webs, cracks, rocks, lava smoke.
# Insert after dungeon lights are created and before UV application.
# ------------------------------------------------------------------
anchor="""    // Apply exported UV/repeat settings after all dungeon geometry is built.
    applyHardcodedTextureOverrides();"""
aesthetic=r'''    // ------------------------------------------------------------
    // MAX AESTHETICS TEST — decorative only, no gameplay collision/support.
    // ------------------------------------------------------------
    const aestheticTorches=[];
    const flameGeo=new THREE.ConeGeometry(.075,.26,9);
    const flameMat=new THREE.MeshBasicMaterial({color:0xffb326,transparent:true,opacity:.92,toneMapped:false});
    const torchWoodMat=new THREE.MeshStandardMaterial({color:0x402614,roughness:.95});
    function addTorch(x,y,z,rotY=0){
      const root=new THREE.Group(); root.position.set(x,y,z); root.rotation.y=rotY; scene.add(root);
      const stick=new THREE.Mesh(new THREE.CylinderGeometry(.025,.035,.42,8),torchWoodMat); stick.rotation.x=Math.PI/2; stick.position.z=.12; root.add(stick);
      const flame=new THREE.Mesh(flameGeo,flameMat.clone()); flame.position.set(0,.18,.29); root.add(flame);
      const light=new THREE.PointLight(0xff7b24,3.8,4.8,2); light.position.set(0,.18,.20); light.castShadow=false; root.add(light);
      aestheticTorches.push({root,flame,light,phase:Math.random()*6.28,base:3.8});
    }
    // Torches along the main path and challenge entrances.
    addTorch(-10.28,2.0,9, Math.PI/2); addTorch(10.28,2.0,9,-Math.PI/2);
    addTorch(-10.28,2.0,-4.2,Math.PI/2); addTorch(10.28,2.0,-4.2,-Math.PI/2);
    addTorch(-10.28,2.0,-15.0,Math.PI/2); addTorch(10.28,2.0,-15.0,-Math.PI/2);
    addTorch(FINAL_LEFT+.17,2.0,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,Math.PI/2);
    addTorch(FINAL_RIGHT-.17,2.0,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,-Math.PI/2);

    // Cobwebs: lightweight procedural line fans in ceiling corners.
    const webMat=new THREE.LineBasicMaterial({color:0xb9b7ae,transparent:true,opacity:.19,depthWrite:false});
    function addWeb(x,y,z,sx=1,sy=1,rotY=0){
      const verts=[];
      const seg=(ax,ay,az,bx,by,bz)=>verts.push(ax,ay,az,bx,by,bz);
      for(let i=0;i<=5;i++){
        const t=i/5; seg(0,0,0,sx*t,-sy*(1-t),0);
      }
      for(let ring=1;ring<=4;ring++){
        const rr=ring/4;
        let prev=null;
        for(let i=0;i<=8;i++){
          const t=i/8, px=sx*t*rr, py=-sy*(1-t)*rr;
          if(prev) seg(prev[0],prev[1],0,px,py,0); prev=[px,py];
        }
      }
      const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
      const l=new THREE.LineSegments(g,webMat); l.position.set(x,y,z); l.rotation.y=rotY; scene.add(l);
    }
    addWeb(-10.32,4.72,11.2,.85,.72,0); addWeb(9.98,4.70,12.72,.85,.75,Math.PI/2);
    addWeb(-10.30,4.72,-8.1,.9,.8,0); addWeb(9.98,4.7,-12.9,.8,.72,Math.PI/2);
    addWeb(FINAL_LEFT+.18,4.68,Z_FINAL_NORTH+.35,.75,.68,0);

    // Cracks as tiny dark line decals slightly in front of selected walls.
    const crackMat=new THREE.LineBasicMaterial({color:0x181510,transparent:true,opacity:.55,depthWrite:false});
    function addCrack(x,y,z,scale=1,rotY=0){
      const pts=[0,0,0,.08,.12,0, .08,.12,0,-.03,.24,0, -.03,.24,0,.07,.37,0, .02,.18,0,.18,.21,0, .08,.12,0,.20,.08,0];
      const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pts.map(v=>v*scale),3));
      const l=new THREE.LineSegments(g,crackMat); l.position.set(x,y,z); l.rotation.y=rotY; l.renderOrder=2; scene.add(l);
    }
    addCrack(-4.8,1.4,12.83,1.8,0); addCrack(6.4,2.0,12.83,1.5,0);
    addCrack(-10.32,1.5,-2.0,1.4,Math.PI/2); addCrack(10.32,2.4,-10.0,1.8,-Math.PI/2);
    addCrack(FINAL_RIGHT-.18,1.35,Z_FINAL_NORTH+2.2,1.7,-Math.PI/2);

    // Loose floor stones. Individual low-poly meshes intentionally add some draw calls for the perf experiment.
    const rockGeo=new THREE.DodecahedronGeometry(.11,0);
    const rockMats=[0x4e473c,0x5a5144,0x403a32].map(c=>new THREE.MeshStandardMaterial({color:c,roughness:1}));
    const rockAreas=[[-9.4,9.6,18,5.0],[-9.5,-15.8,19,3.2],[-3.0,-20.2,6.0,4.6]];
    for(const [cx,cz,w,d] of rockAreas){
      for(let i=0;i<14;i++){
        const r=new THREE.Mesh(rockGeo,rockMats[i%rockMats.length]);
        r.position.set(cx+(Math.random()-.5)*w,.04,cz+(Math.random()-.5)*d);
        const k=.35+Math.random()*.95; r.scale.set(k,.35+Math.random()*.45,k*(.7+Math.random()*.5));
        r.rotation.set(Math.random()*1.2,Math.random()*6.28,Math.random()*.8); r.castShadow=true; r.receiveShadow=true; scene.add(r);
      }
    }

    // Persistent smoky haze above lava, separate from death smoke.
    const lavaSmoke=[];
    const lavaSmokeGeo=new THREE.SphereGeometry(.12,7,5);
    const lavaSmokeBaseMat=new THREE.MeshBasicMaterial({color:0x241b17,transparent:true,opacity:.10,depthWrite:false,toneMapped:false});
    let lavaSmokeTimer=0;
    function spawnLavaSmoke(){
      const m=new THREE.Mesh(lavaSmokeGeo,lavaSmokeBaseMat.clone());
      m.position.set((Math.random()-.5)*20,-9.72,Z_PIT_NORTH+Math.random()*(Z_PIT_SOUTH-Z_PIT_NORTH));
      const k=.8+Math.random()*2.0; m.scale.setScalar(k); scene.add(m);
      lavaSmoke.push({m,age:0,life:1.6+Math.random()*2.1,vx:(Math.random()-.5)*.13,vy:.16+Math.random()*.15,vz:(Math.random()-.5)*.13});
    }
    function updateMaxAesthetics(dt){
      const t=lavaTime;
      for(const q of aestheticTorches){
        const wobble=Math.sin(t*8.1+q.phase)*.12+Math.sin(t*13.7+q.phase*.7)*.06;
        q.light.intensity=q.base*(1+wobble);
        q.flame.scale.set(1+wobble*.5,1+wobble*.25,1+wobble*.5);
        q.flame.rotation.z=Math.sin(t*6.2+q.phase)*.08;
      }
      lavaSmokeTimer-=dt;
      if(lavaSmokeTimer<=0 && lavaSmoke.length<34){spawnLavaSmoke();lavaSmokeTimer=.07+Math.random()*.12;}
      for(let i=lavaSmoke.length-1;i>=0;i--){
        const q=lavaSmoke[i]; q.age+=dt; q.m.position.x+=q.vx*dt; q.m.position.y+=q.vy*dt; q.m.position.z+=q.vz*dt;
        const u=q.age/q.life; q.m.material.opacity=.10*Math.sin(Math.PI*Math.min(1,u)); q.m.scale.multiplyScalar(1+dt*.18);
        if(u>=1){scene.remove(q.m);q.m.material.dispose();lavaSmoke.splice(i,1);}
      }
    }

    // Apply exported UV/repeat settings after all dungeon geometry is built.
    applyHardcodedTextureOverrides();'''
if anchor not in s: raise SystemExit('UV application anchor not found')
s=s.replace(anchor,aesthetic,1)

# Call aesthetic update in render loop.
s=s.replace("      updateLava(dt);\n      updateDeathSmoke(dt);","      updateLava(dt);\n      updateMaxAesthetics(dt);\n      updateDeathSmoke(dt);",1)

# Make perf meter explicitly identify the heavier build.
s=s.replace("ENHANCED · ${fps} FPS", "MAX · ${fps} FPS",1)
s=s.replace("ENHANCED · -- FPS", "MAX · -- FPS",1)

p.write_text(s,encoding='utf-8')
print('index2 max aesthetics + seamless lava + real coyote/buffer patched')
