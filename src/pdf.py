import json,collections,re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,KeepTogether,HRFlowable,CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
import os
F=os.environ.get('FONTDIR','/usr/share/fonts/truetype/dejavu/')
for n,f in [('Sans','DejaVuSans.ttf'),('Sans-B','DejaVuSans-Bold.ttf'),('Sans-I','DejaVuSans-Oblique.ttf'),('Serif','DejaVuSerif.ttf'),('Serif-B','DejaVuSerif-Bold.ttf'),('Mono','DejaVuSansMono.ttf'),('Cond-B','DejaVuSansCondensed-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(n,F+(f if os.path.exists(F+f) else 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='Sans-B',italic='Sans-I',boldItalic='Sans-B')
D=json.load(open('emails.json'))
INK=colors.HexColor('#131820');MUTED=colors.HexColor('#566070');LINE=colors.HexColor('#c9d0d9');ACC=colors.HexColor('#1d4ed8')
S=lambda name,**k:ParagraphStyle(name,**k)
body=S('body',fontName='Serif',fontSize=10.2,leading=14.6,textColor=INK,spaceAfter=7)
hdr=S('hdr',fontName='Sans',fontSize=9.4,leading=13,textColor=INK)
title=S('title',fontName='Sans-B',fontSize=13,leading=16,textColor=INK,spaceAfter=5)
small=S('small',fontName='Sans',fontSize=8.2,leading=11.2,textColor=MUTED,spaceAfter=3)
label=S('label',fontName='Mono',fontSize=7.2,leading=10,textColor=MUTED,spaceBefore=4)
sect=S('sect',fontName='Cond-B',fontSize=30,leading=34,textColor=INK,spaceAfter=10)
toc0=S('toc0',fontName='Sans-B',fontSize=11,leading=15,spaceBefore=10,textColor=INK)
toc1=S('toc1',fontName='Sans',fontSize=8.3,leading=11.3,leftIndent=10,textColor=INK)
intro=S('intro',fontName='Serif',fontSize=10.5,leading=15.5,textColor=INK,spaceAfter=9)
def clean(t):
    # DejaVu lacks emoji; keep text readable
    t=t.replace('\U0001fae1','[salute emoji]').replace('\U0001f642',':)')
    return ''.join(ch if ord(ch)<0x1F000 else '[emoji]' for ch in t)
def P(t,st): return Paragraph(escape(clean(t)).replace('\n','<br/>'),st)
class Doc(BaseDocTemplate):
    def __init__(self,fn):
        super().__init__(fn,pagesize=letter,leftMargin=1.05*inch,rightMargin=1.05*inch,topMargin=0.9*inch,bottomMargin=0.85*inch,title='Elon Emails',author='Compiled archive',subject='Publicly available Elon Musk emails')
        fr=Frame(self.leftMargin,self.bottomMargin,self.width,self.height,id='f',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate('main',frames=[fr],onPageEnd=self.deco)])
        self.section=''
    def deco(self,c,doc):
        c.saveState();c.setFont('Mono',7.5);c.setFillColor(MUTED)
        if doc.page>1:
            c.drawString(self.leftMargin,letter[1]-0.55*inch,'ELON EMAILS'+(('  /  '+self.section.upper()) if self.section else ''))
            c.drawRightString(letter[0]-self.rightMargin,0.5*inch,str(doc.page))
            c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(self.leftMargin,letter[1]-0.62*inch,letter[0]-self.rightMargin,letter[1]-0.62*inch)
        c.restoreState()
    def beforeDocument(self):
        self.section=''
    def afterFlowable(self,fl):
        if hasattr(fl,'_toc'):
            lvl,text,key=fl._toc
            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,lvl,closed=(lvl==0))
            self.notify('TOCEntry',(lvl,text,self.page,key))
            if lvl==0:self.section=text
ORDER=['Tesla','SpaceX','OpenAI','Twitter/X','xAI','SolarCity','Neuralink','Personal']
BLURB={'Tesla':'Company-wide memos, board and investor correspondence, and trial exhibits.','SpaceX':'Memos to SpaceX staff and correspondence tied to the company.','OpenAI':'The founding-era and breakup correspondence, mostly from exhibits in Musk v. OpenAI. Includes replies from Altman, Sutskever, Brockman and others.','Twitter/X':'The offer letter, emails to staff after the takeover, and emails to reporters.','xAI':'Emails to xAI staff.','SolarCity':'Emails from the SolarCity acquisition litigation.','Neuralink':'Messages to Neuralink staff.','Personal':'Correspondence outside the companies: the Thai cave rescue and BuzzFeed emails from Unsworth v. Musk, and the 2012-2013 emails with Jeffrey Epstein released by the Department of Justice.'}
groups=collections.OrderedDict((c,[e for e in D if e['company']==c]) for c in ORDER)
assert sum(len(v) for v in groups.values())==len(D)
st=[]
st+=[Spacer(1,2.1*inch),Paragraph('Elon<font color="#1d4ed8">Emails</font>',S('cov',fontName='Cond-B',fontSize=64,leading=66,textColor=INK)),Spacer(1,14),
 P('Every publicly available Elon Musk email we could source, with the published text, dates, tags and sources.',S('cov2',fontName='Serif',fontSize=14,leading=20,textColor=INK)),Spacer(1,26)]
musk=sum(e['by_musk'] for e in D);full=sum(e['text_status']=='full' for e in D);words=sum(e['words'] for e in D)
st+=[P(f"{len(D)} emails  ·  {musk} written by Musk  ·  {full} with full text  ·  {words:,} words  ·  {min(e['year'] for e in D)}–{max(e['year'] for e in D)}",S('cov3',fontName='Mono',fontSize=9,leading=13,textColor=MUTED)),Spacer(1,6),
 P('Compiled October 3, 2026. An unofficial, independent compilation, not affiliated with Elon Musk or any of his companies.',S('cov4',fontName='Sans',fontSize=9,leading=13,textColor=MUTED)),PageBreak()]
h=Paragraph('How to read this archive',sect);st.append(h)
for t in ["Each entry reproduces an email as it was published by the source linked beneath it: a court exhibit, a news outlet that obtained the email, a government release, or Musk himself. Nothing has been reconstructed or filled in.",
 "Every entry is marked Full text, Partial text or Excerpt. Partial means the source printed most of the email or several passages; a bracketed ellipsis [...] marks a gap. Excerpt means only a line or two was ever made public. Two entries have no published text at all and carry only a summary.",
 "Entries are grouped by company and run in date order. Replies from other people are included where they belong to a published thread, so exchanges can be read in sequence. The sender is always shown.",
 "Most text was transcribed from web pages and court PDFs by automated retrieval. Wording was checked against a second source where one existed, but small differences in punctuation or line breaks from the originals are possible. For anything you intend to quote, follow the source link.",
 "The 'How it became public' line records provenance (court record, leak, government release and so on) and how firmly the email is attributed. Entries whose authenticity is disputed say so in their notes."]:
    st.append(P(t,intro))
st.append(PageBreak())
st.append(Paragraph('Contents',sect))
toc=TableOfContents();toc.levelStyles=[toc0,toc1];toc.dotsMinLevel=1;st+=[toc,PageBreak()]
STT={'full':'Full text','partial':'Partial text','excerpt':'Excerpt','none':'No text published'}
n=0
for comp,es in groups.items():
    if not es:continue
    hp=Paragraph(escape(comp),sect);hp._toc=(0,f'{comp} ({len(es)})','sec%d'%ORDER.index(comp))
    st+=[hp,P(BLURB[comp],intro),P(f"{len(es)} emails, {es[0]['date_display']} to {es[-1]['date_display']}",small),Spacer(1,10)]
    for e in es:
        n+=1
        t=Paragraph(escape(clean(e['title'])),title);t._toc=(1,f"{e['date_display']}  –  {e['title']}",'e%d'%n)
        hl=[f"<b>From:</b> {escape(clean(e['sender_full']))}",f"<b>Date:</b> {escape(e['date_display'])}"+(f" <font color='#566070'>({escape(clean(e['date_note']))})</font>" if e['date_note'] else ''),f"<b>To:</b> {escape(clean(e['to']))}"]
        if e['subject']:hl.append(f"<b>Subject:</b> {escape(clean(e['subject']))}")
        head=[CondPageBreak(1.6*inch),HRFlowable(width='100%',thickness=1.2,color=INK,spaceAfter=6),t,Paragraph('<br/>'.join(hl),hdr),
              P(f"{STT[e['text_status']].upper()}  ·  {e['category'].upper()}  ·  {e['provenance'].upper()}  ·  {e['confidence'].upper()}",label),Spacer(1,7)]
        paras=[p for p in re.split(r'\n\s*\n',e['text']) if p.strip()]
        fl=[P(p.strip(),body) for p in paras]
        if not fl:fl=[P('No verbatim text of this email has been published.',S('nt',parent=body,fontName='Sans-I',textColor=MUTED))]
        st.append(KeepTogether(head+fl[:1]));st+=fl[1:]
        tail=[Spacer(1,2),P('About this email: '+e['summary'],small)]
        if e['notes']:tail.append(P('Notes: '+e['notes'],small))
        srcs=[(e['source_name'],e['source_url'])]+[(m['name'],m['url']) for m in e['more_sources']]
        tail.append(Paragraph('Sources: '+'; '.join(f'<a href="{escape(u)}" color="#1d4ed8">{escape(clean(nm or u))}</a>' for nm,u in srcs),small))
        tail.append(P('Tags: '+', '.join(e['tags']),small));tail.append(Spacer(1,14))
        st+=tail
    st.append(PageBreak())
doc=Doc('out/elon-mails.pdf');doc.multiBuild(st)
print('pages',doc.page)
