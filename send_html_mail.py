import time, re, argparse, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytz
from datetime import datetime

config = {
            'subject_line' : 'Test',
            'sender' : '',
            'receivers' : ''
         }
period_end = time.time()
period_start = time.time()
alertlist = ['','']

class HtmlFormatter(object):
    def __init__(self):
        self.data = [ ]
        self.start = '''\
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns:m="http://schemas.microsoft.com/office/2004/12/omml" xmlns="http://www.w3.org/TR/REC-html40"><head><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=us-ascii"><meta name=Generator content="Microsoft Word 14 (filtered medium)"><style><!--
/* Font Definitions */
@font-face
        {font-family:Calibri;
        panose-1:2 15 5 2 2 2 4 3 2 4;}
@font-face
        {font-family:Consolas;
        panose-1:2 11 6 9 2 2 4 3 2 4;}
/* Style Definitions */
p.MsoNormal, li.MsoNormal, div.MsoNormal
        {margin:0in;
        margin-bottom:.0001pt;
        font-size:11.0pt;
        font-family:"Calibri","sans-serif";}
a:link, span.MsoHyperlink
        {mso-style-priority:99;
        color:blue;
        text-decoration:underline;}
a:visited, span.MsoHyperlinkFollowed
        {mso-style-priority:99;
        color:purple;
        text-decoration:underline;}
p.MsoPlainText, li.MsoPlainText, div.MsoPlainText
        {mso-style-priority:99;
        mso-style-link:"Plain Text Char";
        margin:0in;
        margin-bottom:.0001pt;
        font-size:11.0pt;
        font-family:"Calibri","sans-serif";}
span.PlainTextChar
        {mso-style-name:"Plain Text Char";
        mso-style-priority:99;
        mso-style-link:"Plain Text";
        font-family:"Calibri","sans-serif";}
.MsoChpDefault
        {mso-style-type:export-only;
        font-family:"Calibri","sans-serif";}
@page WordSection1
        {size:8.5in 11.0in;
        margin:1.0in 1.0in 1.0in 1.0in;}
div.WordSection1
        {page:WordSection1;}
--></style><!--[if gte mso 9]><xml>
<o:shapedefaults v:ext="edit" spidmax="1026" />
</xml><![endif]--><!--[if gte mso 9]><xml>
<o:shapelayout v:ext="edit">
<o:idmap v:ext="edit" data="1" />
</o:shapelayout></xml><![endif]--></head>
<body lang=EN-US link=blue vlink=purple><div class=WordSection1>
'''
        self.replacements = [
            ( re.compile(r'\*\*\*(.*?)\*\*\*'),
              r'''<b><span style='color:blue'>\1</span></b>''' ),
            ( re.compile(r'\*\*(.*?)\*\*'),
              r'''<b><span style='color:red'>\1</span></b>''' ),
            ( re.compile(r'\*(.*?)\*'),
              r'''<b>\1</b>''' ),
            ( re.compile(r'<p>'),
              r'''<p class=MsoPlainText>'''),
            ( re.compile(r'</p>'),
              r'''<o:p></o:p></p>''')
            ]
        self.end = '</div></body></html>\n'
    def __str__(self):
        return ''.join([self.start]+self.data+[self.end])
    def write(self, datum):
        for pattern, repl in self.replacements:
            datum = pattern.sub(repl, datum)
        self.data.append(datum)
    def write_line(self, line=''):
        self.write('<p>%s</p>\n' % line)
    def start_dl(self):
        'start Definition List'
        self.write('<DL>\n')
    def write_udl(self, text):
        'write un-indented Definition List line'
        self.write('<DT>%s\n' % text)
    def write_idl(self, text):
        'write indented Definition List line'
        self.write('<DD>%s\n' % text)
    def end_dl(self):
        'end Definition List'
        self.write('</DL>\n')
        

def send_email(loc,config, period_start, period_end, alertlist):
    subject_line = config['subject_line'].format(loc.upper())
    sender = config['sender']
    receivers = config['receivers']
    if isinstance(receivers, list):
        receivers = ', '.join(receivers)

    body = HtmlFormatter()
    body.write_line("Test")
    
    local_tz =  pytz.timezone('America/New_York')
    dt = datetime.fromtimestamp(period_start, local_tz)
    period_start_text = dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    dt = datetime.fromtimestamp(period_end, local_tz)
    period_end_text = dt.strftime('%Y-%m-%d %H:%M:%S %Z')

    body.write_line( 'Report Period *%s* - *%s*' % ( period_start_text, period_end_text))

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject_line
    msg['From'] = sender
    msg['To'] = receivers
    msg.attach( MIMEText(str(body), 'html') )
    smtp_host = 'localhost'
    s = smtplib.SMTP(smtp_host)
    s.sendmail(sender, config['receivers'], msg.as_string())
    s.quit()
    
send_email('abc',config, period_start, period_end, alertlist)
