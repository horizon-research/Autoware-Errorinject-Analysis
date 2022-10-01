from struct import *
import signal
import subprocess
import pdb
import numpy as np
import argparse
import pickle
import gzip
import os
from os import walk

def parse_es_twist(filepath):

    xl = []
    yl = []
    zl = []
    xa = []
    ya = []
    za = []

    file = open(filepath,'r')
    a = file.readlines()

    for i in range(len(a)):
        if 'x:' in a[i]:
            if 'linear:' in a[i-1]:
                xl.append(float(a[i][7:-1]))
            elif 'angular:' in a[i-1]:
                xa.append(float(a[i][7:-1]))
        elif 'y:' in a[i]:
            if 'linear:' in a[i-2]:
                yl.append(float(a[i][7:-1]))
            elif 'angular:' in a[i-2]:
                ya.append(float(a[i][7:-1]))	
        elif 'z:' in a[i]:
            if 'linear:' in a[i-3]:
                zl.append(float(a[i][7:-1]))
            elif 'angular:' in a[i-3]:
                za.append(float(a[i][7:-1]))		

    return xl,yl,zl,xa,ya,za

def main():
    parser = argparse.ArgumentParser(description="base folder, save dir and database query")
    parser.add_argument('--base', default='vel_relay_attack_fpregis')
    parser.add_argument('--save', default='vel_relay.pkl')
    args = parser.parse_args()

    file = gzip.GzipFile(args.save, 'rb')
    data = pickle.load(file)
    file.close()
    pdb_xl = {}
    pdb_yl = {}
    pdb_zl = {}
    pdb_xa = {}
    pdb_ya = {}
    pdb_za = {}

    for i in range(len(data['xl'])):
        for j in range(180,204):
            #pdb.set_trace()
            tmp = round((data['xl'][i][j]),1)
            if tmp not in pdb_xl:
                pdb_xl[tmp] = 1
            else:
                pdb_xl[tmp] += 1
            tmp = round((data['yl'][i][j]),1)
            if tmp not in pdb_yl:
                pdb_yl[tmp] = 1
            else:
                pdb_yl[tmp] += 1
            tmp = round((data['zl'][i][j]),1)
            if tmp not in pdb_zl:
                pdb_zl[tmp] = 1
            else:
                pdb_zl[tmp] += 1
            tmp = round((data['xa'][i][j]),1)
            if tmp not in pdb_xa:
                pdb_xa[tmp] = 1
            else:
                pdb_xa[tmp] += 1
            tmp = round((data['ya'][i][j]),1)
            if tmp not in pdb_ya:
                pdb_ya[tmp] = 1
            else:
                pdb_ya[tmp] += 1
            tmp = round((data['za'][i][j]),1)
            if tmp not in pdb_za:
                pdb_za[tmp] = 1
            else:
                pdb_za[tmp] += 1

    pdb_xl = sorted(pdb_xl.keys())
    pdb_yl = sorted(pdb_yl.keys())
    pdb_zl = sorted(pdb_zl.keys())
    pdb_xa = sorted(pdb_xa.keys())
    pdb_ya = sorted(pdb_ya.keys())
    pdb_za = sorted(pdb_za.keys())

    f = []
    for (dirpath, dirnames, filenames) in walk('/localdisk/attack_autoware_regis/' + args.base):
        f.append(dirpath)
    #pdb.set_trace()
    frame = []
    xp_large = 0
    xp_min = 0
    yp_large = 0
    yp_min = 0
    zp_large = 0
    zp_min = 0
    xo_large = 0
    xo_min = 0
    yo_large = 0
    yo_min = 0
    zo_large = 0
    zo_min = 0

    file_name = []
    for i in range(1,len(f)):
        cmd = 'cp -r ' + f[i] + ' ./tmp/'
        #pdb.set_trace()
        os.system(cmd)
        xp,yp,zp,xo,yo,zo = parse_es_twist('tmp/current_velocity.txt')
        cmd = 'rm -r tmp'
        os.system(cmd)
        
        for j in range(len(xp)):
            if j >= 180 and j < 210:
                #pdb.set_trace()
                if xp[j] > pdb_xl[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (xp[j] - pdb_xl[-1]) > xp_large:
                        xp_large = xp[j] - pdb_xl[-1]
                if xp[j] < pdb_xl[0]:	
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_xl[0] - xp[j]) < xp_min:
                        xp_min = pdb_xl[0] - xp[j]
                if yp[j] > pdb_yl[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (yp[j] - pdb_yl[-1]) > yp_large:
                        yp_large = yp[j] - pdb_yl[-1]
                if yp[j] < pdb_yl[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_yl[0] - yp[j]) < yp_min:
                        yp_min = pdb_yl[0] - yp[j]
                if zp[j] > pdb_zl[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (zp[j] - pdb_zl[-1]) > zp_large:
                        zp_large = zp[j] - pdb_zl[-1]
                if zp[j] < pdb_zl[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_zl[0] - zp[j]) < zp_min:
                        zp_min = pdb_zl[0] - zp[j]
                if xo[j] > pdb_xa[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (xo[j] - pdb_xa[-1]) > xo_large:
                        xo_large = xo[j] - pdb_xa[-1]
                if xo[j] < pdb_xa[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_xa[0] - xo[j]) < xo_min:
                        xo_min = pdb_xa[0] - xo[j]
                if yo[j] > pdb_ya[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (yo[j] - pdb_ya[-1]) > yo_large:
                        yo_large = yo[j] - pdb_ya[-1]
                if yo[j] < pdb_ya[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_ya[0] - yp[j]) < yo_min:
                        yo_min = pdb_ya[0] - yo[j]
                if zo[j] > pdb_za[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (zo[j] - pdb_za[-1]) > zo_large:
                        zo_large = zo[j] - pdb_za[-1]
                if zo[j] < pdb_za[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_za[0] - zo[j]) < zo_min:
                        zo_min = pdb_za[0] - zo[j]
        print(file_name)
    pdb.set_trace()

if __name__ == '__main__':
	main()