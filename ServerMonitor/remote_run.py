'''
Created on Nov 7, 2014

@author: kefengwei
'''
import paramiko
import sys
paramiko.util.log_to_file('demo_simple.log')
#pk_file = '/home/kefengwei/.ssh/id_rsa'
pk_file = 'E:\id_rsa'
password = '12345Abc'

class Batch(object):
    def __init__(self, host, port=22, user='root'):
        self.host = host
        self.key = paramiko.RSAKey.from_private_key_file(pk_file)
        self.port = port
        self.user = user
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "Try to connect %s" % self.host
        self.client.connect(self.host, self.port, self.user, pkey=self.key,compress=True)
        print "Connected %s , command will exec!!" % self.host

    def run(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        result = stdout.read()
        if result != '':
            return result
        else:
            return 'error', stderr.read()

    def close(self):
        self.client.close()


if __name__ == '__main__':
    host = sys.argv[1]
    cmd = sys.argv[2]
    batch = Batch(host)
    result = batch.run(cmd)
    print result