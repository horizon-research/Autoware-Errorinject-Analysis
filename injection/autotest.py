import os
import os
import time
import signal
import subprocess
import pdb
import numpy as np
import argparse

def main():
    t = [24.0]
    var = ['xr','yl','yr','zl','zr']
    for x in var:
        for i in range(10):
            cmd = 'python inject_tc.py --signal %s --delta %f --time %f' % (x, i*(0.3),24.0)
            os.system(cmd)
            time.sleep(10)
            
if __name__ == '__main__':
    main()

