from pathlib import Path
import re

p=Path('index2.html')
s=p.read_text(encoding='utf-8')

# Remove performance meter CSS.
s=re.sub(r'\n\s*#perfMeter\{.*?\}', '', s, count=1, flags=re.S)

# Remove final-screen CSS as one contiguous block.
s=re.sub(r'\n\s*#finalScreen\{.*?@keyframes finalIn\{from\{opacity:0\}to\{opacity:1\}\}', '', s, count=1, flags=re.S)

# Remove performance meter and final-screen markup.
s=re.sub(r'\n\s*<div id="perfMeter">.*?</div>', '', s, count=1, flags=re.S)
s=re.sub(r'\n\s*<div id="finalScreen">.*?</div></div>', '', s, count=1, flags=re.S)

# Remove all purely decorative max-aesthetics additions (torches/webs/cracks/rocks/lava smoke).
start='    // ------------------------------------------------------------\n    // MAX AESTHETICS TEST — decorative only, no gameplay collision/support.\n'
end='    // Apply exported UV/repeat settings after all dungeon geometry is built.\n'
if start not in s or end not in s:
    raise SystemExit('max-aesthetics block anchors not found')
a=s.index(start)
b=s.index(end,a)
s=s[:a]+s[b:]

# Remove final-screen state / button logic while preserving fxFlash.
s=s.replace("    const finalScreen=document.getElementById('finalScreen');\n    const restartBtn=document.getElementById('restartBtn');\n    let finalPosterArmed=false;\n    restartBtn?.addEventListener('click',()=>location.reload());\n",'',1)
s=s.replace("      if(String(poster.userData.posterSource).includes('AFICHE-05')) finalPosterArmed=true;\n",'',1)
old="""      if(finalPosterArmed){ finalPosterArmed=false; setTimeout(()=>{ gameReady=false; P.vel.set(0,0,0); finalScreen.classList.add('show'); },180); }
      else if(matchMedia('(pointer:fine)').matches) setTimeout(()=>renderer.domElement.requestPointerLock?.(),80);"""
new="""      if(matchMedia('(pointer:fine)').matches) setTimeout(()=>renderer.domElement.requestPointerLock?.(),80);"""
if old not in s:
    raise SystemExit('final poster close logic not found')
s=s.replace(old,new,1)

# Remove performance meter JS block and call.
s=re.sub(r"\n\s*const perfMeter=document\.getElementById\('perfMeter'\);.*?\n\s*function updatePerf\(dt\)\{.*?\n\s*\}\n", '\n', s, count=1, flags=re.S)
s=s.replace('      updatePerf(dt);\n','',1)

# Remove max-aesthetics update call if present.
s=s.replace('      updateMaxAesthetics(dt);\n','',1)

# Sanity checks: none of the rolled-back systems may remain referenced.
for forbidden in [
    'aestheticTorches','addTorch(','addWeb(','addCrack(','rockAreas','lavaSmoke','updateMaxAesthetics',
    'perfMeter','updatePerf(','finalScreen','finalPosterArmed','restartBtn'
]:
    if forbidden in s:
        raise SystemExit(f'forbidden reference remains: {forbidden}')

# Required enhanced systems must remain.
for required in [
    'jumpBuffer','.coyoteTime','function tryBigJump','blobShadow','spawnDust','ensureAmbience',
    'lavaCanvas','ClampToEdgeWrapping','function updateBreakTiles','setPosterPromptVisible'
]:
    if required not in s:
        raise SystemExit(f'required enhanced feature missing: {required}')

p.write_text(s,encoding='utf-8')
print('cleaned index2.html',len(s))
