import os
import os
import time
import signal
import subprocess

def main():
    cmd = '''rostopic pub -r 30 /vehicle/odom nav_msgs/Odometry "{'pose':{'pose':{'position':{'x': 5, 'y': 5, 'z': 5}}}}" '''
    #os.system(cmd)
    #process1 = subprocess.Popen(cmd,shell=True)
    process2 = subprocess.Popen('''rostopic echo /vehicle_status > vs_odom.txt ''',shell=True)
    process3 = subprocess.Popen('''rostopic echo /gnss_pose > gnss_odom.txt ''',shell=True)
    #pid1 = process1.pid
    pid2 = process2.pid
    pid3 = process3.pid
    time.sleep(3)
    #os.kill(pid1,signal.SIGINT)
    time.sleep(16)
    #process1 = subprocess.Popen(cmd,shell=True)
    #pid1 = process1.pid
    time.sleep(3)
    #os.kill(pid1,signal.SIGINT)
    time.sleep(16)
    #process1 = subprocess.Popen(cmd,shell=True)
    #pid1 = process1.pid
    time.sleep(3)
    #os.kill(pid1,signal.SIGINT)
    time.sleep(10)
    os.kill(pid2,signal.SIGINT)
    os.kill(pid3,signal.SIGINT)   



if __name__ == '__main__':
    main()
