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

def parse_vehiclecmd(filepath):

    steer_cmd = []
    accel_cmd = []
    brake_cmd = []
    lamp_cmd_l = []
    lamp_cmd_r = []
    gear_cmd = []
    mode = []
    xl = []
    yl = []
    zl = []
    xa = []
    ya = []
    za = []

    file = open(filepath,'r')
    a = file.readlines()

    for i in range(len(a)):
        if 'steer:' in a[i]:
            steer_cmd.append(float(a[i][9:-1]))
        elif 'accel:' in a[i]:
            accel_cmd.append(float(a[i][9:-1]))
        elif 'brake:' in a[i]:
            brake_cmd.append(float(a[i][9:-1]))
        elif 'l:' in a[i] and 'accel:' not in a[i]:
            lamp_cmd_l.append(float(a[i][5:-1]))
        elif 'r:' in a[i] and 'header' not in a[i] and 'steer' not in a[i] and 'gear' not in a[i] and 'linear' not in a[i] and 'angular' not in a[i]:
            #pdb.set_trace()
            lamp_cmd_r.append(float(a[i][5:-1]))
        elif 'gear:' in a[i]:
            gear_cmd.append(float(a[i][8:-1]))
        elif 'mode:' in a[i]:
            mode.append(float(a[i][6:-1]))
        elif 'x' in a[i]:
            if 'linear' in a[i-1]:
                #pdb.set_trace()
                xl.append(float(a[i][9:-1]))
            elif 'angular' in a[i-1]:
                xa.append(float(a[i][9:-1]))
        elif 'y' in a[i] and 'emergency'not in a[i]:
            if 'linear' in a[i-2]:
                #pdb.set_trace()
                yl.append(float(a[i][9:-1]))
            elif 'angular' in a[i-2]:
                ya.append(float(a[i][9:-1]))
        elif 'z' in a[i]:
            if 'linear' in a[i-3]:
                zl.append(float(a[i][9:-1]))
            elif 'angular' in a[i-3]:
                za.append(float(a[i][9:-1]))

    return steer_cmd, accel_cmd, brake_cmd, lamp_cmd_l, lamp_cmd_r, gear_cmd, mode, xl, xa, yl, ya, zl, za

def main():
    parser = argparse.ArgumentParser(description="base folder, save dir and database query")
    parser.add_argument('--base', default='localizer_pose_attack_sdc')
    parser.add_argument('--save', default='vehicle_cmd.pkl')
    args = parser.parse_args()
    file = gzip.GzipFile(args.save, 'rb')
    data = pickle.load(file)
    file.close()

    pdb_steer_cmd = {}
    pdb_accel_cmd = {}
    pdb_brake_cmd = {}
    pdb_lamp_cmd_l = {}
    pdb_lamp_cmd_r = {}
    pdb_gear_cmd = {}
    pdb_mode = {}
    pdb_xl = {}
    pdb_yl = {}
    pdb_zl = {}
    pdb_xa = {}
    pdb_ya = {}
    pdb_za = {}

    for i in range(len(data['xl'])):
        mid_frame = int(len(data['xl'][i]) * 18/51)
        for j in range(mid_frame-12,mid_frame+12):
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


    new_pdb_xl = sorted(pdb_xl.keys())
    new_pdb_yl = sorted(pdb_yl.keys())
    new_pdb_zl = sorted(pdb_zl.keys())
    new_pdb_xa = sorted(pdb_xa.keys())
    new_pdb_ya = sorted(pdb_ya.keys())
    new_pdb_za = sorted(pdb_za.keys())
    for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_attack_sdc/' + args.base):
        f = filenames
    success_file = []
    may_success_file = []
    for i in range(len(f)):
        cmd = 'unzip ' + '/localdisk/autoware_attack_sdc/' + args.base + '/' + f[i]
        #pdb.set_trace()
        os.system(cmd)
        rawfile = []
        steer_cmd, accel_cmd, brake_cmd, lamp_cmd_l, lamp_cmd_r, gear_cmd, mode, xl, xa, yl, ya, zl, za = parse_vehiclecmd(f[i][:-4]+'/vehicle_cmd.txt')
        cmd = 'rm -r '+str(f[i][:-4])
        os.system(cmd)
        mid_frame = int(len(xl)*18/51)
        start_frame = mid_frame - 12
        end_frame = mid_frame + 12
        for j in range(len(xl)):
            if j > start_frame and j < end_frame:
                if round(xl[j],1) < new_pdb_xl[0] or round(xl[j],1) > new_pdb_xl[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                    print(new_pdb_xl)
                    print(xl[j])
                else:
                    if round(xl[j],1) not in pdb_xl.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        print(pdb_xl)
                        print(xl[j])
                if round(yl[j],1) < new_pdb_yl[0] or round(yl[j],1) > new_pdb_yl[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                    print(new_pdb_yl)
                    print(yl[j])
                else:
                    if round(yl[j],1) not in pdb_yl.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        print(pdb_yl)
                        print(yl[j])
                if round(zl[j],1) < new_pdb_zl[0] or round(zl[j],1) > new_pdb_zl[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                    print(new_pdb_zl)
                    print(zl[j])
                else:
                    if round(zl[j],1) not in pdb_zl.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        print(pdb_zl)
                        print(zl[j])
                if round(xa[j],1) < new_pdb_xa[0] or round(xa[j],1) > new_pdb_xa[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                    print(new_pdb_xa)
                    print(xa[j])
                else:
                    if round(xa[j],1) not in pdb_xa.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        print(pdb_xa)
                        print(xa[j])
                if round(ya[j],1) < new_pdb_ya[0] or round(ya[j],1) > new_pdb_ya[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                    print(new_pdb_ya)
                    print(ya[j])
                else:
                    if round(ya[j],1) not in pdb_ya.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        print(pdb_ya)
                        print(ya[j])
                if round(za[j],1) < new_pdb_za[0] or round(za[j],1) > new_pdb_za[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                    print(new_pdb_za)
                    print(za[j])
                else:
                    if round(za[j],1) not in pdb_za.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        print(pdb_za)
                        print(za[j])
        #pdb.set_trace()
    print(len(success_file))
    print(success_file)
    print(len(may_success_file))
    print(may_success_file)
if __name__ == '__main__':
    main()