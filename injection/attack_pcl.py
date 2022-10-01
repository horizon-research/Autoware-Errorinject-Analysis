import pydot
import networkx
import pdb
import os
import time
import signal
import subprocess
import pdb
import numpy as np
import argparse

def main():
    cmd = '''rostopic pub -r 30 /points_no_ground sensor_msgs/PointCloud2 "{'data':['''
    for i in range(30000):
        cmd += str(100) + ','
    cmd += str(100) + ']}"'
    os.system(cmd)

if __name__ == '__main__':
    main()

