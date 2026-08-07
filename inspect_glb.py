import json, struct
from pathlib import Path
p=Path('3354c2e8-ca8b-4056-87f9-db61cd76f25d.glb')
b=p.read_bytes()
magic,version,length=struct.unpack_from('<4sII',b,0)
out={'magic':magic.decode('ascii','replace'),'version':version,'declaredLength':length,'actualLength':len(b)}
o=12
chunks=[]
while o+8<=len(b):
    clen,ctype=struct.unpack_from('<II',b,o); o+=8
    data=b[o:o+clen]; o+=clen
    chunks.append({'type':hex(ctype),'length':clen})
    if ctype==0x4E4F534A:
        j=json.loads(data.decode('utf-8').rstrip('\x00 \t\r\n'))
        out['asset']=j.get('asset')
        out['extensionsUsed']=j.get('extensionsUsed',[])
        out['extensionsRequired']=j.get('extensionsRequired',[])
        out['images']=[{k:v for k,v in img.items() if k in ('mimeType','uri','name')} for img in j.get('images',[])]
        out['meshes']=len(j.get('meshes',[])); out['nodes']=len(j.get('nodes',[])); out['materials']=len(j.get('materials',[]))
out['chunks']=chunks
Path('glb-diagnostic.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))