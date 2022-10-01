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
    parser.add_argument('--signal', default='xp')
    parser.add_argument('--delta', default=0.1,type=float)
    parser.add_argument('--time', default=12.0,type=float)
    parser.add_argument('--iter', default=False)

    args = parser.parse_args()
    #pdb.set_trace()
    xp_ = np.load('./ndtposebase/x_p.npy')
    xo_ = np.load('./ndtposebase/x_o.npy')
    yp_ = np.load('./ndtposebase/y_p.npy')
    yo_ = np.load('./ndtposebase/y_o.npy')
    zp_ = np.load('./ndtposebase/z_p.npy')
    zo_ = np.load('./ndtposebase/z_o.npy')
    wo_ = np.load('./ndtposebase/w.npy')

    sig = ['xp','xo','yp','yo','zp','zo','wo']
    delay = [12,18,22,24,26,30,36,38,40,42]
    #sig = ['xp']
    for lat in delay:
        for ss in sig:
            for i in range(-10,10,2):
                delta = i * 2
                
                cmd = '''roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:="107,59,0.5,0,0,0"'''
                process1 = subprocess.Popen(cmd,shell=True)
                pid1 = process1.pid
                time.sleep(50)
                cmd = '''rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped "{'header': {'seq': 0, 'stamp': {'secs': 0, 'nsecs': 0}, 'frame_id': "world" }, 'pose': {'position': {'x': 170, 'y': 0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.00720201027314, 'w': 0.999974065188}}}" --once'''
                os.system(cmd)
                process2 = subprocess.Popen('''rostopic echo /vehicle_status > vs.txt ''',shell=True)
                process3 = subprocess.Popen('''rostopic echo /gnss_pose > gnss.txt ''',shell=True)
                pid2 = process2.pid
                pid3 = process3.pid

                time.sleep(lat)
                
                if ss == 'xp':
                    injectxp = xp_[int(len(xp_) * lat/51)] + delta
                    yp = yp_[int(len(xp_) * lat/51)]
                    zp = zp_[int(len(xp_) * lat/51)]
                    xo = xo_[int(len(xp_) * lat/51)]
                    yo = yo_[int(len(xp_) * lat/51)]
                    zo = zo_[int(len(xp_) * lat/51)]
                    wo = wo_[int(len(xp_) * lat/51)]
                    
                    if args.iter is False:
                        cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (injectxp,yp,zp,xo,yo,zo,wo)
                        print(cmd)            
                        os.system(cmd)
                        
                elif ss == 'xo':
                    xp = xp_[int(len(xp_) * lat/51)] 
                    yp = yp_[int(len(xp_) * lat/51)]
                    zp = zp_[int(len(xp_) * lat/51)]
                    injectxo = xo_[int(len(xp_) * lat/51)] + delta
                    yo = yo_[int(len(xp_) * lat/51)]
                    zo = zo_[int(len(xp_) * lat/51)]
                    wo = wo_[int(len(xp_) * lat/51)]
                    if args.iter is False:
                        cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,injectxo,yo,zo,wo)
                        print(cmd)            
                        os.system(cmd)

                elif ss == 'yp':
                    xp = xp_[int(len(xp_) * lat/51)]
                    injectyp = yp_[int(len(xp_) * lat/51)] + delta
                    zp = zp_[int(len(xp_) * lat/51)]
                    xo = xo_[int(len(xp_) * lat/51)]
                    yo = yo_[int(len(xp_) * lat/51)]
                    zo = zo_[int(len(xp_) * lat/51)]
                    wo = wo_[int(len(xp_) * lat/51)]
                    if args.iter is False:
                        cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,injectyp,zp,xo,yo,zo,wo)
                        print(cmd)            
                        os.system(cmd)

                elif ss == 'yo':
                    xp = xp_[int(len(xp_) * lat/51)]
                    yp = yp_[int(len(xp_) * lat/51)]
                    zp = zp_[int(len(xp_) * lat/51)]
                    xo = xo_[int(len(xp_) * lat/51)]
                    injectyo = yo_[int(len(xp_) * lat/51)] + delta
                    zo = zo_[int(len(xp_) * lat/51)]
                    wo = wo_[int(len(xp_) * lat/51)]
                    if args.iter is False:
                        cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,xo,injectyo,zo,wo)
                        print(cmd)            
                        os.system(cmd)

                elif ss == 'zp':
                    xp = xp_[int(len(xp_) * lat/51)]
                    yp = yp_[int(len(xp_) * lat/51)]
                    injectzp = zp_[int(len(xp_) * lat/51)] + delta
                    xo = xo_[int(len(xp_) * lat/51)]
                    yo = yo_[int(len(xp_) * lat/51)]
                    zo = zo_[int(len(xp_) * lat/51)]
                    wo = wo_[int(len(xp_) * lat/51)]
                    if args.iter is False:
                        cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,injectzp,xo,yo,zo,wo)
                        print(cmd)            
                        os.system(cmd)

                elif ss == 'zo':
                    xp = xp_[int(len(xp_) * lat/51)]
                    yp = yp_[int(len(xp_) * lat/51)]
                    zp = zp_[int(len(xp_) * lat/51)] 
                    xo = xo_[int(len(xp_) * lat/51)]
                    yo = yo_[int(len(xp_) * lat/51)]
                    injectzo = zo_[int(len(xp_) * lat/51)] + delta
                    wo = wo_[int(len(xp_) * lat/51)]
                    if args.iter is False:
                        cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,xo,yo,injectzo,wo)
                        print(cmd)            
                        os.system(cmd)

                elif ss == 'wo':
                    xp = xp_[int(len(xp_) * lat/51)]
                    yp = yp_[int(len(xp_) * lat/51)]
                    zp = zp_[int(len(xp_) * lat/51)] 
                    xo = xo_[int(len(xp_) * lat/51)]
                    yo = yo_[int(len(xp_) * lat/51)]
                    zo = zo_[int(len(xp_) * lat/51)] 
                    injectwo = wo_[int(len(xp_) * lat/51)] + delta
                    if args.iter is False:
                        cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,xo,yo,zo,injectwo)
                        print(cmd)            
                        os.system(cmd)
                
                else:
                    print('inject fault into non-existing variable')
                    return

                            
                time.sleep(51-lat)
                os.kill(pid2,signal.SIGINT)
                os.kill(pid3,signal.SIGINT)
                
                folder = 'ndtpose-' + ss + '-' + str(lat) + '-' + str(delta) 
                cmd = 'mkdir ' + folder
                os.system(cmd)
                cmd = 'mv *.txt ' + folder
                os.system(cmd)
                time.sleep(10)
                os.system('rosnode kill -a')
if __name__ == '__main__':
    main()

