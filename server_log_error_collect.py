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
        if err:
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
        cmd = "grep " + self.string + " " + self.sdir
        resp = ' ' + self.runcommand.exec_cmd(cmd)
        if resp:
            with open(self.outfile, 'a') as outfile:
                outfile.write(self.host)
                outfile.write(resp)
        
        
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-y", "--yamlfile", required=True, help="yaml file input")
    ap.add_argument("-o", "--outputfile", required=True, help="output file")
    args = vars(ap.parse_args())
            
    #print(args['servers'], args['username'])
    with open(args['yamlfile'], "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for item in data:
                for i in data[item]:
                    slc = serverlogCollect(i['host'], i['string'], i['dir'],args['yamlfile'])
                    slc.run()
        except yaml.YAMLError as exc:
            print(exc)
    
    
    #print(host_list)
    
