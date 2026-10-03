import json,html,os,shutil
D=json.load(open('emails.json'))
tpl=open('page.tpl.html').read()
data=json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/').replace('<!--','<\\!--')
updated='October 3, 2026'
BASE=os.environ.get('BASE_URL','')
def page(cfg):
    return tpl.replace('/*DATA*/',data).replace('/*CFG*/{}',json.dumps(cfg))
os.makedirs('out',exist_ok=True)
open('out/elon-mails.html','w').write(page({'updated':updated}))
shutil.rmtree('site',ignore_errors=True); os.makedirs('site/e')
E=html.escape
head='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
head+='<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#ffd60a">'
def og(title,descr,path,kind):
    if not BASE: return ''
    t=E(title);d=E(descr);u=BASE+path;img=BASE+'og.png'
    return ('<meta property="og:site_name" content="Elon Emails"><meta property="og:type" content="%s"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s">'
            '<meta property="og:image" content="%s"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Elon Emails: a printed email from Elon Musk on a yellow background">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">')%(kind,t,d,u,img,t,d,img)
desc='A searchable archive of every publicly available Elon Musk email: company memos, court exhibits and leaks, with the published text, dates, tags and sources.'
idx=page({'updated':updated,'pdf':'elon-mails.pdf','pages':True,'base':BASE})
h,b=idx.split('</style>',1)
canon=('<link rel="canonical" href="%s">'%BASE) if BASE else ''
open('site/index.html','w').write(head+'<meta name="description" content="'+E(desc)+'">'+og('Elon Emails',desc,'','website')+canon+h+'</style></head><body>'+b+'</body></html>')
css=tpl.split('<style>')[1].split('</style>')[0]
font=tpl.split('\n')[1]
ST={'partial':'Partial text. Only these passages were published; [...] marks a gap.','excerpt':'Excerpt. Only this much of the email has been made public.','none':'No text of this email has been published. See the summary below.'}
band='<header class="top small"><div class="wrap"><a href="%sindex.html"><h1>Elon Emails</h1></a></div></header>'
foot='<footer><p>An unofficial, independent compilation. Not affiliated with Elon Musk or any of his companies. Text is reproduced as published by the linked source.</p></footer>'
for n,e in enumerate(D):
    prev=D[n-1] if n else None; nxt=D[n+1] if n+1<len(D) else None
    src=[{'name':e['source_name'],'url':e['source_url']}]+e['more_sources']
    c=('<link rel="canonical" href="%se/%s.html">'%(BASE,e['id'])) if BASE else ''
    p=[head,'<title>',E(e['title']),' | Elon Emails</title><meta name="description" content="',E(e['summary']),'">',og(e['title'],(e['sender']+' to '+e['to']+', '+e['date_display']+'. '+e['summary'])[:300],'e/%s.html'%e['id'],'article'),c,font,'<style>',css,'</style></head><body>',band%'../',
       '<div class="wrap"><main><h2 class="pagehead">',E(e['title']),'</h2><div class="sheet"><dl class="hdr"><dt>From:</dt><dd>',E(e['sender_full']),'</dd><dt>Date:</dt><dd>',E(e['date_display']),(' <span class="aside">('+E(e['date_note'])+')</span>' if e['date_note'] else ''),'</dd><dt>To:</dt><dd>',E(e['to']),'</dd>']
    if e['subject']: p+=['<dt>Subject:</dt><dd>',E(e['subject']),'</dd>']
    p.append('</dl>')
    if e['text_status']!='full': p+=['<p class="status">',ST[e['text_status']],'</p>']
    if e['text']: p+=['<div class="bodytext">',E(e['text']),'</div>']
    p+=['<div class="meta"><div><p class="label">About this email</p><p>',E(e['summary']),'</p></div>']
    if e['notes']: p+=['<div><p class="label">Notes</p><p>',E(e['notes']),'</p></div>']
    p+=['<div><p class="label">Where it came from</p><p>',E(e['provenance']),'; attribution ',E(e['confidence'].lower()),'.</p><ul>']+['<li><a href="%s" rel="noopener">%s</a></li>'%(E(s['url']),E(s['name'] or s['url'])) for s in src]+['</ul></div>']
    p+=['<p>',E(e['company']),', ',E(e['category'].lower()),'. Tags: ',E(', '.join(e['tags'])),'</p>']
    p+=['<div class="actions">']
    if prev: p.append('<a class="btn" href="%s.html">Earlier email</a>'%prev['id'])
    p.append('<a class="btn solid" href="../index.html">Search all emails</a>')
    if nxt: p.append('<a class="btn" href="%s.html">Later email</a>'%nxt['id'])
    p+=['</div></div></div></main>',foot,'</div></body></html>']
    open('site/e/%s.html'%e['id'],'w').write(''.join(p))
rows=''.join('<li><span class="date">%s</span> <a href="e/%s.html">%s</a> <span class="aside">%s to %s</span></li>'%(E(e['date_display']),e['id'],E(e['title']),E(e['sender']),E(e['to'])) for e in D)
open('site/all.html','w').write(head+'<title>Every email by date | Elon Emails</title>'+og('Every email by date | Elon Emails','A plain list of all %d emails in the archive, oldest first.'%len(D),'all.html','website')+font+'<style>'+css+'</style></head><body>'+band%''+'<div class="wrap"><main><h2 class="pagehead">All %d emails, oldest first</h2><ul class="plain">%s</ul></main>%s</div></body></html>'%(len(D),rows,foot))
open('site/README.txt','w').write('Elon Emails static site.\n\nindex.html  searchable archive (single page)\nall.html    plain list linking to every email page\ne/          one static page per email, for search engines and sharing\nelon-mails.pdf  the full archive as a PDF\nemails.json     the dataset\n\nUpload this folder as-is to any static host. No build step.\n')
if BASE:
    urls=[BASE,BASE+'all.html']+[BASE+'e/%s.html'%e['id'] for e in D]
    open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>%s</loc></url>'%u for u in urls)+'</urlset>')
    open('site/robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n'%BASE)
for f in ['og.png','favicon.ico','favicon.svg','apple-touch-icon.png','icon-192.png','icon-512.png']:
    if os.path.exists('assets/'+f): shutil.copy('assets/'+f,'site/'+f)
json.dump(D,open('site/emails.json','w'),ensure_ascii=False)
print(len(D),os.path.getsize('out/elon-mails.html'),os.path.getsize('site/index.html'),len(os.listdir('site/e')))
