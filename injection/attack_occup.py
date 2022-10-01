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
    cmd = '''rostopic pub --once /semantics/costmap_generator/occupancy_grid nav_msgs/OccupancyGrid "{'data':['''
    for i in range(10):
        cmd += str(100) + ','
    cmd += str(100) + ']}"'
    os.system(cmd)
if __name__ == '__main__':
    main()