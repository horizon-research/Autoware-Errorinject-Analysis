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
    a = open('pt_nogd.txt')
    f = a.readlines()
    point = []
    t = 0
    for i in f:
        if 'data:' in i:
            #pdb.set_trace()
            s = i[7:-2].split(",")
            for p in s:
                point.append(int(p))
            print(len(point))
            t += 1
        point = []
            

    print('numbers',t)

if __name__ == '__main__':
    main()
