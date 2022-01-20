import paramiko
import sys
import ssh_lib
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

class TestStringMethods(unittest.TestCase):
    def test_snd_cmd(self):
        
        paramiko.SSHClient.set_missing_host_key_policy =  MagicMock(return_value=True)
        paramiko.SSHClient.connect = MagicMock()
        paramiko.SSHClient.invoke_shell = MagicMock()
        paramiko.SSHClient.exec_command =  MagicMock(return_value=[sys.stdin,sys.stdout,sys.stderr])
        paramiko.SSHClient.get_transport =  MagicMock()
        sshc = ssh_lib.SSHsession()
        sshc._read_stdout = MagicMock(return_value='1')
        self.assertEqual(sshc.send_cmd('ls'),'1')
    
    def test_snd_cmd_except(self):
        
        paramiko.SSHClient.set_missing_host_key_policy =  MagicMock(return_value=True)
        paramiko.SSHClient.connect = MagicMock()
        paramiko.SSHClient.invoke_shell = MagicMock()
        paramiko.SSHClient.exec_command =  MagicMock(return_value=[sys.stdin,sys.stdout,sys.stderr])
        paramiko.SSHClient.exec_command.side_effect = paramiko.SSHException
        paramiko.SSHClient.get_transport =  MagicMock()
        sshc = ssh_lib.SSHsession()
        sshc._read_stdout = MagicMock(return_value='1')
        self.assertEqual(sshc.send_cmd('ls'), None)
