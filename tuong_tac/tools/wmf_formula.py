"""Render equation WMFs without losing GDI character advances or UPDATECP.

Only equation assets use this route. Assembly illustrations keep the native
Inkscape importer. The glyph positions, font sizes and lines come from the
uploaded WMF records, rather than a re-typed mathematical interpretation.
"""
from pathlib import Path
from html import escape
import struct
from reportlab.pdfbase import _fontdata,pdfmetrics
from fontTools.agl import toUnicode

def render_equation(path):
    b=Path(path).read_bytes()
    if b[:4]!=b'\xd7\xcd\xc6\x9a':raise ValueError('A placeable WMF is required')
    _,_,left,top,right,bottom,_,_,_=struct.unpack('<I H hhhh H I H',b[:22])
    header=struct.unpack_from('<HHHIHIH',b,22)
    objects=[None]*header[4]
    font=dict(height=-100,width=0,italic=False,bold=False,charset=0,name='Times New Roman')
    pen=dict(width=3,color='#000000')
    current=[0,0];align=0;parts=[];p=40;color='#000000'
    def alloc(obj):
        try:i=objects.index(None)
        except ValueError:i=len(objects);objects.append(None)
        objects[i]=obj
    def rgb(v):return '#%02x%02x%02x'%(v&255,(v>>8)&255,(v>>16)&255)
    while p+6<=len(b):
        size,fn=struct.unpack_from('<IH',b,p)
        if size<3:break
        v=b[p+6:p+size*2]
        if fn==0x2fb:
            h,w,_,_,weight=struct.unpack_from('<hhhhh',v)
            alloc(dict(kind='font',height=h,width=w,bold=weight>=600,italic=bool(v[10]),
                       charset=v[13],name=v[18:].split(b'\0')[0].decode('latin1')))
        elif fn==0x2fa:
            style,width,_,c=struct.unpack_from('<HhhI',v)
            alloc(dict(kind='pen',width=max(2,abs(width)),color=rgb(c)))
        elif fn in [0x2fc,0xf7,0x142,0x1f9,0x6fe,0x6ff,0x2fd]:alloc(dict(kind='other'))
        elif fn==0x1f0:
            i=struct.unpack_from('<H',v)[0]
            if i<len(objects):objects[i]=None
        elif fn==0x12d:
            i=struct.unpack_from('<H',v)[0]
            obj=objects[i] if i<len(objects) else None
            if obj and obj['kind']=='font':font=obj.copy()
            if obj and obj['kind']=='pen':pen=obj.copy()
        elif fn==0x12e:align=struct.unpack_from('<H',v)[0]
        elif fn==0x209:color=rgb(struct.unpack_from('<I',v)[0])
        elif fn==0x214:
            y,x=struct.unpack_from('<hh',v);current=[x,y]
        elif fn==0x213:
            y,x=struct.unpack_from('<hh',v)
            parts.append(f'<path d="M{current[0]} {current[1]} L{x} {y}" fill="none" stroke="{pen["color"]}" stroke-width="{pen["width"]}"/>')
            current=[x,y]
        elif fn==0xa32:
            y,x,n,opt=struct.unpack_from('<hhHH',v)
            start=8+(8 if opt&6 else 0);chars=v[start:start+n]
            remainder=v[start+((n+1)//2)*2:]
            dx=list(struct.unpack('<'+'h'*(len(remainder)//2),remainder))
            if len(dx)<n:
                dx=[]
                for char in chars:
                    if font['name'].lower()=='symbol':
                        name=_fontdata.encodings['SymbolEncoding'][char]
                        text=toUnicode(name) if name else chr(char)
                        dx.append(pdfmetrics.stringWidth(text,'Symbol',abs(font['height'])))
                    else:
                        text=bytes([char]).decode('cp1252')
                        dx.append(pdfmetrics.stringWidth(text,'Times-Italic' if font['italic'] else 'Times-Roman',abs(font['height'])))
            if align&1:x,y=current
            height=abs(font['height'])
            # Equation WMFs set TA_BASELINE. Support TOP/BOTTOM for completeness.
            if align&24==24:baseline=y
            elif align&8:baseline=y-height*.2
            else:baseline=y+height*.8
            if align&6==6:x-=sum(dx[:n])/2
            elif align&2:x-=sum(dx[:n])
            for i,char in enumerate(chars):
                symbol=font['name'].lower()=='symbol'
                if symbol:
                    name=_fontdata.encodings['SymbolEncoding'][char]
                    text=toUnicode(name) if name else chr(char)
                else:text=bytes([char]).decode('cp1252')
                if text.strip():
                    family='Times New Roman, DejaVu Serif, serif'
                    style='italic' if font['italic'] and not symbol else 'normal'
                    parts.append(f'<text x="{x}" y="{baseline}" font-family="{family}" font-size="{height}" font-style="{style}" font-weight="{700 if font["bold"] else 400}" fill="{color}">{escape(text)}</text>')
                x+=dx[i]
            if align&1:current=[x,y]
        p+=size*2
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left} {top} {right-left} {bottom-top}" width="{right-left}" height="{bottom-top}"><rect x="{left}" y="{top}" width="{right-left}" height="{bottom-top}" fill="white"/>'+''.join(parts)+'</svg>'
