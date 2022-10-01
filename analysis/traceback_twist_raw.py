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
import random
from collections import deque
import math

def bitflip_small(signal, i, ori_num):
    if signal == 'xl':
        xp_min = ori_num - 5
        if i == 32:
            return ori_num - random.randint(1,10)
        elif i == 33:
            return ori_num + random.randint(1,10)
        else:
            return xp_min + 10/32*i
    if signal == 'yl':
        yp_min = ori_num - 5
        if i == 32:
            return ori_num - random.randint(1,10)
        elif i == 33:
            return ori_num + random.randint(1,10)
        else:
            return yp_min + 10/32*i
    if signal == 'zl':
        zp_min = ori_num - 5
        if i == 32:
            return ori_num - random.randint(1,10)
        elif i == 33:
            return ori_num + random.randint(1,10)
        else:
            return zp_min + 10/32*i
    if signal == 'xa':
        xo_min = ori_num - 5
        if i == 32:
            return ori_num - random.randint(1,10)
        elif i == 33:
            return ori_num + random.randint(1,10)
        else:
            return xo_min + 10/32*i    
    if signal == 'ya':
        yo_min = ori_num - 5
        if i == 32:
            return ori_num - random.randint(1,10)
        elif i == 33:
            return ori_num + random.randint(1,10)
        else:
            return yo_min + 10/32*i  
    if signal == 'za':
        zo_min = ori_num - 5
        if i == 32:
            return ori_num - random.randint(1,10)
        elif i == 33:
            return ori_num + random.randint(1,10)
        else:
            return zo_min + 10/32*i

def bitflip(signal, i, ori_num):
    if signal == 'xl':
        xp_min = ori_num - 600
        if i == 32:
            return ori_num - random.randint(1,600)
        elif i == 33:
            return ori_num + random.randint(1,600)
        else:
            return xp_min + 1200/32*i
    if signal == 'yl':
        yp_min = ori_num - 600
        if i == 32:
            return ori_num - random.randint(1,600)
        elif i == 33:
            return ori_num + random.randint(1,600)
        else:
            return yp_min + 1200/32*i
    if signal == 'zl':
        zp_min = ori_num - 600
        if i == 32:
            return ori_num - random.randint(1,600)
        elif i == 33:
            return ori_num + random.randint(1,600)
        else:
            return zp_min + 1200/32*i
    if signal == 'xa':
        xo_min = ori_num - 600
        if i == 32:
            return ori_num - random.randint(1,600)
        elif i == 33:
            return ori_num + random.randint(1,600)
        else:
            return xo_min + 1200/32*i    
    if signal == 'ya':
        yo_min = ori_num - 600
        if i == 32:
            return ori_num - random.randint(1,600)
        elif i == 33:
            return ori_num + random.randint(1,600)
        else:
            return yo_min + 1200/32*i  
    if signal == 'za':
        zo_min = ori_num - 600
        if i == 32:
            return ori_num - random.randint(1,600)
        elif i == 33:
            return ori_num + random.randint(1,600)
        else:
            return zo_min + 1200/32*i

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

def parse_twistraw(filepath):

    xl = []
    yl = []
    zl = []
    xa = []
    ya = []
    za = []

    file = open(filepath,'r')
    a = file.readlines()

    for i in range(len(a)):
        if 'x' in a[i]:
            if 'linear' in a[i-1]:
                xl.append(float(a[i][7:-1]))
            elif 'angular' in a[i-1]:
                xa.append(float(a[i][7:-1]))
        elif 'y' in a[i]:
            if 'linear' in a[i-2]:
                yl.append(float(a[i][7:-1]))
            elif 'angular' in a[i-2]:
                ya.append(float(a[i][7:-1]))
        elif 'z' in a[i]:
            if 'linear' in a[i-3]:
                zl.append(float(a[i][7:-1]))
            elif 'angular' in a[i-3]:
                za.append(float(a[i][7:-1]))

    return xl,xa,yl,ya,zl,za

def cavg(q):
    sum_q = 0
    for i in range(len(q)):
        sum_q += q[i]
    avg_q = sum_q/len(q)
    std_q = 0
    for i in range(len(q)):
        std_q += (q[i]-avg_q)*(q[i]-avg_q)
    std_q = std_q/len(q)
    std_q = math.sqrt(std_q)
    return avg_q,std_q

def find_injection_raw(xl_vo, xa_vo, yl_vo, ya_vo, zl_vo, za_vo,filename):
    file_str = filename.split('_')
    signal = file_str[2][6:8]
    q = deque(maxlen=8)

    if signal == 'xl':
        for i in range(len(xl_vo)):
            if len(q) < 8:
                q.append(xl_vo[i])
            else:
                avg,std = cavg(q)
                if (abs(xl_vo[i] - avg) > 3*std):
                    return i 
                else:
                    q.append(xl_vo[i])      
    if signal == 'yl':
        for i in range(len(yl_vo)):
            if len(q) < 8:
                q.append(yl_vo[i])
            else:
                avg,std = cavg(q)
                if (abs(yl_vo[i] - avg) > 3*std):
                    return i 
                else:
                    q.append(yl_vo[i])    
    if signal == 'zl':
        for i in range(len(zl_vo)):
            if len(q) < 8:
                q.append(zl_vo[i])
            else:
                avg,std = cavg(q)
                if (abs(zl_vo[i] - avg) > 3*std):
                    return i 
                else:
                    q.append(zl_vo[i])    
    if signal == 'xa':
        for i in range(len(xa_vo)):
            if len(q) < 8:
                q.append(xa_vo[i])
            else:
                avg,std = cavg(q)
                if (abs(xa_vo[i] - avg) > 3*std):
                    return i 
                else:
                    q.append(xa_vo[i])   
    if signal == 'ya':
        for i in range(len(ya_vo)):
            if len(q) < 8:
                q.append(ya_vo[i])
            else:
                avg,std = cavg(q)
                if (abs(ya_vo[i] - avg) > 3*std):
                    return i 
                else:
                    q.append(ya_vo[i])   
    if signal == 'za':
        for i in range(len(za_vo)):
            if len(q) < 8:
                q.append(za_vo[i])
            else:
                avg,std = cavg(q)
                if (abs(za_vo[i] - avg) > 3*std) and i > len(za_vo)/5 and (za_vo[i] > 0.1 or za_vo[i] < -0.1):
                    return i 
                else:
                    q.append(za_vo[i])  
    return 0                   

def find_injection_range(xl_vo, xa_vo, yl_vo, ya_vo, zl_vo, za_vo,filename):
    #pdb.set_trace()
    file_str = filename.split('_')
    signal = file_str[2][6:8]
    bit = int(file_str[2][11:])
    flag = 0
    ori_xl, ori_yl, ori_zl, ori_xa, ori_ya, ori_za = parse_twistraw('/localdisk/autoware_attack_sdc/baseline148/twist_raw.txt')
    if signal == 'xl':
        inject_number = bitflip('xl',bit,ori_xl[int(len(ori_xl)*18/51)])
        if ori_xl[int(len(ori_xl)*18/51)] == 0:
            return 0
        else:
            return (inject_number - ori_xl[int(len(ori_xl)*18/51)])/ori_xl[int(len(ori_xl)*18/51)]

    if signal == 'yl':
        inject_number = bitflip('yl',bit,ori_yl[int(len(ori_yl)*18/51)])
        if ori_yl[int(len(ori_yl)*18/51)] == 0:
            return 0
        else:
            return (inject_number - ori_yl[int(len(ori_yl)*18/51)])/ori_yl[int(len(ori_yl)*18/51)]

    if signal == 'zl':
        inject_number = bitflip('zl',bit,ori_zl[int(len(ori_zl)*18/51)])
        if ori_zl[int(len(ori_zl)*18/51)] == 0:
            return 0
        else:
            return (inject_number - ori_zl[int(len(ori_zl)*18/51)])/ori_zl[int(len(ori_zl)*18/51)]

    if signal == 'xa':
        inject_number = bitflip('xa',bit,ori_xa[int(len(ori_xa)*18/51)])
        if ori_xa[int(len(ori_xa)*18/51)] == 0:
            return 0
        else:
            return (inject_number - ori_xa[int(len(ori_xa)*18/51)])/ori_xa[int(len(ori_xa)*18/51)]
    
    if signal == 'ya':
        inject_number = bitflip('ya',bit,ori_ya[int(len(ori_ya)*18/51)])
        if ori_ya[int(len(ori_ya)*18/51)] == 0:
            return 0
        else:
            return (inject_number - ori_ya[int(len(ori_ya)*18/51)])/ori_ya[int(len(ori_ya)*18/51)]

    if signal == 'za':
        inject_number = bitflip('za',bit,ori_za[int(len(ori_za)*18/51)])
        if ori_za[int(len(ori_za)*18/51)] == 0:
            return 0
        else:
            return (inject_number - ori_za[int(len(ori_za)*18/51)])/ori_za[int(len(ori_za)*18/51)]

def main():
    parser = argparse.ArgumentParser(description="base folder, save dir and database query")
    parser.add_argument('--base', default='protect_twist_raw_small')
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
    all_injection_amp = {0:0,0.1:0,0.2:0,0.5:0,1:0,2:0,3:0}
    succss_injection_amp = {0:0,0.1:0,0.2:0,0.5:0,1:0,2:0,3:0}
    for i in range(len(f)):
        cmd = 'unzip ' + '/localdisk/autoware_attack_sdc/' + args.base + '/' + f[i]
        #pdb.set_trace()
        os.system(cmd)

        rawfile = []
        steer_cmd, accel_cmd, brake_cmd, lamp_cmd_l, lamp_cmd_r, gear_cmd, mode, xl, xa, yl, ya, zl, za = parse_vehiclecmd(f[i][:-4]+'/vehicle_cmd.txt')
        xl_tr,xa_tr,yl_tr,ya_tr,zl_tr,za_tr = parse_twistraw(f[i][:-4]+'/twist_raw.txt')
        #pdb.set_trace()
        mid_frame_ = find_injection_raw(xl_tr, xa_tr, yl_tr, ya_tr, zl_tr, za_tr,f[i][:-4])
        amp = find_injection_range(xl_tr, xa_tr, yl_tr, ya_tr, zl_tr, za_tr,f[i][:-4])

        if amp == 0:
            all_injection_amp[0] += 1
        elif amp < 0.1:
            all_injection_amp[0.1] += 1
        elif amp > 0.1 and amp < 0.2:
            all_injection_amp[0.2] += 1
        elif amp > 0.2 and amp < 0.5:
            all_injection_amp[0.5] += 1
        elif amp > 0.5 and amp < 1:
            all_injection_amp[1] += 1
        elif amp > 1 and amp < 2:
            all_injection_amp[2] += 1
        else:
            if 'za' in f[i]:
                cmd = 'rm -r '+str(f[i][:-4])
                os.system(cmd)
                continue
            all_injection_amp[3] += 1
        
        if mid_frame_ == 0:
            mid_frame = int(len(xl)*mid_frame_)
        else:
            mid_frame = int(mid_frame_/len(xl_tr)*len(xl))
        start_frame = mid_frame - 6
        end_frame = mid_frame + 6
        for j in range(len(xl)):
            if j > start_frame and j < end_frame:
                if round(xl[j],1) < new_pdb_xl[0] or round(xl[j],1) > new_pdb_xl[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
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
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
                    print(new_pdb_yl)
                    print(yl[j])
                else:
                    if round(yl[j],1) not in pdb_yl.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
                        print(pdb_yl)
                        print(yl[j])
                if round(zl[j],1) < new_pdb_zl[0] or round(zl[j],1) > new_pdb_zl[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
                    print(new_pdb_zl)
                    print(zl[j])
                else:
                    if round(zl[j],1) not in pdb_zl.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
                        print(pdb_zl)
                        print(zl[j])
                if round(xa[j],1) < new_pdb_xa[0] or round(xa[j],1) > new_pdb_xa[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
                    print(new_pdb_xa)
                    print(xa[j])
                else:
                    if round(xa[j],1) not in pdb_xa.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
                        print(pdb_xa)
                        print(xa[j])
                if round(ya[j],1) < new_pdb_ya[0] or round(ya[j],1) > new_pdb_ya[-1]:
                    if f[i] not in success_file:
                        success_file.append(f[i])
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
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
                        if amp == 0:
                            succss_injection_amp[0] += 1
                        elif amp < 0.1:
                            succss_injection_amp[0.1] += 1
                        elif amp > 0.1 and amp < 0.2:
                            succss_injection_amp[0.2] += 1
                        elif amp > 0.2 and amp < 0.5:
                            succss_injection_amp[0.5] += 1
                        elif amp > 0.5 and amp < 1:
                            succss_injection_amp[1] += 1
                        elif amp > 1 and amp < 2:
                            succss_injection_amp[2] += 1
                        else:
                            #pdb.set_trace()
                            succss_injection_amp[3] += 1
                    print(new_pdb_za)
                    print(za[j])
                else:
                    if round(za[j],1) not in pdb_za.keys():
                        if f[i] not in may_success_file:
                            may_success_file.append(f[i])
                        print(pdb_za)
                        print(za[j])
        #pdb.set_trace()
        cmd = 'rm -r '+str(f[i][:-4])
        os.system(cmd)
        print(succss_injection_amp)
        print(all_injection_amp)
    print(len(success_file))
    print(success_file)
    print(len(may_success_file))
    print(may_success_file)

if __name__ == '__main__':
    main()