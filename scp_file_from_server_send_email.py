#!/usr/bin/env python
#This Script will scp to access vm's and get the analyzer_ntc.log files from each server and rename the files to access-{ntc name}.log, 
#using this file script will do the html formatting to add color and bold related changes to email reporting, 
#it will consolidate all the report together and send email to DL-BSA@att.com.

import subprocess
import pipes
import os, yaml
import socket
import fcntl
import struct
import time, re, argparse, smtplib
from datetime import datetime,timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

config = {
            'subject_line' : 'BSA error log report',
         }
errored_servers = []
servers_list = []
location_list = []
loc_details = {}
formatted_line_list = []
sender_email = ''
html_str = '<span style="color:blue">{}</span> <span style="color:green">{}</span> '
html_str_hdr = '<span style="color:blue">{}</span> : <span style="color:green">{}</span> : <span style="color:green">{}</span> '
html_str_tme = '<span style="color:black">{}</span>'
html_str_fat = '<span style="color:red">{}</span>'
html_str_summary = '<span style="color:blue">{}</span>  <span style="color:green">{}</span>'
html_str_bold = "<strong>{}</strong>"

def get_ip_address(ifname):
    """ Logice to identify the active access node where your Cron job should run."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      return(socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
      )[20:24]))
    except IOError:
      pass

class HtmlFormatter(object):
    """ In HtmlFormatter class it will get the color details from www.w3.org website, for this script we would be using blue, green, red colors """
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
        
def send_email(body,recvrs):
    """ In send_email we would get the receivers information from yaml file, we will configure subject line and sender email in the script
    It will format the summary based on location, server and no.of error count. It will add the ssh error log info and followed by detailed log messages """
    with open ('/etc/postfix/sender_canonical_maps', "r") as myfile:
        data=myfile.readlines()
        for line in data:
           if '/^bsa@.+/' in line:
               sender_email = line.strip('/^bsa@.+/').strip()
    subject_line = config['subject_line']
    sender = sender_email
    receivers = recvrs
    if isinstance(receivers, list):
        receivers = ', '.join(receivers)
    
    body.write_line(html_str_bold.format("SUMMARY" ))

    location_list.sort()
    print(loc_details)
    def get_html_count(sname,loc):
        nvms = 0
        ecnt = 0
        print(sname,loc)
        error_count = loc_details[loc]['error']
        for item  in error_count.keys():
            if sname in item:
                nvms += 1
                ecnt += error_count[item]
        return "{} ({} VMs) : {}".format(sname,nvms,ecnt)
    snames = []
    for server_name in servers_list:
        #print(server_name)
        sname = {}
        sname['server'] =  server_name.split('-')[0][:-1]
        sname['loc'] = server_name.split('-')[1]
        snames.append(sname)

    added = []
    flag = False
    for location in location_list:
        loc = location
        flag = False
        added = []
        for sname in snames:
            print(sname['loc'],location)
            if sname['server'] not in added and sname['loc'] in location:
                print(sname,location)
                ftd_line = html_str_summary.format(loc+':',get_html_count(sname['server'],location))
                body.write_line(ftd_line)
                flag = True
                if flag :
                    loc = "&nbsp;&nbsp;&nbsp;&nbsp;"
                added.append(sname['server'])
        body.write_line('<br>')
    body.write_line("<br>")
    if (len(errored_servers)) > 0:
        body.write_line(html_str_fat.format('SSH connection failed VM count:' + str(len(errored_servers))))
        body.write_line("<br>")
    
    body.write_line(html_str_bold.format("DETAILS" ))    
    for fmtd_line in formatted_line_list:           
        body.write_line(fmtd_line + '\n')
        
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject_line
    msg['From'] = sender
    msg['To'] = receivers
    msg.attach( MIMEText(str(body), 'html') )
    smtp_host = 'localhost'
    s = smtplib.SMTP(smtp_host)
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()

def copy_file(USER = 'bsa',SERVER = '',PATH = '',FILE = ''):
    """ copy_file will pull path info from default path, server details from yaml file and 
    saves the file where this current script runs"""

    RURL = "{}@{}:{}".format(USER,SERVER,PATH)
    resp = subprocess.Popen(["scp","-o","StrictHostKeyChecking=no",RURL, FILE],
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    result, err = resp.communicate()
    if resp.returncode != 0:
        formatted_line_list.append(SERVER + ': No file Found' )

def process_file(filename = 'analyzer_ntc.log', hostname= ''):error_count = {}
    """In process_file it will format the summary for location, server and error count and add logic for color
    and add color and bold logic to detailed error log""" 
    error_count = {}
    formatted_line_list.append('<br>' )
    with open(filename,"r") as inputfile:
        location_list.append(hostname)
        print(hostname)
        for line in inputfile:
            if len(line) != 1:
                llist = line.strip().split()
                for item in llist:
                    if 'mspfwd.py' in item: llist.remove(item)
                if 'ERROR' in llist[0]:
                    formatted_line = html_str_fat.format(line)
                    errored_servers.append(line.split()[7])
                else:
                    rest_line = '\t' + ' '.join(llist[6:len(llist)-1])
                    if 'FATAL' in rest_line:
                        rest_line = html_str_fat.format(rest_line)
                    formatted_line = html_str.format(llist[0], llist[1]) + '\t' + ' '.join(llist[2:5]) + rest_line + '\t' + html_str_bold.format(llist[-1])
                    if 'Script' in llist[0]:
                        formatted_line = html_str_tme.format(line)
                    if llist[0] not in servers_list and 'Script' not in llist[0]:
                        servers_list.append(llist[0])
                        error_count[llist[0]] = int(llist[-1].split(":")[-1])
                    elif 'Script' not in llist[0]:
                        error_count[llist[0]] += int(llist[-1].split(":")[-1])
                formatted_line_list.append(formatted_line )
    loc_details[hostname] = {}
    loc_details[hostname]['error'] = error_count
    
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--yamlfile", required=True, help="yaml file input")
    ap.add_argument("-l", "--logfilepath", required=False, help="log file",
                    default="/opt/bsa/bin/analyzer_ntc.log")
    args = vars(ap.parse_args())
    """ In main it will open the yaml file and gather server details and uses default path and 
    pull the log_analyser.log file and does the html fomatting and send an email """
    body = HtmlFormatter()
    zone = time.tzname[0]
    today = datetime.now().date()
    Previous_Date = (today - timedelta(1)).strftime("%m-%d-%Y 03:00 %p") + ' ' + zone

    ip = get_ip_address('eth0:1')
    if ip is not None:
        with open ('/opt/bsa/bin/analyzer_ntc.log', "r") as myfile:
            data=myfile.readlines()
            for line in data:
                llist = line.strip().split()
                if 'Script' in llist:
                    output = (llist[3], llist[4].strip(":")[:-3], llist[5], llist[6])
                    cron_start = ' '.join(output)

        body.write_line( 'BSA Log analysis report for period: ' + Previous_Date + ' ' + 'to' + ' ' + cron_start)

        with open(args['yamlfile'], "r") as stream:
            try:
                data = yaml.safe_load(stream)
                for item in data:
                    if 'input1' == item:
                        for i in data[item]:
                            local_file_name = "./{}.log".format(i['host'])
                            remote_file_name = args['logfilepath']
                            if os.path.isfile(local_file_name):
                               os.remove(local_file_name)
                            copy_file(SERVER=i['host'],PATH = remote_file_name ,FILE =local_file_name)
                            if os.path.isfile(local_file_name):
                                process_file(local_file_name, i['host'].split('-')[1])
            except yaml.YAMLError as exc:
                print(exc)
            send_email(body,data['receivers'])
