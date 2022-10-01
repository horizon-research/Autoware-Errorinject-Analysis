import os
import os
import time
import signal
import subprocess
import pdb
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description='Inject error in twist raw')
    parser.add_argument('--signal', default='xl')
    parser.add_argument('--delta', default=0.1,type=float)
    parser.add_argument('--time', default=5.0,type=float)
    parser.add_argument('--iter', default=False)

    args = parser.parse_args()
    #pdb.set_trace()
    xl_ = np.load('./tr_base/x_linear.npy')
    xa_ = np.load('./tr_base/x_angular.npy')
    yl_ = np.load('./tr_base/y_linear.npy')
    ya_ = np.load('./tr_base/y_angular.npy')
    zl_ = np.load('./tr_base/z_linear.npy')
    za_ = np.load('./tr_base/z_angular.npy')
    #pdb.set_trace()
    cmd = '''rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped "{'header': {'seq': 0, 'stamp': {'secs': 0, 'nsecs': 0}, 'frame_id': "world" }, 'pose': {'position': {'x': 170, 'y': 0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.00720201027314, 'w': 0.999974065188}}}" --once'''
    os.system(cmd)
    process2 = subprocess.Popen('''rostopic echo /vehicle_status > vs.txt ''',shell=True)
    process3 = subprocess.Popen('''rostopic echo /gnss_pose > gnss.txt ''',shell=True)
    pid2 = process2.pid
    pid3 = process3.pid

    time.sleep(args.time)
    if args.signal == 'xl':
        injectxl = xl_[int(len(xl_) * args.time/51)] + args.delta
        yl = yl_[int(len(xl_) * args.time/51)]
        zl = zl_[int(len(xl_) * args.time/51)]
        xa = xa_[int(len(xl_) * args.time/51)]
        ya = ya_[int(len(xl_) * args.time/51)]
        za = za_[int(len(xl_) * args.time/51)]
        if args.iter is False:
            cmd = '''rostopic pub --once /twist_raw geometry_msgs/TwistStamped "{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x': %f,'y': %f, 'z': %f}}}"''' % (injectxl,yl,zl,xa,ya,za)
            print(cmd)
            os.system(cmd)

    elif args.signal == 'xa':
        xl = xl_[int(len(xl_) * args.time/51)] 
        yl = yl_[int(len(xl_) * args.time/51)]
        zl = zl_[int(len(xl_) * args.time/51)]
        injectxa = xa_[int(len(xl_) * args.time/51)] + args.delta
        ya = ya_[int(len(xl_) * args.time/51)]
        za = za_[int(len(xl_) * args.time/51)]
        if args.iter is False:
            cmd = '''rostopic pub --once /twist_raw geometry_msgs/TwistStamped "{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x': %f,'y': %f, 'z': %f}}}"''' % (xl,yl,zl,injectxa,ya,za)
            print(cmd)
            os.system(cmd)    

    elif args.signal == 'yl':
        xl = xl_[int(len(xl_) * args.time/51)] 
        injectyl = yl_[int(len(xl_) * args.time/51)]+ args.delta
        zl = zl_[int(len(xl_) * args.time/51)]
        xa = xa_[int(len(xl_) * args.time/51)] 
        ya = ya_[int(len(xl_) * args.time/51)]
        za = za_[int(len(xl_) * args.time/51)]
        if args.iter is False:
            cmd = '''rostopic pub --once /twist_raw geometry_msgs/TwistStamped "{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x': %f,'y': %f, 'z': %f}}}"''' % (xl,injectyl,zl,xa,ya,za)
            print(cmd)
            os.system(cmd)

    elif args.signal == 'ya':
        xl = xl_[int(len(xl_) * args.time/51)] 
        yl = yl_[int(len(xl_) * args.time/51)]
        zl = zl_[int(len(xl_) * args.time/51)]
        xa = xa_[int(len(xl_) * args.time/51)] 
        injectya = ya_[int(len(xl_) * args.time/51)] + args.delta
        za = za_[int(len(xl_) * args.time/51)]
        if args.iter is False:
            cmd = '''rostopic pub --once /twist_raw geometry_msgs/TwistStamped "{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x': %f,'y': %f, 'z': %f}}}"''' % (xl,yl,zl,xa,injectya,za)
            print(cmd)
            os.system(cmd)

    elif args.signal == 'zl':
        xl = xl_[int(len(xl_) * args.time/51)] 
        yl = yl_[int(len(xl_) * args.time/51)]
        injectzl = zl_[int(len(xl_) * args.time/51)] + args.delta
        xa = xa_[int(len(xl_) * args.time/51)] 
        ya = ya_[int(len(xl_) * args.time/51)]
        za = za_[int(len(xl_) * args.time/51)]
        if args.iter is False:
            cmd = '''rostopic pub --once /twist_raw geometry_msgs/TwistStamped "{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x': %f,'y': %f, 'z': %f}}}"''' % (xl,yl,injectzl,xa,ya,za)
            print(cmd)
            os.system(cmd)    

    elif args.signal == 'za':
        xl = xl_[int(len(xl_) * args.time/51)] 
        yl = yl_[int(len(xl_) * args.time/51)]
        zl = zl_[int(len(xl_) * args.time/51)]
        xa = xa_[int(len(xl_) * args.time/51)] 
        ya = ya_[int(len(xl_) * args.time/51)]
        injectza = za[int(len(xl) * args.time/51)] + args.delta
        if args.iter is False:
            cmd = '''rostopic pub --once /twist_raw geometry_msgs/TwistStamped "{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x': %f,'y': %f, 'z': %f}}}"''' % (xl,yl,zl,xa,ya,injectza)
            print(cmd)
            os.system(cmd) 
    else:
        print('inject fault into non-existing variable')
        return
                       
    time.sleep(51-args.time)
    os.kill(pid2,signal.SIGINT)
    os.kill(pid3,signal.SIGINT)

    folder = 'tr-' + args.signal + '-' + str(args.time) + '-' + str(args.delta) 
    cmd = 'mkdir ' + folder
    os.system(cmd)
    cmd = 'mv *.txt ' + folder
    os.system(cmd)
if __name__ == '__main__':
    main()
