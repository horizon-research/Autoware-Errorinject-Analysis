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
    base = 'baseline'
    for i in range(30):
        cmd = 'zip -r ' + base + str(i) + '.zip ' + base + str(i)
        os.system(cmd)
        cmd = 'rm -r ' + base + str(i)
if __name__ == '__main__':
    main()