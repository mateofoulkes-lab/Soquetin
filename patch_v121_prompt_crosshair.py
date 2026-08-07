from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Version badge.
s=s.replace('V1.20 · ajuste UV en superficies equivalentes','V1.21 · interacción de afiches simplificada',1)

# Remove crosshair CSS + element (the floating dot above Soquetin).
s=s.replace("    #crosshair { position:absolute; left:50%; top:50%; width:5px; height:5px; margin:-2px; border-radius:50%; background:rgba(255,255,255,.55); }\n",'',1)
s=s.replace("      #crosshair { display:none; }\n",'',1)
s=s.replace('    <div id="crosshair"></div>\n','',1)

# Restyle poster prompt: neutral translucent gray rounded frame.
old_prompt='''  <div id="posterPrompt" style="position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:18;display:none;padding:10px 16px;border-radius:10px;background:rgba(0,0,0,.68);border:1px solid rgba(255,255,255,.18);color:#fff;font:700 14px Inter,system-ui,sans-serif;pointer-events:none;backdrop-filter:blur(5px);white-space:nowrap">Toca la imagen o presiona F para ampliar...</div>'''
new_prompt='''  <div id="posterPrompt" style="position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:58;display:none;padding:10px 16px;border-radius:14px;background:rgba(105,105,105,.46);border:1px solid rgba(255,255,255,.26);color:#fff;font:700 14px Inter,system-ui,sans-serif;pointer-events:none;backdrop-filter:blur(6px);white-space:nowrap;user-select:none">Pulsa F para ampliar</div>'''
if old_prompt not in s: raise SystemExit('poster prompt HTML not found')
s=s.replace(old_prompt,new_prompt,1)

# Replace screen-space poster click/touch machinery with device-specific prompt behavior.
start=s.index('    // Screen-space poster hit testing: robust on mobile and independent from 3D raycasts.')
end=s.index("    document.addEventListener('mousemove',e=>{", start)
replacement='''    const isMobileUI=matchMedia('(pointer:coarse)').matches;\n    posterPrompt.textContent=isMobileUI?'Pulsa aquí para ampliar':'Pulsa F para ampliar';\n    if(isMobileUI){\n      posterPrompt.style.pointerEvents='auto';\n      posterPrompt.style.cursor='pointer';\n      posterPrompt.addEventListener('pointerdown',e=>{\n        if(!nearbyPoster || posterOverlayOpen || P.dead)return;\n        e.preventDefault();\n        e.stopPropagation();\n        openPoster(nearbyPoster);\n      });\n    }\n\n'''
s=s[:start]+replacement+s[end:]

# F only works on desktop/fine pointer. Mobile uses prompt only.
s=s.replace("      if(e.code==='KeyF'){\n        e.preventDefault();\n        if(posterOverlayOpen) closePoster(); else if(nearbyPoster) openPoster(nearbyPoster);\n        return;\n      }",
'''      if(e.code==='KeyF' && !isMobileUI){\n        e.preventDefault();\n        if(posterOverlayOpen) closePoster(); else if(nearbyPoster) openPoster(nearbyPoster);\n        return;\n      }''',1)

# Only advertise/open a poster when the player is on its geometric front side.
s=s.replace("        if(d<bestD){bestD=d;best=poster;}","        if(isPosterFrontFacing(poster) && d<bestD){bestD=d;best=poster;}",1)

# Prompt should always reflect the current device mode when shown.
s=s.replace("      posterPrompt.style.display=nearbyPoster?'block':'none';",
"      posterPrompt.textContent=isMobileUI?'Pulsa aquí para ampliar':'Pulsa F para ampliar';\n      posterPrompt.style.display=nearbyPoster?'block':'none';",1)

p.write_text(s,encoding='utf-8')
print('patched V1.21')
