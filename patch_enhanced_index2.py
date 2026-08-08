from pathlib import Path
import re

src=Path('index.html').read_text(encoding='utf-8')
s=src

# Branding / test HUD styles.
s=s.replace('<title>El Enigma de Soquetin</title>','<title>El Enigma de Soquetin — Enhanced</title>',1)
s=s.replace('</style>',r'''
    #fxFlash{position:fixed;inset:0;z-index:115;pointer-events:none;opacity:0;background:rgba(75,0,0,.55)}
    #fxFlash.hit{animation:fxHit .22s ease-out}
    #fxFlash.respawn{animation:fxRespawn .30s ease-out}
    @keyframes fxHit{0%{opacity:.48}100%{opacity:0}}
    @keyframes fxRespawn{0%{opacity:.65;background:#060403}45%{opacity:.3;background:rgba(90,16,5,.45)}100%{opacity:0}}
    #perfMeter{position:fixed;left:10px;bottom:10px;z-index:55;padding:7px 9px;border-radius:8px;background:rgba(0,0,0,.44);border:1px solid rgba(255,255,255,.12);font:600 10px ui-monospace,monospace;color:#ded7c6;pointer-events:none;backdrop-filter:blur(5px)}
    #finalScreen{position:fixed;inset:0;z-index:100;display:none;place-items:center;background:rgba(4,3,2,.94);text-align:center;padding:28px}
    #finalScreen.show{display:grid;animation:finalIn .55s ease both}
    #finalScreen h1{font-size:clamp(42px,9vw,84px);margin:0 0 8px;letter-spacing:.08em}
    #finalScreen p{opacity:.7;margin:0 0 24px}
    #finalScreen button{border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.09);color:#fff;border-radius:12px;padding:12px 18px;font-weight:800;cursor:pointer}
    @keyframes finalIn{from{opacity:0}to{opacity:1}}
  </style>''',1)

# Extra overlays and perf meter.
s=s.replace('<div id="blackFade"></div>',r'''<div id="blackFade"></div>
  <div id="fxFlash"></div>
  <div id="perfMeter">ENHANCED · -- FPS · -- ms · -- calls · -- tris</div>
  <div id="finalScreen"><div><h1>FIN</h1><p>El Enigma de Soquetin</p><button id="restartBtn">VOLVER A EMPEZAR</button></div></div>''',1)

# Poster prompt becomes fade/scale instead of display toggle.
s=s.replace('z-index:58;display:none;padding:10px 16px;','z-index:58;display:block;opacity:0;visibility:hidden;padding:10px 16px;',1)
s=s.replace('transform:translateX(-50%);z-index:58;display:block;opacity:0;visibility:hidden;','transform:translateX(-50%) scale(.96);z-index:58;display:block;opacity:0;visibility:hidden;',1)
s=s.replace('white-space:nowrap;user-select:none">Pulsa F para ampliar</div>','white-space:nowrap;user-select:none;transition:opacity .18s ease,transform .18s ease,visibility .18s">Pulsa F para ampliar</div>',1)

# Lava receives a procedural animated texture.
old="""    const lavaMat = new THREE.MeshStandardMaterial({
      color:0xff5b15, emissive:0xff2600, emissiveIntensity:1.6, roughness:.55
    });"""
new="""    const texLava=canvasTexture(512,(g,z)=>{
      const grad=g.createLinearGradient(0,0,z,z);
      grad.addColorStop(0,'#7c0d00'); grad.addColorStop(.45,'#ff5a0a'); grad.addColorStop(1,'#ffb11b');
      g.fillStyle=grad; g.fillRect(0,0,z,z);
      for(let i=0;i<120;i++){
        g.strokeStyle=`rgba(255,${80+Math.random()*100|0},0,${.12+Math.random()*.16})`;
        g.lineWidth=2+Math.random()*6; g.beginPath();
        const y=Math.random()*z; g.moveTo(-20,y);
        for(let x=0;x<z+40;x+=32) g.lineTo(x,y+Math.sin(x*.035+Math.random()*2)*18);
        g.stroke();
      }
    },2.4,4.2);
    const lavaMat = new THREE.MeshStandardMaterial({
      map:texLava,color:0xff8a28, emissive:0xff2600, emissiveMap:texLava, emissiveIntensity:1.6, roughness:.55
    });"""
if old not in s: raise SystemExit('lava material anchor missing')
s=s.replace(old,new,1)

# Audio: ambient procedural bed + lightweight echo + pitch support.
old="""    function playSfx(key,volume=1){
      const base=sfxBase[key];
      if(!base)return;
      const a=base.cloneNode();
      a.volume=THREE.MathUtils.clamp(volume,0,1);
      a.play().catch(()=>{});
    }"""
new="""    let ambienceCtx=null;
    function ensureAmbience(){
      if(ambienceCtx){ if(ambienceCtx.state==='suspended') ambienceCtx.resume(); return; }
      const AC=window.AudioContext||window.webkitAudioContext; if(!AC)return;
      ambienceCtx=new AC();
      const master=ambienceCtx.createGain(); master.gain.value=.038; master.connect(ambienceCtx.destination);
      const len=ambienceCtx.sampleRate*3, buf=ambienceCtx.createBuffer(1,len,ambienceCtx.sampleRate), data=buf.getChannelData(0);
      for(let i=0;i<len;i++) data[i]=(Math.random()*2-1)*.18;
      const noise=ambienceCtx.createBufferSource(); noise.buffer=buf; noise.loop=true;
      const lp=ambienceCtx.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=240;
      const ng=ambienceCtx.createGain(); ng.gain.value=.18; noise.connect(lp).connect(ng).connect(master); noise.start();
      const hum=ambienceCtx.createOscillator(); hum.type='sine'; hum.frequency.value=49;
      const hg=ambienceCtx.createGain(); hg.gain.value=.035; hum.connect(hg).connect(master); hum.start();
    }
    addEventListener('pointerdown',ensureAmbience,{passive:true});
    addEventListener('keydown',ensureAmbience,{passive:true});
    function playSfx(key,volume=1,rate=1,echo=true){
      const base=sfxBase[key];
      if(!base)return;
      const a=base.cloneNode();
      a.volume=THREE.MathUtils.clamp(volume,0,1); a.playbackRate=rate;
      a.play().catch(()=>{});
      if(echo && key!=='pop') setTimeout(()=>{
        const e=base.cloneNode(); e.volume=THREE.MathUtils.clamp(volume*.11,0,.16); e.playbackRate=rate*.995; e.play().catch(()=>{});
      },72);
    }"""
if old not in s: raise SystemExit('playSfx anchor missing')
s=s.replace(old,new,1)

# Extra player state for buffered jump / idle.
s=s.replace("spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false","spawn:new THREE.Vector3(0,.02,10.2), bigJumpUsed:false, jumpBuffer:0, coyoteTime:.11, idleTime:0",1)

# Input always buffers the jump for a short time, while immediate behavior stays intact.
s=s.replace("if(e.code==='Space'){ e.preventDefault(); tryBigJump(); }","if(e.code==='Space'){ e.preventDefault(); P.jumpBuffer=.12; tryBigJump(); }",1)
s=s.replace("document.getElementById('jumpBtn').addEventListener('pointerdown',e=>{e.preventDefault();if(posterOverlayOpen) closePoster();tryBigJump();});","document.getElementById('jumpBtn').addEventListener('pointerdown',e=>{e.preventDefault();if(posterOverlayOpen) closePoster();P.jumpBuffer=.12;tryBigJump();});",1)

# Poster fade helper + final overlay.
anchor="""    let nearbyPoster=null;
    let posterOverlayOpen=false;
"""
insert="""    let nearbyPoster=null;
    let posterOverlayOpen=false;
    const fxFlash=document.getElementById('fxFlash');
    const finalScreen=document.getElementById('finalScreen');
    const restartBtn=document.getElementById('restartBtn');
    let finalPosterArmed=false;
    restartBtn?.addEventListener('click',()=>location.reload());
    function setPosterPromptVisible(show){
      posterPrompt.style.opacity=show?'1':'0';
      posterPrompt.style.visibility=show?'visible':'hidden';
      posterPrompt.style.transform=show?'translateX(-50%) scale(1)':'translateX(-50%) scale(.96)';
    }
    function pulseFlash(cls){
      fxFlash.classList.remove('hit','respawn'); void fxFlash.offsetWidth; fxFlash.classList.add(cls);
      setTimeout(()=>fxFlash.classList.remove(cls),360);
    }
"""
if anchor not in s: raise SystemExit('poster state anchor missing')
s=s.replace(anchor,insert,1)
s=s.replace("posterPrompt.style.display='none';","setPosterPromptVisible(false);",3)
s=s.replace("posterPrompt.style.display=nearbyPoster?'block':'none';","setPosterPromptVisible(!!nearbyPoster);",1)

# Arm final screen when final poster opens; show it after closing.
s=s.replace("posterOverlayImg.src=poster.userData.posterSource;","posterOverlayImg.src=poster.userData.posterSource;\n      if(String(poster.userData.posterSource).includes('AFICHE-05')) finalPosterArmed=true;",1)
s=s.replace("if(matchMedia('(pointer:fine)').matches) setTimeout(()=>renderer.domElement.requestPointerLock?.(),80);","if(finalPosterArmed){ finalPosterArmed=false; setTimeout(()=>finalScreen.classList.add('show'),180); }\n      else if(matchMedia('(pointer:fine)').matches) setTimeout(()=>renderer.domElement.requestPointerLock?.(),80);",1)

# Particle FX + blob shadow, inserted before character physics.
anchor="""    // ------------------------------------------------------------
    // CHARACTER PHYSICS
    // ------------------------------------------------------------
"""
insert=r'''    // ------------------------------------------------------------
    // ENHANCED FEEDBACK FX
    // ------------------------------------------------------------
    const dustParticles=[];
    const dustGeo=new THREE.SphereGeometry(.025,6,4);
    function spawnDust(x,y,z,count=7,warm=false){
      for(let i=0;i<count;i++){
        const mat=new THREE.MeshBasicMaterial({color:warm?0x8f3a16:0x827865,transparent:true,opacity:.26,depthWrite:false});
        const m=new THREE.Mesh(dustGeo,mat); m.position.set(x+(Math.random()-.5)*.42,y+.025,z+(Math.random()-.5)*.42);
        const sc=.7+Math.random()*1.2; m.scale.setScalar(sc); scene.add(m);
        dustParticles.push({m,age:0,life:.26+Math.random()*.24,vx:(Math.random()-.5)*.7,vy:.18+Math.random()*.35,vz:(Math.random()-.5)*.7});
      }
    }
    function updateDust(dt){
      for(let i=dustParticles.length-1;i>=0;i--){
        const p=dustParticles[i]; p.age+=dt; p.m.position.x+=p.vx*dt; p.m.position.y+=p.vy*dt; p.m.position.z+=p.vz*dt;
        const q=p.age/p.life; p.m.material.opacity=.26*(1-q); p.m.scale.multiplyScalar(1+dt*1.5);
        if(q>=1){scene.remove(p.m);p.m.material.dispose();dustParticles.splice(i,1);}
      }
    }
    const blobShadow=new THREE.Mesh(new THREE.CircleGeometry(.26,24),new THREE.MeshBasicMaterial({color:0x000000,transparent:true,opacity:.28,depthWrite:false,toneMapped:false}));
    blobShadow.rotation.x=-Math.PI/2; blobShadow.renderOrder=3; scene.add(blobShadow);
    function updateBlobShadow(){
      if(P.dead){blobShadow.visible=false;return;}
      const sup=supportAt(P.pos.x,P.pos.z); if(!sup){blobShadow.visible=false;return;}
      const h=Math.max(0,P.pos.y-sup.y); if(h>3.2){blobShadow.visible=false;return;}
      blobShadow.visible=true; blobShadow.position.set(P.pos.x,sup.y+.014,P.pos.z);
      const k=1+Math.min(1.5,h)*.32; blobShadow.scale.set(k,k,k); blobShadow.material.opacity=.28/(1+h*.55);
    }
    let cameraImpact=0;

    // ------------------------------------------------------------
    // CHARACTER PHYSICS
    // ------------------------------------------------------------
'''
if anchor not in s: raise SystemExit('character physics anchor missing')
s=s.replace(anchor,insert,1)

# False tile trigger gives a tiny visual warning, but never any support/collision.
s=s.replace("t.broken=true; t.t=0; break;","t.broken=true; t.t=0; spawnDust(t.mesh.position.x,.02,t.mesh.position.z,5,false); break;",1)

# Death/respawn flash.
s=s.replace("P.grounded=false;\n      playSfx('death',.9);","P.grounded=false;\n      pulseFlash('hit');\n      playSfx('death',.9,.98);",1)
s=s.replace("clearDeathSmoke();\n      playSfx('pop',.9);","clearDeathSmoke();\n      pulseFlash('respawn');\n      playSfx('pop',.9,1,false);",1)

# UpdatePlayer: buffer decay and idle timer.
s=s.replace("const dir=inputVector();\n      const hasInput=dir.lengthSq()>.025;","P.jumpBuffer=Math.max(0,P.jumpBuffer-dt);\n      const dir=inputVector();\n      const hasInput=dir.lengthSq()>.025;",1)

# Surface-dependent takeoff sound.
s=s.replace("playSfx('walkExpand',.48);","const takeoffSupport=supportAt(P.pos.x,P.pos.z);\n          const takeoffRate=takeoffSupport?.type==='safeTile'?1.08:takeoffSupport?.type==='column'?.94:1;\n          playSfx('walkExpand',.48,takeoffRate);",1)

# Landing feedback: dust/camera/pitch and buffered jump on real supports only.
old="""        if(!P.grounded && P.vel.y<-1.2){
          P.squash=.38;
          beginLandingTilt();
          playSfx('walkCompress',.48);
        }
        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;"""
new="""        if(!P.grounded && P.vel.y<-1.2){
          const impactVy=Math.abs(P.vel.y);
          P.squash=.38;
          beginLandingTilt();
          cameraImpact=Math.min(.12,impactVy*.016);
          spawnDust(P.pos.x,support.y,P.pos.z,Math.min(10,4+Math.floor(impactVy)),false);
          const landRate=support.type==='safeTile'?1.08:support.type==='column'?.94:1;
          playSfx('walkCompress',.48,landRate);
        }
        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;
        P.coyoteTime=.11;
        if(P.jumpBuffer>0 && !P.bigJumpUsed){ P.jumpBuffer=0; tryBigJump(); }"""
if old not in s: raise SystemExit('landing anchor missing')
s=s.replace(old,new,1)

# Coyote timer is preserved briefly after leaving legitimate support.
s=s.replace("} else if(!support || P.pos.y>0.18) {\n        P.grounded=false;\n      }","} else if(!support || P.pos.y>0.18) {\n        if(P.grounded) P.coyoteTime=.11; else P.coyoteTime=Math.max(0,P.coyoteTime-dt);\n        P.grounded=false;\n      }",1)

# Idle breathing + slow look left/right; visualRoot remains foot-pivoted and physics untouched.
old="""      visualRoot.scale.set(sxz,sy,sxz);
      updateJumpTilt(dt);"""
new="""      const trulyIdle=P.grounded && !hasInput && P.animPhase==='idle';
      if(trulyIdle){
        P.idleTime+=dt;
        const breath=Math.sin(P.idleTime*1.7);
        sy*=1+breath*.018; sxz*=1-breath*.005;
        const lookWave=Math.sin(P.idleTime*.55);
        tiltRoot.rotation.y=THREE.MathUtils.lerp(tiltRoot.rotation.y,lookWave*THREE.MathUtils.degToRad(9),1-Math.exp(-dt*2.4));
      }else{
        P.idleTime=0;
        tiltRoot.rotation.y=THREE.MathUtils.lerp(tiltRoot.rotation.y,0,1-Math.exp(-dt*8));
      }
      visualRoot.scale.set(sxz,sy,sxz);
      updateJumpTilt(dt);"""
if old not in s: raise SystemExit('visual scale anchor missing')
s=s.replace(old,new,1)

# Camera impact.
s=s.replace("const desired=tmpV2.set(\n        target.x + Math.sin(P.camYaw)*horiz,","const desired=tmpV2.set(\n        target.x + Math.sin(P.camYaw)*horiz,",1)
s=s.replace("target.z + Math.cos(P.camYaw)*horiz\n      );","target.z + Math.cos(P.camYaw)*horiz\n      );\n      cameraImpact*=Math.exp(-dt*15);\n      desired.y-=cameraImpact;",1)

# False tiles: first 0.10 s is only a tiny sink, then the existing fall. Still absent from supportRects.
old="""        if(t.t<.65){
          const k=t.t/.65;
          t.mesh.position.y=t.baseY-1.4*k*k;
          t.mesh.rotation.x=k*.8; t.mesh.rotation.z=k*.35;
        } else t.mesh.visible=false;"""
new="""        if(t.t<.10){
          const k=THREE.MathUtils.smoothstep(t.t/.10,0,1);
          t.mesh.position.y=t.baseY-.08*k;
          t.mesh.rotation.x=k*.045; t.mesh.rotation.z=k*.025;
        } else if(t.t<.65){
          const k=(t.t-.10)/.55;
          t.mesh.position.y=t.baseY-.08-1.4*k*k;
          t.mesh.rotation.x=.045+k*.8; t.mesh.rotation.z=.025+k*.35;
        } else t.mesh.visible=false;"""
if old not in s: raise SystemExit('break tile animation anchor missing')
s=s.replace(old,new,1)

# Lava bubbles and UV flow.
old="""    // Gentle lava motion
    let lavaTime=0;
    function updateLava(dt){
      lavaTime+=dt;
      lava.material.emissiveIntensity=1.45+Math.sin(lavaTime*2.1)*.2;
      lava.position.y=-10+Math.sin(lavaTime*.8)*.04;"""
new="""    // Enhanced lava motion: UV flow + small bubbles.
    let lavaTime=0, lavaBubbleTimer=0;
    const lavaBubbles=[];
    const lavaBubbleGeo=new THREE.SphereGeometry(.07,8,6);
    const lavaBubbleMat=new THREE.MeshBasicMaterial({color:0xff7a14,transparent:true,opacity:.72,toneMapped:false});
    function spawnLavaBubble(){
      const b=new THREE.Mesh(lavaBubbleGeo,lavaBubbleMat.clone());
      b.position.set((Math.random()-.5)*20.5,-9.94,Z_PIT_NORTH+Math.random()*(Z_PIT_SOUTH-Z_PIT_NORTH));
      const k=.45+Math.random()*1.2;b.scale.setScalar(k);scene.add(b);lavaBubbles.push({b,age:0,life:.35+Math.random()*.35});
    }
    function updateLava(dt){
      lavaTime+=dt; lavaBubbleTimer-=dt;
      texLava.offset.x=(lavaTime*.018)%1; texLava.offset.y=(lavaTime*.011)%1;
      lava.material.emissiveIntensity=1.45+Math.sin(lavaTime*2.1)*.2;
      lava.position.y=-10+Math.sin(lavaTime*.8)*.04;
      if(lavaBubbleTimer<=0){spawnLavaBubble();lavaBubbleTimer=.12+Math.random()*.22;}
      for(let i=lavaBubbles.length-1;i>=0;i--){const q=lavaBubbles[i];q.age+=dt;q.b.position.y+=dt*.13;q.b.scale.multiplyScalar(1+dt*.65);q.b.material.opacity=.72*(1-q.age/q.life);if(q.age>=q.life){scene.remove(q.b);q.b.material.dispose();lavaBubbles.splice(i,1);}}
"""
if old not in s: raise SystemExit('lava update anchor missing')
s=s.replace(old,new,1)

# Perf monitor and per-frame enhanced updates.
anchor="""    function animate(){
      requestAnimationFrame(animate);
      let dt=Math.min(.033,clock.getDelta());"""
insert="""    const perfMeter=document.getElementById('perfMeter');
    let perfT=0,perfFrames=0;
    function updatePerf(dt){
      perfT+=dt; perfFrames++;
      if(perfT>=.5){
        const fps=Math.round(perfFrames/perfT), ms=(1000*perfT/perfFrames).toFixed(1), info=renderer.info.render;
        perfMeter.textContent=`ENHANCED · ${fps} FPS · ${ms} ms · ${info.calls} calls · ${Math.round(info.triangles/1000)}k tris`;
        perfT=0; perfFrames=0;
      }
    }
    function animate(){
      requestAnimationFrame(animate);
      let dt=Math.min(.033,clock.getDelta());"""
if anchor not in s: raise SystemExit('animate anchor missing')
s=s.replace(anchor,insert,1)
s=s.replace("updateDeathSmoke(dt);\n      updatePosterInteraction();","updateDeathSmoke(dt);\n      updateDust(dt);\n      updateBlobShadow();\n      updatePosterInteraction();",1)
s=s.replace("renderer.render(scene,camera);","renderer.render(scene,camera);\n      updatePerf(dt);",1)

# Ensure preload label identifies alt version without touching gameplay title art.
s=s.replace("<div id=\"loadText\">CARGANDO · 0%</div>","<div id=\"loadText\">CARGANDO ENHANCED · 0%</div>",1)

Path('index2.html').write_text(s,encoding='utf-8')
print('index2.html generated with enhanced visual/game-feel experiment')
