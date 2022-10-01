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

def parse_ndt(filepath):

    xp = []
    yp = []
    zp = []
    xo = []
    yo = []
    zo = []
    wo = []

    file = open(filepath,'r')
    a = file.readlines()

    for i in range(len(a)):
        if 'x' in a[i]:
            if 'position:' in a[i-1]:
                xp.append(float(a[i][7:-1]))
            elif 'orientation:' in a[i-1]:
                xo.append(float(a[i][7:-1]))
        elif 'y' in a[i]:
            if 'position:' in a[i-2]:
                yp.append(float(a[i][7:-1]))
            elif 'orientation:' in a[i-2]:
                yo.append(float(a[i][7:-1]))
        elif 'z' in a[i]:
            if 'position:' in a[i-3]:
                zp.append(float(a[i][7:-1]))
            elif 'orientation:' in a[i-3]:
                zo.append(float(a[i][7:-1]))
        elif 'w:' in a[i]:
            wo.append(float(a[i][7:-1]))

    return xp,yp,zp,xo,yo,zo,wo

def main():
    parser = argparse.ArgumentParser(description="base folder, save dir and database query")
    parser.add_argument('--base', default='ndt_matching_attack_generalregis')
    parser.add_argument('--save', default='ndt_pose.pkl')
    args = parser.parse_args()

    file = gzip.GzipFile(args.save, 'rb')
    data = pickle.load(file)
    file.close()
    pdb_xp = {}
    pdb_yp = {}
    pdb_zp = {}
    pdb_xo = {}
    pdb_yo = {}
    pdb_zo = {}
    pdb_wo = {}

    for i in range(len(data['xp'])):
        for j in range(180,204):
            #pdb.set_trace()
            tmp = round((data['xp'][i][j]),1)
            if tmp not in pdb_xp:
                pdb_xp[tmp] = 1
            else:
                pdb_xp[tmp] += 1
            tmp = round((data['yp'][i][j]),1)
            if tmp not in pdb_yp:
                pdb_yp[tmp] = 1
            else:
                pdb_yp[tmp] += 1
            tmp = round((data['zp'][i][j]),1)
            if tmp not in pdb_zp:
                pdb_zp[tmp] = 1
            else:
                pdb_zp[tmp] += 1
            tmp = round((data['xo'][i][j]),1)
            if tmp not in pdb_xo:
                pdb_xo[tmp] = 1
            else:
                pdb_xo[tmp] += 1
            tmp = round((data['yo'][i][j]),1)
            if tmp not in pdb_yo:
                pdb_yo[tmp] = 1
            else:
                pdb_yo[tmp] += 1
            tmp = round((data['zo'][i][j]),1)
            if tmp not in pdb_zo:
                pdb_zo[tmp] = 1
            else:
                pdb_zo[tmp] += 1
            tmp = round((data['wo'][i][j]),1)
            if tmp not in pdb_wo:
                pdb_wo[tmp] = 1
            else:
                pdb_wo[tmp] += 1
    pdb_xp = sorted(pdb_xp.keys())
    pdb_yp = sorted(pdb_yp.keys())
    pdb_zp = sorted(pdb_zp.keys())
    pdb_xo = sorted(pdb_xo.keys())
    pdb_yo = sorted(pdb_yo.keys())
    pdb_zo = sorted(pdb_zo.keys())
    pdb_wo = sorted(pdb_wo.keys())

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
    wo_large = 0
    wo_min = 0
    file_name = []
    for i in range(1,len(f)):
        cmd = 'cp -r ' + f[i] + ' ./tmp/'
        #pdb.set_trace()
        os.system(cmd)
        xp,yp,zp,xo,yo,zo,wo = parse_ndt('tmp/ndt_pose.txt')
        cmd = 'rm -r tmp'
        os.system(cmd)
        for j in range(len(xp)):
            if j >= 180 and j < 204:
                if xp[j] > pdb_xp[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (xp[j] - pdb_xp[-1]) > xp_large:
                        xp_large = xp[j] - pdb_xp[-1]
                if xp[j] < pdb_xp[0]:	
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_xp[0] - xp[j]) < xp_min:
                        xp_min = pdb_xp[0] - xp[j]
                if yp[j] > pdb_yp[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (yp[j] - pdb_yp[-1]) > yp_large:
                        yp_large = yp[j] - pdb_yp[-1]
                if yp[j] < pdb_yp[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_yp[0] - yp[j]) < yp_min:
                        yp_min = pdb_yp[0] - yp[j]
                if zp[j] > pdb_zp[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (zp[j] - pdb_zp[-1]) > zp_large:
                        zp_large = zp[j] - pdb_zp[-1]
                if zp[j] < pdb_zp[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_zp[0] - zp[j]) < zp_min:
                        zp_min = pdb_zp[0] - zp[j]
                if xo[j] > pdb_xo[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (xo[j] - pdb_xo[-1]) > xo_large:
                        xo_large = xo[j] - pdb_xo[-1]
                if xo[j] < pdb_xo[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_xo[0] - xo[j]) < xo_min:
                        xo_min = pdb_xo[0] - xo[j]
                if yo[j] > pdb_yo[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (yo[j] - pdb_yo[-1]) > yo_large:
                        yo_large = yo[j] - pdb_yo[-1]
                if yo[j] < pdb_yo[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_yo[0] - yp[j]) < yo_min:
                        yo_min = pdb_yo[0] - yo[j]
                if zo[j] > pdb_zo[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (zo[j] - pdb_zo[-1]) > zo_large:
                        zo_large = zo[j] - pdb_zo[-1]
                if zo[j] < pdb_zo[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_zo[0] - zo[j]) < zo_min:
                        zo_min = pdb_zo[0] - zo[j]
                if wo[j] > pdb_wo[-1]:
                    if i not in file_name:
                        file_name.append(i)
                    if (wo[j] - pdb_wo[-1]) > wo_large:
                        wo_large = wo[j] - pdb_wo[-1]
                if wo[j] < pdb_wo[0]:
                    if i not in file_name:
                        file_name.append(i)
                    if (pdb_wo[0] - wo[j]) < wo_min:
                        wo_min = pdb_wo[0] - wo[j]
        print(file_name)
    pdb.set_trace()

if __name__ == '__main__':
	main()