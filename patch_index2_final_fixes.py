from pathlib import Path
p=Path('index2.html')
s=p.read_text(encoding='utf-8')
old="""        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;
        P.coyoteTime=.11;
        if(P.jumpBuffer>0 && !P.bigJumpUsed){ P.jumpBuffer=0; tryBigJump(); }"""
new="""        P.pos.y=support.y+.02; P.vel.y=0; P.grounded=true;
        P.coyoteTime=.11;
        // A real support resets the one-big-jump lock before consuming the buffer.
        // False tiles never reach this branch because they are not supportRects.
        P.bigJumpUsed=false;
        if(P.jumpBuffer>0){ P.jumpBuffer=0; tryBigJump(); }"""
if old not in s: raise SystemExit('landing buffer anchor missing')
s=s.replace(old,new,1)
old="if(finalPosterArmed){ finalPosterArmed=false; setTimeout(()=>finalScreen.classList.add('show'),180); }"
new="if(finalPosterArmed){ finalPosterArmed=false; setTimeout(()=>{ gameReady=false; P.vel.set(0,0,0); finalScreen.classList.add('show'); },180); }"
if old not in s: raise SystemExit('final screen anchor missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('fixed buffered landing jump and froze gameplay on final screen')
