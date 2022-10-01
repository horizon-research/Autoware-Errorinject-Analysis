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
    xp_ = np.load('./vo_raw/xp.npy')
    xo_ = np.load('./vo_raw/xo.npy')
    yp_ = np.load('./vo_raw/yp.npy')
    yo_ = np.load('./vo_raw/yo.npy')
    zp_ = np.load('./vo_raw/zp.npy')
    zo_ = np.load('./vo_raw/zo.npy')
    wo_ = np.load('./vo_raw/wo.npy')

    sig = ['xp','xo','yp','yo','wo']
    delay = [18,22,24,25,26,28,30,36]
    error = [0.5]
    #sig = ['xp']
    #delay = [18]
    for lat in delay:
        for ss in sig:
            for i in range(1):
                for delta in error:
                    cmd = '''roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:="107,59,0.5,0,0,0"'''
                    process1 = subprocess.Popen(cmd,shell=True)
                    pid1 = process1.pid
                    time.sleep(45)
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
                            cmd = '''rostopic pub -r 30 /vehicle/odom nav_msgs/Odometry "{'pose':{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}}"''' % (injectxp,yp,zp,xo,yo,zo,wo)
                            f = open('error_inject.txt','w')
                            f.write(str(injectxp)+'\n')
                            f.write(str(yp)+'\n')
                            f.write(str(zp)+'\n')
                            f.write(str(xo)+'\n')
                            f.write(str(yo)+'\n')
                            f.write(str(zo)+'\n')
                            f.write(str(wo)+'\n')            
                            #os.system(cmd)
                            process4 = subprocess.Popen(cmd,shell=True)
                            pid4 = process4.pid
                            time.sleep(1)
                            os.kill(pid3,signal.SIGINT)
                            
                    elif ss == 'xo':
                        xp = xp_[int(len(xp_) * lat/51)] 
                        yp = yp_[int(len(xp_) * lat/51)]
                        zp = zp_[int(len(xp_) * lat/51)]
                        injectxo = xo_[int(len(xp_) * lat/51)] + delta
                        yo = yo_[int(len(xp_) * lat/51)]
                        zo = zo_[int(len(xp_) * lat/51)]
                        wo = wo_[int(len(xp_) * lat/51)]
                        if args.iter is False:
                            cmd = '''rostopic pub -r 30 /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,injectxo,yo,zo,wo)
                            f = open('error_inject.txt','w')
                            f.write(str(xp)+'\n')
                            f.write(str(yp)+'\n')
                            f.write(str(zp)+'\n')
                            f.write(str(injectxo)+'\n')
                            f.write(str(yo)+'\n')
                            f.write(str(zo)+'\n')
                            f.write(str(wo)+'\n')              
                            process4 = subprocess.Popen(cmd,shell=True)
                            pid4 = process4.pid
                            time.sleep(1)
                            os.kill(pid3,signal.SIGINT)

                    elif ss == 'yp':
                        xp = xp_[int(len(xp_) * lat/51)]
                        injectyp = yp_[int(len(xp_) * lat/51)] + delta
                        zp = zp_[int(len(xp_) * lat/51)]
                        xo = xo_[int(len(xp_) * lat/51)]
                        yo = yo_[int(len(xp_) * lat/51)]
                        zo = zo_[int(len(xp_) * lat/51)]
                        wo = wo_[int(len(xp_) * lat/51)]
                        if args.iter is False:
                            cmd = '''rostopic pub -r 30 /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,injectyp,zp,xo,yo,zo,wo)
                            f = open('error_inject.txt','w')
                            f.write(str(xp)+'\n')
                            f.write(str(injectyp)+'\n')
                            f.write(str(zp)+'\n')
                            f.write(str(xo)+'\n')
                            f.write(str(yo)+'\n')
                            f.write(str(zo)+'\n')
                            f.write(str(wo)+'\n')              
                            process4 = subprocess.Popen(cmd,shell=True)
                            pid4 = process4.pid
                            time.sleep(1)
                            os.kill(pid3,signal.SIGINT)

                    elif ss == 'yo':
                        xp = xp_[int(len(xp_) * lat/51)]
                        yp = yp_[int(len(xp_) * lat/51)]
                        zp = zp_[int(len(xp_) * lat/51)]
                        xo = xo_[int(len(xp_) * lat/51)]
                        injectyo = yo_[int(len(xp_) * lat/51)] + delta
                        zo = zo_[int(len(xp_) * lat/51)]
                        wo = wo_[int(len(xp_) * lat/51)]
                        if args.iter is False:
                            cmd = '''rostopic pub -r 30 /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,xo,injectyo,zo,wo)
                            f = open('error_inject.txt','w')
                            f.write(str(xp)+'\n')
                            f.write(str(yp)+'\n')
                            f.write(str(zp)+'\n')
                            f.write(str(xo)+'\n')
                            f.write(str(injectyo)+'\n')
                            f.write(str(zo)+'\n')
                            f.write(str(wo)+'\n')  
                            process4 = subprocess.Popen(cmd,shell=True)
                            pid4 = process4.pid
                            time.sleep(1)
                            os.kill(pid3,signal.SIGINT)

                    elif ss == 'zp':
                        xp = xp_[int(len(xp_) * lat/51)]
                        yp = yp_[int(len(xp_) * lat/51)]
                        injectzp = zp_[int(len(xp_) * lat/51)] + delta
                        xo = xo_[int(len(xp_) * lat/51)]
                        yo = yo_[int(len(xp_) * lat/51)]
                        zo = zo_[int(len(xp_) * lat/51)]
                        wo = wo_[int(len(xp_) * lat/51)]
                        if args.iter is False:
                            cmd = '''rostopic pub -r 30 /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,injectzp,xo,yo,zo,wo)
                            f = open('error_inject.txt','w')
                            f.write(str(xp)+'\n')
                            f.write(str(yp)+'\n')
                            f.write(str(injectzp)+'\n')
                            f.write(str(xo)+'\n')
                            f.write(str(yo)+'\n')
                            f.write(str(zo)+'\n')
                            f.write(str(wo)+'\n')              
                            process4 = subprocess.Popen(cmd,shell=True)
                            pid4 = process4.pid
                            time.sleep(1)
                            os.kill(pid3,signal.SIGINT)

                    elif ss == 'zo':
                        xp = xp_[int(len(xp_) * lat/51)]
                        yp = yp_[int(len(xp_) * lat/51)]
                        zp = zp_[int(len(xp_) * lat/51)] 
                        xo = xo_[int(len(xp_) * lat/51)]
                        yo = yo_[int(len(xp_) * lat/51)]
                        injectzo = zo_[int(len(xp_) * lat/51)] + delta
                        wo = wo_[int(len(xp_) * lat/51)]
                        if args.iter is False:
                            cmd = '''rostopic pub -r 30 /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,xo,yo,injectzo,wo)
                            f = open('error_inject.txt','w')
                            f.write(str(xp)+'\n')
                            f.write(str(yp)+'\n')
                            f.write(str(zp)+'\n')
                            f.write(str(xo)+'\n')
                            f.write(str(yo)+'\n')
                            f.write(str(injectzo)+'\n')
                            f.write(str(wo)+'\n')              
                            process4 = subprocess.Popen(cmd,shell=True)
                            pid4 = process4.pid
                            time.sleep(1)
                            os.kill(pid3,signal.SIGINT)

                    elif ss == 'wo':
                        xp = xp_[int(len(xp_) * lat/51)]
                        yp = yp_[int(len(xp_) * lat/51)]
                        zp = zp_[int(len(xp_) * lat/51)] 
                        xo = xo_[int(len(xp_) * lat/51)]
                        yo = yo_[int(len(xp_) * lat/51)]
                        zo = zo_[int(len(xp_) * lat/51)] 
                        injectwo = wo_[int(len(xp_) * lat/51)] + delta
                        if args.iter is False:
                            cmd = '''rostopic pub -r 30 /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': %f, 'y': %f, 'z': %f},'orientation':{'x': %f,'y': %f, 'z': %f, 'w': %f}}}"''' % (xp,yp,zp,xo,yo,zo,injectwo)
                            f = open('error_inject.txt','w')
                            f.write(str(xp)+'\n')
                            f.write(str(yp)+'\n')
                            f.write(str(zp)+'\n')
                            f.write(str(xo)+'\n')
                            f.write(str(yo)+'\n')
                            f.write(str(zo)+'\n')
                            f.write(str(injectwo)+'\n')              
                            process4 = subprocess.Popen(cmd,shell=True)
                            pid4 = process4.pid
                            time.sleep(1)
                            os.kill(pid3,signal.SIGINT)
                    
                    else:
                        print('inject fault into non-existing variable')
                        return

                                
                    time.sleep(51-lat)
                    os.kill(pid2,signal.SIGINT)
                    os.kill(pid3,signal.SIGINT)
                    
                    folder = 'vo-' + ss + '-' + str(lat) + '-' + str(delta) + '-' + str(i)
                    cmd = 'mkdir ' + folder
                    os.system(cmd)
                    cmd = 'mv *.txt ' + folder
                    os.system(cmd)
                    time.sleep(5)
                    os.system('rosnode kill -a')
if __name__ == '__main__':
    main()