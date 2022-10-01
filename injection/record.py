import os
import os
import time
import signal
import subprocess
import pdb
import numpy as np
import argparse

def main():

    cmd = '''roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:="107,59,0.5,0,0,0"'''
    process1 = subprocess.Popen(cmd,shell=True)
    pid1 = process1.pid
    time.sleep(45)
    cmd = '''rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped "{'header': {'seq': 0, 'stamp': {'secs': 0, 'nsecs': 0}, 'frame_id': "world" }, 'pose': {'position': {'x': 170, 'y': 0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.00720201027314, 'w': 0.999974065188}}}" --once'''
    os.system(cmd)


    #process2 = subprocess.Popen('''rostopic echo /detection/image_detector/objects > img_detec.txt ''',shell=True)
    #process3 = subprocess.Popen('''rostopic echo /detection/image_tracker/objects > img_track.txt ''',shell=True)
    #process4 = subprocess.Popen('''rostopic echo /detection/lidar_tracker/objects > lidar_track.txt ''',shell=True)
    #process5 = subprocess.Popen('''rostopic echo /detection/lidar_detector/objects > lidar_detect.txt ''',shell=True)
    #process6 = subprocess.Popen('''rostopic echo /detection/fusion_tools/objects > fusion.txt ''',shell=True)
    #process7 = subprocess.Popen('''rostopic echo /vehicle/odom > vo.txt ''',shell=True)
    #process8 = subprocess.Popen('''rostopic echo /localizer_pose > lp.txt ''',shell=True)
    #process9 = subprocess.Popen('''rostopic echo /estimate_twist > es_twist.txt ''',shell=True)
    #process10 = subprocess.Popen('''rostopic echo /ndt_pose > ndt.txt ''',shell=True)
    #process11 = subprocess.Popen('''rostopic echo /semantics/costmap_generator/occupancy_grid > occp.txt ''',shell=True)
    #process12 = subprocess.Popen('''rostopic echo /prediction/motion_predictor/objects > motion_pred.txt ''',shell=True)
    #process13 = subprocess.Popen('''rostopic echo /current_pose > curr_pose.txt ''',shell=True)
    #process14 = subprocess.Popen('''rostopic echo /obstacle_waypoint > obstacle.txt ''',shell=True)
    #process15 = subprocess.Popen('''rostopic echo /stopline_waypoint > stopwp.txt ''',shell=True)
    #process16 = subprocess.Popen('''rostopic echo /decision_maker/state > destate.txt ''',shell=True)
    #process17 = subprocess.Popen('''rostopic echo /lamp_cmd > lpcmd.txt ''',shell=True)
    #process18 = subprocess.Popen('''rostopic echo /final_waypoints > finalwp.txt ''',shell=True)
    #process19 = subprocess.Popen('''rostopic echo /ctrl_raw > ctraw.txt ''',shell=True)
    #process20 = subprocess.Popen('''rostopic echo /twist_raw > trraw.txt ''',shell=True)
    #process21 = subprocess.Popen('''rostopic echo /twist_cmd > trcmd.txt ''',shell=True)
    #process22 = subprocess.Popen('''rostopic echo /ctrl_cmd > ctcmd.txt ''',shell=True)
    #process23 = subprocess.Popen('''rostopic echo /vehicle_cmd > vhcmd.txt ''',shell=True)
    #process24 = subprocess.Popen('''rostopic echo /cloest_waypoint > clowp.txt ''',shell=True)
    #process25 = subprocess.Popen('''rostopic echo /base_waypoint > bswp.txt ''',shell=True)
    #process26 = subprocess.Popen('''rostopic echo /light_color_managed > ltcol.txt ''',shell=True)
    #process27 = subprocess.Popen('''rostopic echo /red_waypoints_array > redwp.txt ''',shell=True)
    #process28 = subprocess.Popen('''rostopic echo /green_waypoints_array > greenwp.txt ''',shell=True)
    process29 = subprocess.Popen('''rostopic echo /safety_waypoints > sfwp.txt''', shell = True)

    time.sleep(51)

    cmd = 'rosnode kill -a'
    os.system(cmd)
    '''
    /detection/image_detector/objects
    /detection/image_tracker/objects
    /detection/lidar_tracker/objects
    /detection/lidar_detector/objects
    /detection/fusion_tools/objects
    /vehicle/odom
    /localizer_pose
    /estimate_twist
    /ndt_pose
    /semantics/costmap_generator/occupancy_grid
    /prediction/motion_predictor/objects
    /current_pose
    /obstacle_waypoint
    /stopline_waypoint
    /decision_maker/state
    /lamp_cmd
    /final_waypoints
    /ctrl_raw
    /twist_raw
    /twist_cmd
    /ctrl_cmd
    /vehicle_cmd
    /cloest_waypoint
    /base_waypoint
    /light_color_managed
    /red_waypoints_array
    /green_waypoints_array
    '''
if __name__ == '__main__':
    main()


