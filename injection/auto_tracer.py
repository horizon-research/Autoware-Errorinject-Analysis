import os
import pdb
import time
import random
import rosnode
import rosgraph
import sys
import argparse
try:
    from xmlrpc.client import ServerProxy
except ImportError:
    from xmlrpclib import ServerProxy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ROS_MASTER_URI', type=str, nargs='?', metavar='URI', help='ROS master URI to use.')
    args = parser.parse_args()
    previsou_pid = 0

    while(1):
        f = open('pidckpt','r')
        a = f.readlines()
        f.close()
        if len(a) == 0:
            continue
        pid = int(a[0])
        if pid == -1:
            return
        else:
            if pid == previsou_pid:
                time.sleep(0.2)
            else:    
                cmd = '''rosnode info /can_odometry 2>/dev/null | grep Pid| cut -d ' ' -f2 > realpid'''
                os.system(cmd)
                time.sleep(0.1)
                fn = open('realpid','r')
                b = fn.readlines()
                realpid = int(b[0])
                cmd = 'sudo ./Tracer '+str(realpid) + ' ' + str(random.randint(0,5)) + ' ' + str(random.randint(0,32))
                os.system(cmd)
                previsou_pid = pid
if __name__ == '__main__':
    main()
