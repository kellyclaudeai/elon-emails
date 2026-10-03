import asyncio
from PIL import Image,ImageDraw
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1200,'height':630})
        await pg.goto('file:///home/claude/build/assets/og.html'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='og.png'); await b.close()
asyncio.run(main())
def icon(n):
    s=4; N=n*s; im=Image.new('RGB',(N,N),'#ffd60a'); d=ImageDraw.Draw(im)
    u=N/32  # E drawn on a 32 grid: stem x 9-14, bars to x 23, y 7-25
    k='#0a0a0a'
    d.rectangle([9*u,7*u,14*u,25*u],fill=k)
    for y0 in (7,13.75,20.5): d.rectangle([9*u,y0*u,23.5*u,(y0+4.5)*u],fill=k)
    return im.resize((n,n),Image.LANCZOS)
icon(180).save('apple-touch-icon.png'); icon(192).save('icon-192.png'); icon(512).save('icon-512.png')
icon(48).save('favicon.ico',sizes=[(16,16),(32,32),(48,48)])
open('favicon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#ffd60a"/><path fill="#0a0a0a" d="M9 7h14.5v4.5H14v2.25h9.5v4.5H14v2.25h9.5V25H9z"/></svg>')
