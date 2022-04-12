import subprocess
import os, yaml
import time, re, argparse, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytz
from datetime import datetime

config = {
            'subject_line' : 'Test',
            'sender' : ''
            'receivers' : ''
         }
errored_servers = []
servers_list = []
location_list = []
error_count = {}
formatted_line_list = []
html_str = '<span style="color:blue">{}</span> <span style="color:green">{}</span> '
html_str_hdr = '<span style="color:blue">{}</span> : <span style="color:green">{}</span> : <span style="color:green">{}</span> '
html_str_err = '<span style="color:yellow">{}</span>'
html_str_fat = '<span style="color:red">{}</span>'

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
        

def send_email(body):
    subject_line = config['subject_line'].format(loc.upper())
    sender = config['sender']
    receivers = config['receivers']
    if isinstance(receivers, list):
        receivers = ', '.join(receivers)
    
    body.write_line("SUMMARY" )
    
    for location in location_list:
    for server in servers_list:
        ftd_line = html_str_hdr.format(location,server,str(error_count[server]))
        body.write_line(ftd_line + '\n')
    body.write_line(html_str_err.format('Connect_failed_list_servers:' + ','.join(errored_servers)))
    
    body.write_line("DETAILS" )
    
    for fmtd_line in formatted_line_list:           
        body.write_line(fmtd_line + '\n')
        
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject_line
    msg['From'] = sender
    msg['To'] = receivers
    msg.attach( MIMEText(str(body), 'html') )
    smtp_host = 'localhost'
    s = smtplib.SMTP(smtp_host)
    s.sendmail(sender, config['receivers'], msg.as_string())
    s.quit()

def copy_file(USER = 'bsa',SERVER = '',PATH = '',FILE = ''):
    RURL = "{}@{}:{}".format(USER,SERVER,PATH)
    resp = subprocess.Popen(["scp",RURL, FILE],
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    result, err = resp.communicate()

def process_file(filename = 'gen_file.log'):
    with open(filename,"r") as inputfile:
        location_list.append(filename.split('.')[0])
        for line in inputfile:
            if len(line) != 1:
                llist = line.strip().split()
                if 'ERROR' in llist[0]:
                    formatted_line = html_str_err.format(line)
                    errored_servers.append(line.split()[7])
                else:
                    rest_line = ' '.join(llist[2:])
                    if 'ERROR' in rest_line:
                        rest_line = html_str_err.format(rest_line)
                    elif 'FATAL' in rest_line:
                        rest_line = html_str_fat.format(rest_line)
                    formatted_line = html_str.format(llist[0], llist[1]) + rest_line
                    if llist[0] not in servers_list :
                        servers_list.append(llist[0])
                        error_count[llist[0]] = 1
                    else:
                        error_count[llist[0]] += 1
                formatted_line_list.append(formatted_line )

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--yamlfile", required=True, help="yaml file input")
    ap.add_argument("-l", "--logfilepath", required=False, help="log file",
                    default="/opt/bin/gen_file.txt")
    args = vars(ap.parse_args())
    body = HtmlFormatter()
    body.write_line( 'Report of Log Analysis')
    with open(args['yamlfile'], "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for item in data:
                if 'email' in item:break
                for i in data[item]:
                    local_file_name = "./{}.log".format(i['host'])
                    remote_file_name = args['logfilepath']
                    copy_file(SERVER=i['host'],PATH = remote_file_name ,FILE =local_file_name)
                    if os.path.isfile(local_file_name):
                        process_file(local_file_name)
        except yaml.YAMLError as exc:
            print(exc)
        send_email(body,data['receivers'])
