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

data = dict(
    hostname = '',
    error_data = dict(
        host = '',
        folder = '',
        pattern = '',
    )
)

def populate_dict(hostname="nap", host= "mspfwd1", folder="/tmp", pattern="abc"):
    temp = data
    temp['hostname'] = hostname
    temp['error_data']["host"] = host
    temp['error_data']["folder"] = folder
    temp['error_data']["pattern"] = pattern
    return temp



LOGPATH = "/var/log/temp"
PATTERN = "ERROR"

class Error(Exception):
    """Base class for other exceptions"""
    pass

class SSHCommandExecError(Error):
    """Raised when the Command Execution Fails over SSH"""
    pass


class runServerCmd:
    
    def __init__(self, host, user):
        self.host = host
        self.user = user
        
    def exec_cmd(self, cmd):
        resp = subprocess.Popen(["ssh", "%s" % self.host, cmd], 
                         shell=False, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        result, err = resp.communicate()
        if err:
            logging.info(err.decode('utf-8'))
            raise SSHCommandExecError
        return result.decode('utf-8')

class serverlogCollect:
    def __init__(self, username, hostname, errfile ):
        self.hostname = hostname
        self.username = username
        self.errorfile = errfile
        self.runcommand = runServerCmd(self.hostname,self.username)
        self.result = {}
        
    def run(self):
        try:
            self.runcommand.exec_cmd('ls')
        except SSHCommandExecError:
            return
        # command to grep 
        cmd = "cat "+ LOGPATH +  " | grep " + PATTERN
        resp = ' ' + self.runcommand.exec_cmd(cmd)
        if resp:
            data = populate_dict("",self.hostname, LOGPATH, PATTERN)
            with open(self.errorfile, 'a') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)
        
        
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--servers", required=True, help="Server list file")
    ap.add_argument("-u", "--username", required=True, help="name of user")
    ap.add_argument("-y", "--errorfile", required=True, help="yaml filr for save log")
    args = vars(ap.parse_args())
            
    #print(args['servers'], args['username'])
    host_list = []
    with open(args['servers']) as slf:
        while True:
            line = slf.readline()
            if not line:
                break
            host_list.append(line.strip())
    
    for host in host_list:
        sdc = serverlogCollect(args['username'],host,args['errorfile'])
        sdc.run()
    #print(host_list)
    
