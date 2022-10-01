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
    a = open('occupanc_grid.txt')
    f = a.readlines()
    point = []
    for i in f:
        if 'data' in i:
            s = i[7:-2].split(",")
            for p in s:
                point.append(int(p))
            pdb.set_trace()

if __name__ == '__main__':
    main()