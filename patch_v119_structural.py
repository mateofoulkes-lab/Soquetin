from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Rename game everywhere in visible HTML / title.
s=s.replace('<title>Recuperador de password de Soquetin</title>','<title>El Enigma de Soquetin</title>')
s=s.replace('Recuperador de password de Soquetin · V1.18','El Enigma de Soquetin · V1.19')
s=s.replace('Recuperador de password de Soquetin','El Enigma de Soquetin')

# Replace old start overlay CSS block with splash screen styles.
start_css="""    #startOverlay {\n      position:fixed; inset:0; z-index:20; background:radial-gradient(circle at 50% 42%, #2e2920 0, #14110d 48%, #070605 100%);\n      display:grid; place-items:center; padding:24px;\n    }\n    #startCard {\n      width:min(520px,92vw); padding:26px; border:1px solid rgba(255,255,255,.14);\n      border-radius:18px; background:rgba(15,13,10,.78); box-shadow:0 24px 80px rgba(0,0,0,.48);\n    }\n    #startCard h1 { margin:0 0 10px; font-size:clamp(25px,4vw,38px); }\n    #startCard p { margin:8px 0 18px; color:#d6d0c4; line-height:1.45; }\n    #startBtn {\n      appearance:none; border:0; border-radius:12px; padding:13px 18px; width:100%;\n      font-weight:800; font-size:16px; cursor:pointer; background:#ded0a7; color:#201b13;\n    }\n    #status { margin-top:12px; font-size:12px; opacity:.65; text-align:center; }\n"""
splash_css="""    #splash {\n      position:fixed; inset:0; z-index:120; display:grid; place-items:center; padding:24px;\n      background:#050504; opacity:1; transition:opacity .32s ease; pointer-events:auto;\n    }\n    #splash.fade-out { opacity:0; }\n    #splashCard { width:min(430px,84vw); text-align:center; }\n    #splashTitle { font-weight:850; font-size:clamp(24px,5vw,38px); letter-spacing:.015em; margin-bottom:20px; }\n    #loadTrack { width:100%; height:7px; overflow:hidden; border-radius:999px; background:rgba(255,255,255,.12); }\n    #loadBar { width:0%; height:100%; background:#e8dfc7; transition:width .12s linear; }\n    #loadText { margin-top:9px; font:600 11px ui-monospace,monospace; opacity:.62; }\n    #blackFade { position:fixed; inset:0; z-index:119; background:#000; opacity:0; pointer-events:none; transition:opacity .22s ease; }\n    #blackFade.on { opacity:1; }\n    #buildInfo {\n      position:fixed; left:10px; bottom:9px; z-index:55; padding:6px 8px; border-radius:7px;\n      background:rgba(0,0,0,.42); border:1px solid rgba(255,255,255,.10); color:rgba(255,255,255,.72);\n      font:600 10px/1.25 ui-monospace,monospace; pointer-events:none; backdrop-filter:blur(4px);\n    }\n"""
if start_css not in s: raise SystemExit('start CSS anchor not found')
s=s.replace(start_css,splash_css,1)

# Replace presentation HTML with loading splash.
old_html="""  <div id=\"startOverlay\">\n    <div id=\"startCard\">\n      <h1>El Enigma de Soquetin</h1>\n      <p>Prototipo V1.18: exploración 3D, saltos, losetas falsas, columnas, lava y respawn. Modelo Soquetin GLB provisional integrado.</p>\n      <button id=\"startBtn\">ENTRAR AL DUNGEON</button>\n      <div id=\"status\">PC: WASD / flechas · Mouse · Espacio &nbsp;—&nbsp; Celular: dos controles + SALTO</div>\n    </div>\n  </div>\n"""
new_html="""  <div id=\"splash\">\n    <div id=\"splashCard\">\n      <div id=\"splashTitle\">El Enigma de Soquetin</div>\n      <div id=\"loadTrack\"><div id=\"loadBar\"></div></div>\n      <div id=\"loadText\">CARGANDO · 0%</div>\n    </div>\n  </div>\n  <div id=\"blackFade\"></div>\n  <div id=\"buildInfo\">V1.19 · splash + nombre nuevo</div>\n"""
if old_html not in s: raise SystemExit('start HTML anchor not found')
s=s.replace(old_html,new_html,1)

# Remove old HUD title and keep model diagnostic hidden (still useful internally).
s=s.replace('<div id="title">El Enigma de Soquetin · V1.19</div><div id="modelStatus"','<div id="modelStatus"')
s=s.replace('style="position:absolute;left:18px;top:58px;','style="display:none;position:absolute;left:18px;top:58px;',1)

# Renderer click no longer checks the old start screen.
s=s.replace(" && document.getElementById('startOverlay').style.display==='none'","")

# Replace old button-start section with a real preloader and short black transition.
old_start="""    // ------------------------------------------------------------\n    // START\n    // ------------------------------------------------------------\n    document.getElementById('startBtn').addEventListener('click',()=>{\n      ensureAudio(); welcome();\n      document.getElementById('startOverlay').style.display='none';\n      if(matchMedia('(pointer:fine)').matches) setTimeout(()=>renderer.domElement.requestPointerLock?.(),80);\n    });\n"""
new_start="""    // ------------------------------------------------------------\n    // SPLASH / PRELOAD\n    // ------------------------------------------------------------\n    let gameReady=false;\n    const splash=document.getElementById('splash');\n    const blackFade=document.getElementById('blackFade');\n    const loadBar=document.getElementById('loadBar');\n    const loadText=document.getElementById('loadText');\n    const preloadAssets=[SOQUETIN_MODEL_URL,'1000142570.jpg'];\n    async function preloadGame(){\n      let done=0;\n      const setProgress=()=>{\n        const pct=Math.round((done/preloadAssets.length)*100);\n        loadBar.style.width=pct+'%'; loadText.textContent=`CARGANDO · ${pct}%`;\n      };\n      await Promise.all(preloadAssets.map(async url=>{\n        try{\n          const r=await fetch(url,{cache:'force-cache'});\n          if(!r.ok) throw new Error(String(r.status));\n          await r.blob();\n        }catch(err){ console.warn('Preload warning',url,err); }\n        done++; setProgress();\n      }));\n      loadBar.style.width='100%'; loadText.textContent='CARGANDO · 100%';\n      await new Promise(r=>setTimeout(r,120));\n      blackFade.classList.add('on');\n      await new Promise(r=>setTimeout(r,220));\n      splash.classList.add('fade-out');\n      await new Promise(r=>setTimeout(r,320));\n      splash.remove();\n      await new Promise(r=>setTimeout(r,90));\n      blackFade.classList.remove('on');\n      setTimeout(()=>blackFade.remove(),260);\n      gameReady=true;\n    }\n    preloadGame();\n"""
if old_start not in s: raise SystemExit('start JS anchor not found')
s=s.replace(old_start,new_start,1)

# Do not move the player under the splash.
s=s.replace('      updatePlayer(dt);','      if(gameReady) updatePlayer(dt);',1)

# Ensure no visible legacy phrase remains.
if 'Recuperador de password' in s or 'recuperación de password' in s.lower():
    raise SystemExit('legacy password wording remains')

p.write_text(s,encoding='utf-8')
print('patched V1.19 structural')
