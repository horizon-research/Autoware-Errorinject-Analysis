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
from rostopic_parser import parse_curr_pose
from sklearn.cluster import DBSCAN
from rostopic_parser import parse_curr_velo
from rostopic_parser import parse_lpcmd
from rostopic_parser import parse_vodometry
from rostopic_parser import parse_ndt
from rostopic_parser import parse_twistraw
from rostopic_parser import parse_twistcmd
from rostopic_parser import parse_vehiclecmd

def is_outlier(points, thresh=10.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh

def is_outlier_doubleMAD(points):
    """
    FOR ASSYMMETRIC DISTRIBUTION
    Returns : filtered array excluding the outliers

    Parameters : the actual data Points array

    Calculates median to divide data into 2 halves.(skew conditions handled)
    Then those two halves are treated as separate data with calculation same as for symmetric distribution.(first answer) 
    Only difference being , the thresholds are now the median distance of the right and left median with the actual data median
    """

    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    medianIndex = int(points.size/2)
    
    leftData = np.copy(points[0:medianIndex])
    rightData = np.copy(points[medianIndex:points.size])

    median1 = np.median(leftData, axis=0)
    diff1 = np.sum((leftData - median1)**2, axis=-1)
    diff1 = np.sqrt(diff1)

    median2 = np.median(rightData, axis=0)
    diff2 = np.sum((rightData - median2)**2, axis=-1)
    diff2 = np.sqrt(diff2)

    med_abs_deviation1 = max(np.median(diff1),0.000001)
    med_abs_deviation2 = max(np.median(diff2),0.000001)

    threshold1 = ((median-median1)/med_abs_deviation1)*3
    threshold2 = ((median2-median)/med_abs_deviation2)*3

    #if any threshold is 0 -> no outliers
    if threshold1==0:
        threshold1 = sys.maxint
    if threshold2==0:
        threshold2 = sys.maxint
    #multiplied by a factor so that only the outermost points are removed
    modified_z_score1 = 0.6745 * diff1 / med_abs_deviation1
    modified_z_score2 = 0.6745 * diff2 / med_abs_deviation2

    filtered1 = []
    i = 0
    for data in modified_z_score1:
        if data < threshold1:
            filtered1.append(leftData[i])
        i += 1
    i = 0
    filtered2 = []
    for data in modified_z_score2:
        if data < threshold2:
            filtered2.append(rightData[i])
        i += 1

    filtered = filtered1 + filtered2
    return filtered

def main():
    
    #check vehicle odomtry signal
    xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za = [],[],[],[],[],[],[],[],[],[],[],[],[]
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
    for i in range(10):
        path = base_std + str(i) + '/vehicle_odom.txt'
        xp_,yp_,zp_,xo_,yo_,zo_,wo_,xl_,yl_,zl_,xa_,ya_,za_ = parse_vodometry(path)
        xp.append(xp_)
        yp.append(yp_)
        zp.append(zp_)
        xo.append(xo_)
        yo.append(yo_)
        zo.append(zo_)
        wo.append(wo_)
        xl.append(xl_)
        yl.append(yl_)
        zl.append(zl_)
        xa.append(xa_)
        ya.append(ya_)
        za.append(za_)
    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/vehicle_odom.txt'
        #pdb.set_trace()
        xpa,ypa,zpa,xoa,yoa,zoa,woa,xla,yla,zla,xaa,yaa,zaa = parse_vodometry(path)
        #pdb.set_trace()
        #window_mid = int(len(xpa)*18/51)
        window_mid = 120
        window_start = window_mid-1
        window_end = window_mid+1
        #pdb.set_trace()
        for k in range(window_start,window_end):
            attack = [xpa[k],ypa[k],zpa[k],xoa[k],yoa[k],zoa[k],woa[k],xla[k],yla[k],zla[k],xaa[k],yaa[k],zaa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(xp[t][j])
                    base[1].append(yp[t][j])
                    base[2].append(zp[t][j])
                    base[3].append(xo[t][j])
                    base[4].append(yo[t][j])
                    base[5].append(zo[t][j])
                    base[6].append(wo[t][j])
                    base[7].append(xl[t][j])
                    base[8].append(yl[t][j])
                    base[9].append(zl[t][j])
                    base[10].append(xa[t][j])
                    base[11].append(ya[t][j])
                    base[12].append(za[t][j])
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('vehicle odom signal checked')                                        

    #check current pose signal
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
    xp,yp,zp,xo,yo,zo,wo = [],[],[],[],[],[],[]
    for i in range(10):
        path = base_std + str(i) + '/current_pose.txt'
        xp_,yp_,zp_,xo_,yo_,zo_,wo_ = parse_curr_pose(path)
        xp.append(xp_)
        yp.append(yp_)
        zp.append(zp_)
        xo.append(xo_)
        yo.append(yo_)
        zo.append(zo_)
        wo.append(wo_)

    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/current_pose.txt'
        xpa,ypa,zpa,xoa,yoa,zoa,woa = parse_curr_pose(path)
        #xpa[189] = 0.1
        #window_mid = int(len(xpa)*18/51)
        window_mid = 120
        window_start = window_mid-5
        window_end = window_mid+6
        
        for k in range(window_start,window_end):
            attack = [xpa[k],ypa[k],zpa[k],xoa[k],yoa[k],zoa[k],woa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(xp[t][j])
                    base[1].append(yp[t][j])
                    base[2].append(zp[t][j])
                    base[3].append(xo[t][j])
                    base[4].append(yo[t][j])
                    base[5].append(zo[t][j])
                    base[6].append(wo[t][j])
                #regular outlier detection not working as most of statistical outlier detection methods assume a distribution,
                #lead to very high false positive
                '''
                for t in range(len(base)):
                    base[t].append(attack[t])
                    temp = np.array(base[t])
                    outlier_detection = is_outlier(temp)
                    #pdb.set_trace()
                    if True in list(outlier_detection):
                        print('outlier in current_pose, time frame %d'%k)
                        print('outlier signal %d'%t)
                        pdb.set_trace()
                '''
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    #pdb.set_trace()
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('current_pose signal checked')

    #check current velocity signal
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
    xl,yl,zl,xa,ya,za = [],[],[],[],[],[]
    for i in range(10):
        path = base_std + str(i) + '/current_velocity.txt'
        xl_,yl_,zl_,xa_,ya_,za_ = parse_curr_velo(path)
        xl.append(xl_)
        yl.append(yl_)
        zl.append(zl_)
        xa.append(xa_)
        ya.append(ya_)
        za.append(za_)
    
    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/current_velocity.txt'
        xla,yla,zla,xaa,yaa,zaa = parse_curr_velo(path)
        #window_mid = int(len(xla)*18/51)
        window_mid = 120
        window_start = window_mid-5
        window_end = window_mid+6
        for k in range(window_start,window_end):
            attack = [xla[k],yla[k],zla[k],xaa[k],yaa[k],zaa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(xl[t][j])
                    base[1].append(yl[t][j])
                    base[2].append(zl[t][j])
                    base[3].append(xa[t][j])
                    base[4].append(ya[t][j])
                    base[5].append(za[t][j])
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    #pdb.set_trace()
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('current_velocity signal checked')
    #pdb.set_trace()

    #check estimate twist signal
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
    xl,yl,zl,xa,ya,za = [],[],[],[],[],[]
    for i in range(10):
        path = base_std + str(i) + '/estimate_twist.txt'
        xl_,yl_,zl_,xa_,ya_,za_ = parse_curr_velo(path)
        xl.append(xl_)
        yl.append(yl_)
        zl.append(zl_)
        xa.append(xa_)
        ya.append(ya_)
        za.append(za_)

    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/estimate_twist.txt'
        xla,yla,zla,xaa,yaa,zaa = parse_curr_velo(path)
        #pdb.set_trace()
        #window_mid = int(len(xla)*18/51)
        window_mid = 120
        window_start = window_mid-5
        window_end = window_mid+6
        for k in range(window_start,window_end):
            attack = [xla[k],yla[k],zla[k],xaa[k],yaa[k],zaa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(xl[t][j])
                    base[1].append(yl[t][j])
                    base[2].append(zl[t][j])
                    base[3].append(xa[t][j])
                    base[4].append(ya[t][j])
                    base[5].append(za[t][j])
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    #pdb.set_trace()
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('estimate_twist signal checked')

    #final waypoint check, need development

    #grid map wayarea check, need development

    #ndt pose check
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
    xp,yp,zp,xo,yo,zo,wo = [],[],[],[],[],[],[]
    for i in range(10):
        path = base_std + str(i) + '/ndt_pose.txt'
        xp_,yp_,zp_,xo_,yo_,zo_,wo_ = parse_curr_pose(path)
        xp.append(xp_)
        yp.append(yp_)
        zp.append(zp_)
        xo.append(xo_)
        yo.append(yo_)
        zo.append(zo_)
        wo.append(wo_)

    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/ndt_pose.txt'
        xpa,ypa,zpa,xoa,yoa,zoa,woa = parse_curr_pose(path)
        #xpa[189] = 0.1
        #window_mid = int(len(xpa)*18/51)
        window_mid = 120
        window_start = window_mid-5
        window_end = window_mid+6
        
        for k in range(window_start,window_end):
            attack = [xpa[k],ypa[k],zpa[k],xoa[k],yoa[k],zoa[k],woa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(xp[t][j])
                    base[1].append(yp[t][j])
                    base[2].append(zp[t][j])
                    base[3].append(xo[t][j])
                    base[4].append(yo[t][j])
                    base[5].append(zo[t][j])
                    base[6].append(wo[t][j])
                #regular outlier detection not working as most of statistical outlier detection methods assume a distribution,
                #lead to very high false positive
                '''
                for t in range(len(base)):
                    base[t].append(attack[t])
                    temp = np.array(base[t])
                    outlier_detection = is_outlier(temp)
                    #pdb.set_trace()
                    if True in list(outlier_detection):
                        print('outlier in current_pose, time frame %d'%k)
                        print('outlier signal %d'%t)
                        pdb.set_trace()
                '''
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    #pdb.set_trace()
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('ndt_pose signal checked')

    #check twist raw signal
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
    xl,yl,zl,xa,ya,za = [],[],[],[],[],[]
    for i in range(10):
        path = base_std + str(i) + '/twist_raw.txt'
        xl_,yl_,zl_,xa_,ya_,za_ = parse_twistraw(path)
        xl.append(xl_)
        yl.append(yl_)
        zl.append(zl_)
        xa.append(xa_)
        ya.append(ya_)
        za.append(za_)

    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/twist_raw.txt'
        xla,yla,zla,xaa,yaa,zaa = parse_twistraw(path)
        #window_mid = int(len(xla)*18/51)
        #false positive here, so change the window
        window_mid = 120
        window_start = window_mid+5
        window_end = window_mid+15
        for k in range(window_start,window_end):
            attack = [xla[k],yla[k],zla[k],xaa[k],yaa[k],zaa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(xl[t][j])
                    base[1].append(yl[t][j])
                    base[2].append(zl[t][j])
                    base[3].append(xa[t][j])
                    base[4].append(ya[t][j])
                    base[5].append(za[t][j])
                #pdb.set_trace()
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    #pdb.set_trace()
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('twist_raw signal checked')    

    #check twist cmd signal
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
    xl,yl,zl,xa,ya,za = [],[],[],[],[],[]
    for i in range(10):
        path = base_std + str(i) + '/twist_cmd.txt'
        xl_,yl_,zl_,xa_,ya_,za_ = parse_twistraw(path)
        xl.append(xl_)
        yl.append(yl_)
        zl.append(zl_)
        xa.append(xa_)
        ya.append(ya_)
        za.append(za_)

    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/twist_cmd.txt'
        xla,yla,zla,xaa,yaa,zaa = parse_twistraw(path)
        #window_mid = int(len(xla)*18/51)
        window_mid = 120
        window_start = window_mid-5
        window_end = window_mid+6
        for k in range(window_start,window_end):
            attack = [xla[k],yla[k],zla[k],xaa[k],yaa[k],zaa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(xl[t][j])
                    base[1].append(yl[t][j])
                    base[2].append(zl[t][j])
                    base[3].append(xa[t][j])
                    base[4].append(ya[t][j])
                    base[5].append(za[t][j])
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    #pdb.set_trace()
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('twist_cmd signal checked')

    #check vehicle cmd
    base_std = '/home/Yangtze/12042021/vehicle__odom_attack'
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
    for i in range(10):
        path = base_std + str(i) + '/vehicle_cmd.txt'
        steer_cmd_,accel_cmd_,brake_cmd_,lamp_cmd_l_,lamp_cmd_r_,gear_cmd_,mode_,xl_,yl_,zl_,xa_,ya_,za_ = parse_vehiclecmd(path)
        steer_cmd.append(steer_cmd_)
        accel_cmd.append(accel_cmd_)
        brake_cmd.append(brake_cmd_)
        lamp_cmd_l.append(lamp_cmd_l_)
        lamp_cmd_r.append(lamp_cmd_r_)
        gear_cmd.append(gear_cmd_)
        mode.append(mode_)
        xl.append(xl_)
        yl.append(yl_)
        zl.append(zl_)
        xa.append(xa_)
        ya.append(ya_)
        za.append(za_)
        #pdb.set_trace()
    attack_std = '/home/Yangtze/12082021/vehicle__odom_attack'
    for i in range(3):
        path = attack_std + str(i) + '/vehicle_cmd.txt'
        steer_cmda,accel_cmda,brake_cmda,lamp_cmd_la,lamp_cmd_ra,gear_cmda,modea,xla,yla,zla,xaa,yaa,zaa = parse_vehiclecmd(path)
        #window_mid = int(len(xla)*18/51)
        window_mid = 120
        window_start = window_mid-5
        window_end = window_mid+6
        for k in range(window_start,window_end):
            attack = [steer_cmda[k],accel_cmda[k],brake_cmda[k],lamp_cmd_la[k],lamp_cmd_ra[k],gear_cmda[k],modea[k],xla[k],yla[k],zla[k],xaa[k],yaa[k],zaa[k]]
            for j in range(window_start,window_end):
                base = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
                for t in range(10):
                    base[0].append(steer_cmd[t][j])
                    base[1].append(accel_cmd[t][j])
                    base[2].append(brake_cmd[t][j])
                    base[3].append(lamp_cmd_l[t][j])
                    base[4].append(lamp_cmd_r[t][j])
                    base[5].append(gear_cmd[t][j])
                    base[6].append(mode[t][j])
                    base[7].append(xl[t][j])
                    base[8].append(yl[t][j])
                    base[9].append(zl[t][j])
                    base[10].append(xa[t][j])
                    base[11].append(ya[t][j])
                    base[12].append(za[t][j])
                for t in range(len(base)):
                    base[t].sort()
                    temp = {}
                    for x in base[t]:
                        if x in temp.keys():
                            temp[x] += 1
                        else:
                            temp[x] = 1
                    base_value = []
                    base_prob = []
                    for x in temp.keys():
                        base_value.append(x)
                        base_prob.append(temp[x]/sum(temp.values()))
                    pdb.set_trace()
                    if attack[t] > base_value[-1] and ((attack[t]-base_value[-1]) > (base_value[-1]-base_value[0])) and (attack[t]-base_value[-1]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
                    if attack[t] < base_value[0] and ((base_value[0]-attack[t]) > (base_value[-1]-base_value[0])) and (base_value[0]-attack[t]>0.5):
                        print('outlier exist in frame %d'%k)
                        print('outlier exist in signal %d'%t)
                        print('outlier exist in attack %d'%i)
                        #pdb.set_trace()
    print('vehicle_cmd signal checked')



if __name__ == '__main__':
    main()