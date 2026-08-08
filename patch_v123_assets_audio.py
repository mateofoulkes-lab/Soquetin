from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('V1.22 · distancia de afiches + salto','V1.23 · afiches y sonidos finales',1)

old_posters="""    // All poster planes are 150% of their previous physical size.\n    posterOnHorizontalWall(-3.9,2.0,Z_CHALLENGE_SOUTH+.001,3.225,1.875,'IMAGEN 01',false,false);\n    posterOnHorizontalWall(3.9,2.0,Z_CHALLENGE_SOUTH+.001,3.225,1.875,'IMAGEN 02',false,false);\n    // Poster 03 uses the movement artwork. 3.75 / 2.175 matches its 1647:955 aspect ratio.\n    posterOnHorizontalWall(0,2.15,Z_START_FRONT-.001,3.75,2.175,'1000142570.jpg',true,true);\n    posterOnHorizontalWall(-2.8,2.0,Z_COMMON_NORTH+.001,2.25,1.725,'PISTA',false,false);\n    posterOnRightWall(FINAL_RIGHT,2.15,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,3.30,2.175,'INSTAGRAM',false);\n"""
new_posters="""    // Final artwork set. Keep each plane close to the source aspect ratio to avoid stretching.\n    posterOnHorizontalWall(-3.9,2.0,Z_CHALLENGE_SOUTH+.001,3.225,2.419,'AFICHE-01.JPG',false,true);\n    posterOnHorizontalWall(3.9,2.0,Z_CHALLENGE_SOUTH+.001,3.225,2.419,'AFICHE-02.JPG',false,true);\n    // AFICHE-03 is the movement/control poster (wide format).\n    posterOnHorizontalWall(0,2.15,Z_START_FRONT-.001,3.75,2.175,'AFICHE-03.JPG',true,true);\n    // AFICHE-04 is the pre-final congratulations poster.\n    posterOnHorizontalWall(-2.8,2.0,Z_COMMON_NORTH+.001,2.25,1.688,'AFICHE-04.JPG',false,true);\n    // AFICHE-05 is the Instagram reveal in the final room.\n    posterOnRightWall(FINAL_RIGHT,2.15,(Z_COMMON_NORTH+Z_FINAL_NORTH)/2,3.30,2.475,'AFICHE-05.JPG',true);\n"""
if old_posters not in s: raise SystemExit('poster block not found')
s=s.replace(old_posters,new_posters,1)

old_audio="""    // ------------------------------------------------------------\n    // AUDIO\n    // ------------------------------------------------------------\n    let audioCtx=null;\n    function ensureAudio(){ if(!audioCtx) audioCtx=new (window.AudioContext||window.webkitAudioContext)(); if(audioCtx.state==='suspended')audioCtx.resume(); }\n    function tone(freq,dur=.1,type='sine',gain=.05){\n      if(!audioCtx) return;\n      const o=audioCtx.createOscillator(), g=audioCtx.createGain(); o.type=type; o.frequency.value=freq;\n      g.gain.setValueAtTime(gain,audioCtx.currentTime); g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+dur);\n      o.connect(g).connect(audioCtx.destination); o.start(); o.stop(audioCtx.currentTime+dur);\n    }\n    function welcome(){ ensureAudio(); tone(392,.08,'triangle',.035); setTimeout(()=>tone(523,.11,'triangle',.03),100); }\n    function lavaSound(){ ensureAudio(); tone(90,.26,'sawtooth',.06); setTimeout(()=>tone(58,.30,'square',.035),40); }\n"""
new_audio="""    // ------------------------------------------------------------\n    // AUDIO\n    // ------------------------------------------------------------\n    const SFX={\n      death:'death.mp3',\n      jump:'jump1.mp3',\n      pop:'pop.mp3',\n      walkCompress:'walk-compress.mp3',\n      walkExpand:'walk-expand.mp3'\n    };\n    const sfxBase={};\n    for(const [key,src] of Object.entries(SFX)){\n      const a=new Audio(src);\n      a.preload='auto';\n      sfxBase[key]=a;\n    }\n    function playSfx(key,volume=1){\n      const base=sfxBase[key];\n      if(!base)return;\n      const a=base.cloneNode();\n      a.volume=THREE.MathUtils.clamp(volume,0,1);\n      a.play().catch(()=>{});\n    }\n    // Keep one tiny synthetic effect for false tiles.\n    let audioCtx=null;\n    function tone(freq,dur=.1,type='sine',gain=.05){\n      if(!audioCtx) audioCtx=new (window.AudioContext||window.webkitAudioContext)();\n      if(audioCtx.state==='suspended') audioCtx.resume();\n      const o=audioCtx.createOscillator(), g=audioCtx.createGain();\n      o.type=type; o.frequency.value=freq;\n      g.gain.setValueAtTime(gain,audioCtx.currentTime);\n      g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+dur);\n      o.connect(g).connect(audioCtx.destination); o.start(); o.stop(audioCtx.currentTime+dur);\n    }\n"""
if old_audio not in s: raise SystemExit('audio block not found')
s=s.replace(old_audio,new_audio,1)

# Big jump sound.
s=s.replace("      beginJumpTilt(4.433);","      beginJumpTilt(4.433);\n      playSfx('jump',.82);",1)

# Keep the existing synthetic false-tile click for now.

# Death sound.
s=s.replace("      lavaSound();","      playSfx('death',.9);",1)

# Automatic hop expansion sound.
s=s.replace("          beginJumpTilt(2.585);","          beginJumpTilt(2.585);\n          playSfx('walkExpand',.48);",1)

# Landing/compression sound on real landings.
s=s.replace("          P.squash=.38;\n          beginLandingTilt();","          P.squash=.38;\n          beginLandingTilt();\n          playSfx('walkCompress',.48);",1)

# Respawn pop.
s=s.replace("      clearDeathSmoke();\n    }","      clearDeathSmoke();\n      playSfx('pop',.9);\n    }",1)

# Preload all final artwork and sound assets.
old_pre="const preloadAssets=[SOQUETIN_MODEL_URL,'1000142570.jpg'];"
new_pre="const preloadAssets=[SOQUETIN_MODEL_URL,'AFICHE-01.JPG','AFICHE-02.JPG','AFICHE-03.JPG','AFICHE-04.JPG','AFICHE-05.JPG','death.mp3','jump1.mp3','pop.mp3','walk-compress.mp3','walk-expand.mp3'];"
if old_pre not in s: raise SystemExit('preload list not found')
s=s.replace(old_pre,new_pre,1)

p.write_text(s,encoding='utf-8')
print('patched V1.23 assets + audio')
