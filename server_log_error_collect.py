#!/usr/bin/env python3
import subprocess
import csv
import argparse
import logging
import yaml
logging.basicConfig(filename='server_data_collect.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

EMAIL_STR = ''

class Error(Exception):
    """Base class for other exceptions"""
    pass

class SSHCommandExecError(Error):
    """Raised when the Command Execution Fails over SSH"""
    pass

class runServerCmd:
    def __init__(self, host):
        self.host = host
        
    def exec_cmd(self, cmd):
        resp = subprocess.Popen(["ssh", "%s" % self.host, cmd], 
                         shell=False, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        result, err = resp.communicate()
        if err and 'Warning' not in err.decode('utf-8'):
            logging.info(err.decode('utf-8'))
            raise SSHCommandExecError
        return result.decode('utf-8')

class serverlogCollect:
    def __init__(self, host, string, sdir, outfile):
        self.host = host
        self.outfile = outfile
        self.sdir = sdir
        self.string = string
        self.runcommand = runServerCmd(self.host)
        self.result = {}
        
    def run(self):
        try:
            self.runcommand.exec_cmd('ls')
        except SSHCommandExecError:
            return
        # command to grep 
        # command to grep 
        cmd = "grep -m1 " + self.string + " " + self.sdir 
        resp += ' ' + self.runcommand.exec_cmd(cmd) 
        self.result["Log"] = resp 
        cmd = "grep " + self.string + " " + self.sdir + "| wc -l" 
        resp += ' ' + self.runcommand.exec_cmd(cmd) 
        self.result["Count"] = resp
        if resp:
            EMAIL_STR += resp + '\n'
        
        
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-y", "--yamlfile", required=True, help="yaml file input")
    ap.add_argument("-o", "--outputfile", required=True, help="output file")
    ap.add_argument("-l", "--logfilepath", required=True, help="log file", default="/var/log/mspfwd.log")
    args = vars(ap.parse_args())
            
    #print(args['servers'], args['username'])
    with open(args['yamlfile'], "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for item in data:
                for i in data[item]:
                    slc = serverlogCollect(i['host'], i['string'], args['logfilepath'],args['yamlfile'])
                    slc.run()
        except yaml.YAMLError as exc:
            print(exc)
            
    cmd="""echo """+ EMAIL_STR +"""  | mailx -s 'Error Detail' sk3798@att.com""" 
    p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) 
    output, errors = p.communicate()
    
    #print(host_list)
    
