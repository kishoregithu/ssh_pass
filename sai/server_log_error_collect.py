#!/usr/bin/env python
#Script neeeds an input file loganalyzer.yaml which has server details and string pattern
#It will ssh to various servers and search for string pattern provided in the yaml file
#default path location: /var/log/mspfwd.log, /var/log/messages
#command to run the script /opt/bsa/bin/loganalyzer.py -f /opt/bsa/lib/loganalyzer.yaml
#If user need to change the path location they need to pass "-l path location"
#change of path command: /opt/bsa/bin/loganalyzer.py -f /opt/bsa/lib/loganalyzer.yaml -l "path"
#Script will capture one occurance of search pattern in the log file and it also calculate
#number of times log pattern is repeated in the log. Once the details are collected it will
#send email to the distibution list.

import subprocess
import argparse
import logging
import yaml
import sys
import socket
import fcntl
import struct

logging.basicConfig(filename='/opt/bsa/log/log_analyzer.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

EMAIL_STR = ''
Email = ''

class Error(Exception):
    """Base class for other exceptions"""
    pass

class SSHCommandExecError(Error):
    """Raised when the Command Execution Fails over SSH"""
    pass

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

class runServerCmd:
    """ In runServerCmd class host name will be captured from yaml file
    and it will ssh to the hosts and search for the string in /var/log/mspfwd.log, /var/log/messages file,
    if user doesnot have access to any host it will log the information to log file and
    send the error details to email specified in the yaml file."""

    def __init__(self, host):
        self.host = host

    def exec_cmd(self, cmd):
        resp = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no", "root@%s" % self.host, cmd],
                         shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        result, err = resp.communicate()
        if err and 'warning' not in err:
            global EMAIL_STR
            LOG = "ERROR LOG: " + err.replace('\r', '') + '\n'
            if ((len(str(LOG).strip())) > 25):
                EMAIL_STR += LOG
            logging.error(err)
            raise SSHCommandExecError
        return result


class serverlogCollect:
    """In this class it will execute series of commands, one to capture the error string and
    other to count the number of occurances in the log file.
    Once we receive these information it will send those details to body of an email specified in the yaml file
    @attribute host - Server we connect to
    @attribute outfile - Yaml file, it has host, string and email details
    @attribute string - string pattern which is used while performing grep command
    @attribute email - list of users to receive email"""

    def __init__(self, host, string, email, sdir, outfile):
        self.host = host
        self.outfile = outfile
        self.sdir = sdir
        self.string = string
        self.email = email
        self.runcommand = runServerCmd(self.host)
        self.result = {}
        global Email
        Email =  ",".join(self.email)

    def run(self):
        try:
            self.runcommand.exec_cmd('ls')
        except SSHCommandExecError:
            return
        global EMAIL_STR
        global LOG
        resp = ' '
        if ',' in self.sdir:
            logs = self.sdir.split(',')
            for item in logs:
                cmd = " grep -m1 " + '"' + self.string + '"' + " " + item
                resp1=self.runcommand.exec_cmd(cmd).strip()
                if resp1:
                    resp += self.host + '\t' + item + '\t ' + resp1
                    cmd = "grep -i " + '"' +  self.string + '"' +  " " + item + "| wc -l"
                    resp += '\t' + '"Count:"' + self.runcommand.exec_cmd(cmd)
                    resp += '\n'
        else:
            cmd = " grep -m1 " + '"' + self.string + '"' + " " + self.sdir
            resp1=self.runcommand.exec_cmd(cmd)
            if resp1:
                resp += self.host + '\t' + self.sdir + '\t' + resp1
                cmd = "grep -i " + '"' +  self.string + '"' +  " " + self.sdir + "| wc -l"
                resp += '\t' + '"Count:"' + self.runcommand.exec_cmd(cmd)
            resp += '\n'
        if resp and ((len(str(resp).strip())) > 72):
            EMAIL_STR += resp
              
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--yamlfile", required=True, help="yaml file input")
    ap.add_argument("-l", "--logfilepath", required=False, help="log file",
                    default="/var/log/mspfwd.log,/var/log/messages")
    args = vars(ap.parse_args())
    """ serverlogcollect needs yaml file as argument.
    we have a default logpath set to "/var/log/mspfwd.log,/var/log/message". If user want to change the location we can use     -l as argument while running.
    It will pull host, string and email details from yaml file as input and it will ssh to host and pull error log     information.
    If we receive any String error log or ssh connection log, we will send and email to users specifeid in the yaml file."""
    with open(args['yamlfile'], "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for item in data:
                if 'email' in item:break
                for i in data[item]:
                    slc = serverlogCollect(i['host'], i['string'], data['email'], args['logfilepath'], args['yamlfile'])
                    ip = get_ip_address('eth0:1')
                    if ip is not None:
                        slc.run()
        except yaml.YAMLError as exc:
            print(exc)
    with open('/opt/bsa/bin/log_analyser.log','w') as lg_file:
        global EMAIL_STR
        lg_file.write(EMAIL_STR)
