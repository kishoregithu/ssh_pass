#!/usr/bin/env python3
import subprocess
import csv
import argparse

field_names = ['SERVER','APPID','CRONJOB','RPM']

class runServerCmd:
    
    def __init__(self, host, user):
        self.host = host
        self.user = user
        
    def exec_cmd(self, cmd):
        resp = subprocess.Popen(["ssh", "%s" % self.host, cmd], 
                         shell=False, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        result = resp.stdout.readlines() 
        return result
    
    def exec_cmd2(self, cmd):
        import os
        os.system('%s > tmp'%cmd)
        result = open('tmp', 'r').read()
        return result

class serverDataCollect:
    def __init__(self, username, hostname):
        self.hostname = hostname
        self.username = username
        self.runcommand = runServerCmd(self.hostname,self.username)
        self.result = {}
        
    def run(self):
        apps = ["tini","tini"]
        self.result["SERVER"] = self.hostname
        
        #check process on appid 
        self.result["APPID"] = ''
        for app in apps:
            cmd = "ps -ef | grep " + app + " | awk '{print $2}'"
            resp = ' ' + self.runcommand.exec_cmd(cmd)
            print(cmd, resp.split('\n')[0])
            self.result["APPID"] += resp.split('\n')[0]
        #check crontab
        self.result["CRONJOB"] = ''
        for app in apps:
            cmd = "crontab -u " + app + " -l"
            self.result["CRONJOB"] += ' ' + self.runcommand.exec_cmd(cmd)
        # run listing rpm packages
        cmd = "rpm -qa"
        self.result["RPM"] = self.runcommand.exec_cmd(cmd)
        print(self.result)
        
        with open('event.csv', 'a') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(self.result)
            f_object.close()
        
        
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--servers", required=True, help="Server list file")
    ap.add_argument("-u", "--username", required=True, help="name of user")
    args = vars(ap.parse_args())
    
    with open('event.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(field_names)
        f.close()
            
    #print(args['servers'], args['username'])
    host_list = []
    with open(args['servers']) as slf:
        while True:
            line = slf.readline()
            if not line:
                break
            host_list.append(line.strip())
    
    for host in host_list:
        sdc = serverDataCollect(args['username'],host)
        sdc.run()
    #print(host_list)
    
