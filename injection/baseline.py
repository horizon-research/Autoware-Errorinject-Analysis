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

def bfs(graph,root,terminate):
	queue = []
	visited = set()

	queue.append(root)
	#visited.add(root)

	while len(queue) > 0:
		vertex = queue.pop(0)
		nodes = graph.successors(vertex)
		for w in nodes:
			if w not in visited and w != terminate:
				queue.append(w)
				visited.add(w)
			if w == terminate:
				visited.add(w)
				break

	return visited

def parse_ctrlcmd():

	return ctrlcmd 

def parse_twistcmd():

	return twistcmd 

def parse_vehiclecmd():

	return vehiclecmd

def main():

    echocmd = []
    echocmd.append('rostopic echo /gnss_pose > gnss_pose.txt')
    echocmd.append('rostopic echo /vehicle/odom > vehicle_odom.txt')
    echocmd.append('rostopic echo /filtered_points > filtered_points.txt')
    echocmd.append('rostopic echo /ndt_pose > ndt_pose.txt')
    echocmd.append('rostopic echo /estimate_twist > estimate_twist.txt')
    echocmd.append('rostopic echo /localizer_pose > localizer_pose.txt')
    echocmd.append('rostopic echo /current_pose > current_pose.txt')
    echocmd.append('rostopic echo /current_velocity > current_velocity.txt')
    echocmd.append('rostopic echo /safety_waypoints > safety_waypoints.txt')
    echocmd.append('rostopic echo /final_waypoints > final_waypoints.txt')
    echocmd.append('rostopic echo /stopline_waypoint > stopline_waypoints.txt')
    echocmd.append('rostopic echo /obstacle_waypoint > obstacle_waypoints.txt')
    echocmd.append('rostopic echo /twist_raw > twist_raw.txt')
    echocmd.append('rostopic echo /twist_cmd > twist_cmd.txt')
    echocmd.append('rostopic echo /vehicle_cmd > vehicle_cmd.txt')
    echocmd.append('rostopic echo /lamp_cmd > lamp_cmd.txt')
    echocmd.append('rostopic echo /decision_maker/state > decision_maker_state.txt')
    echocmd.append('rostopic echo /based/lane_waypoints_raw > based_lane_waypoints_raw.txt')
    echocmd.append('rostopic echo /based/lane_waypoints_array > based_lane_waypoints_array.txt')
    echocmd.append('rostopic echo /lane_waypoints_array > lane_waypoints_array.txt')
    echocmd.append('rostopic echo /red_waypoints_array > red_waypoints_array.txt')
    echocmd.append('rostopic echo /green_waypoints_array > green_waypoints_array.txt')
    echocmd.append('rostopic echo /points_no_ground > points_no_ground.txt')
    echocmd.append('rostopic echo /prediction/motion_predictor/objects > prediction_motion_predictor_objects.txt')
    echocmd.append('rostopic echo /detection/fusion_tools/objects > detection_fusion_tools_objects.txt')
    echocmd.append('rostopic echo /detection/image_detector/objects > detection_image_detector_objects.txt')
    echocmd.append('rostopic echo /detection/lidar_tracker/objects > detection_lidar_tracker_objects.txt')
    echocmd.append('rostopic echo /detection/lidar_detector/objects > detection_lidar_detecotr_objects.txt')
    echocmd.append('rostopic echo /detection/image_tracker/objects > detection_image_tracker_objects.txt')
    echocmd.append('rostopic echo /semantics/costmap_generator/occupancy_grid > semantics_costmap_generator_occupancy_grid.txt')
    echocmd.append('rostopic echo /base_waypoints > base_waypoints.txt')
    echocmd.append('rostopic echo /cloest_waypoint > cloest_waypoints.txt')
    echocmd.append('rostopic echo /change_flag > change_flag.txt')
    echocmd.append('rostopic echo /traffic_waypoints_array > traffic_waypoints_array.txt')
    #pdb.set_trace()
    for i in range(2):
        pid = []
        cmd = '''roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:="107,59,0.5,0,0,0"'''
        process1 = subprocess.Popen(cmd,shell=True)
        pid1 = process1.pid
        time.sleep(45)
        cmd = '''rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped "{'header': {'seq': 0, 'stamp': {'secs': 0, 'nsecs': 0}, 'frame_id': "world" }, 'pose': {'position': {'x': 170, 'y': 0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.00720201027314, 'w': 0.999974065188}}}" --once'''
        os.system(cmd)
        for j in echocmd:
            process = subprocess.Popen(j,shell=True)
            pid.append(process.pid)

        for t in pid:
            os.kill(t,signal.SIGINT)
        time.sleep(51)

        folder = 'baseline' + str(i)
        cmd = 'mkdir ' + folder
        os.system(cmd)
        cmd = 'mv *.txt ' + folder
        os.system(cmd)
        time.sleep(5)
        os.system('rosnode kill -a')

if __name__ == '__main__':
    main()