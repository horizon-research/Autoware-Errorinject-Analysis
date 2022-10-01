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

	graphs = pydot.graph_from_dot_file("rosgraph.dot")
	graph = graphs[0]
	ntx = networkx.drawing.nx_pydot.from_pydot(graph)
	target = 't___traffic_waypoints_array'
	terminate = 't___vehicle_cmd'

	#for i in ntx.nodes():
	#	if 'cmd' in i:
	#		print(i)
	for i in ntx.nodes():
		if i == target:
			#pdb.set_trace()
			ss = bfs(ntx,i,terminate)
	for i in ntx.nodes():
		if 'based' in i:
			print(i)
	
	print(ss)
	#pdb.set_trace()
	signal_collect = []
	if target == 't___vehicle__odom':
		signal_collect.append('/vehicle/odom')
	elif target == 't___based__lane_waypoints_raw':
		signal_collect.append('/based/lane_waypoints_raw')
	elif target == 't___based__lane_waypoints_array':
		signal_collect.append('/based/lane_waypoints_array')
	elif target == 't__decision_maker__state':
		signal_collect.append('/decision_maker/state')
	elif target == 't___semantics__costmap_generator__occupancy_grid':
		signal_collect.append('/semantics/costmap_generator/occupancy_grid')
	else:
		signal_collect.append('/'+target[4:])
	for i in ss:
		if 't___' in i:
			signal_collect.append('/'+i[4:])
	
	#collect gt signal for xx times
	#pid = []
	print(signal_collect)
	pdb.set_trace()
	for i in range(3):
		pid = []
		cmd = '''roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:="107,59,0.5,0,0,0"'''
		process1 = subprocess.Popen(cmd,shell=True)
		pid1 = process1.pid
		time.sleep(45)
		cmd = '''rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped "{'header': {'seq': 0, 'stamp': {'secs': 0, 'nsecs': 0}, 'frame_id': "world" }, 'pose': {'position': {'x': 170, 'y': 0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.00720201027314, 'w': 0.999974065188}}}" --once'''
		os.system(cmd)
		
		for j in signal_collect:
			if j == '/vehicle/odom':
				echocmd = 'rostopic echo /vehicle/odom > vehicle_odom.txt'
			elif j == '/based/lane_waypoints_raw':
				echocmd = 'rostopic echo /based/lane_waypoints_raw > base_lane_waypoints.txt'
			elif j == '/decision_maker/state':
				echocmd = 'rostopic echo /decision_maker/state > decision_maker_state.txt'
			elif j == '/semantics/costmap_generator/occupancy_grid':
				echocmd = 'rostopic echo /semantics/costmap_generator/occupancy_grid > semantics_costmap_generator_occupancy_grid.txt'
			elif j == '/based/lane_waypoints_raw':
				echocmd = 'rostopic echo /based/lane_waypoints_raw > based_lane_waypoints_raw.txt'
			elif j == '/based/lane_waypoints_array':
				echocmd = 'rostopic echo /based/lane_waypoints_array > based_lane_waypoints_array.txt'
			else:
				echocmd = "rostopic echo " + j + " > " + j[1:] + ".txt"
			#print(echocmd)
			process = subprocess.Popen(echocmd,shell=True)
			pid.append(process.pid)
		time.sleep(18)
		#cmd = '''rostopic pub --once /twist_raw geometry_msgs/TwistStamped "{'twist':{'linear':{'x': 50.0, 'y': 15.0, 'z': 10.0},'angular':{'x': 0.0,'y': 0.0, 'z': 0.0}}}"'''
		#cmd = '''rostopic pub --once /vehicle/odom nav_msgs/Odometry "{'pose':{'pose':{'position':{'x': 5, 'y': 5, 'z': 5},'orientation':{'x':5.0,'y':5.0,'z':5.0,'w':5.0}}}}" '''
		#cmd = '''rostopic pub --once /vehicle/odom nav_msgs/Odometry "{'twist':{'twist':{'linear':{'x': 5.0, 'y': 5.0, 'z': 5.0},'angular':{'x':5.0,'y':5.0,'z':5.0}}}}"'''
		#cmd = '''rostopic pub --once /ndt_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': 3.0, 'y': 3.0, 'z': 0.0},'orientation':{'x': 3.0,'y': 3.0, 'z': 0, 'w': 0}}}"'''
		#cmd = '''rostopic pub --once /estimate_twist geometry_msgs/TwistStamped "{'twist':{'linear':{'x': 50.0, 'y': 15.0, 'z': 10.0},'angular':{'x': 0.0,'y': 0.0, 'z': 0.0}}}"'''
		#cmd = '''rostopic pub --once /current_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': 3.0, 'y': 3.0, 'z': 0.0},'orientation':{'x': 3.0,'y': 3.0, 'z': 0, 'w': 0}}}"'''
		#cmd = '''rostopic pub --once /current_velocity geometry_msgs/TwistStamped "{'twist':{'linear':{'x': 50.0, 'y': 15.0, 'z': 10.0},'angular':{'x': 0.0,'y': 0.0, 'z': 0.0}}}"'''
		#cmd = '''rostopic pub --once /final_waypoints autoware_msgs/Lane "{'waypoints':['change_flag': 1.0,'dtlane':{'dist': 1.0, 'dir': 1.0, 'apara': 2.0, 'r': 2.0, 'slope': 2.0, 'cant': 2.0, 'lw': 2.0, 'rw': 2.0},'wpstate':{'aid': 1.0, 'lanechange_state': 1.0, 'steering_state': 1.0, 'accel_state': 2.0, 'stop_state': 1.0, 'event_state': 1.0}]}"'''
		#cmd = '''rostopic pub --once /lamp_cmd autoware_msgs/LampCmd "{'l':10.0,'r':10.0}"'''
		#cmd = '''rostopic pub --once /final_waypoints autoware_msgs/Lane "{'waypoints':['twist':{'twist':{'linear':{'x': 15.0, 'y': 15.0, 'z': 15.0},'angular':{'x':15.0,'y':15.0,'z':15.0}}}]}"'''
		#os.system(cmd)
		#cmd = '''rostopic pub --once /final_waypoints autoware_msgs/Lane "{'waypoints':['twist':{'twist':{'linear':{'x': 50.0, 'y': 15.0, 'z': 15.0},'angular':{'x':15.0,'y':15.0,'z':15.0}}}]}"'''
		#cmd = '''rostopic pub --once /vehicle/odom nav_msgs/Odometry "{'twist':{'twist':{'linear':{'x': 10, 'y': 10,'z': 10},'angular':{'x':10.0,'y':10.0,'z':10.0}}}}"'''
		#cmd = '''rostopic pub --once /stopline_waypoint std_msgs/Int32 "{'data':5}"'''
		#cmd = '''rostopic pub --once /obstacle_waypoint std_msgs/Int32 "{'data':5}"'''
		#cmd = '''rostopic pub --once /safety_waypoints autoware_msgs/Lane "{'waypoints':['twist':{'twist':{'linear':{'x': 15.0, 'y': 15.0, 'z': 15.0},'angular':{'x':15.0,'y':15.0,'z':15.0}}}]}"'''
		#cmd = '''rostopic pub --once /detection/image_detector/objects autoware_msgs/DetectedObjectArray "{'objects':['label':car,'score':0.9,'x':0,'y':200,'height':50,'width':80]}"'''
		#injection for occupancygrid
		#cmd = '''rostopic pub --once /semantics/costmap_generator/occupancy_grid nav_msgs/OccupancyGrid "{'data':['''
		#for xx in range(30000):
		#	cmd += str(100) + ','
		#for xx in range(7499):
		#	cmd += str(0) + ','
		#cmd += str(100) + ']}"'
		#injection for points_no_ground
		#cmd = '''rostopic pub --once /points_no_ground sensor_msgs/PointCloud2 "{'data':['''
		#for xx in range(30000):
		#	cmd += str(100) + ','
		#cmd += str(100) + ']}"'
		#cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': 50.0, 'y': 15.0, 'z': 15.0},'angular':{'x':15.0,'y':15.0,'z':15.0}}}]]}"'''
		#cmd = '''rostopic pub --once /change_flag std_msgs/Int32 "{'data':5}"'''
		#cmd = '''rostopic pub --once /gnss_pose geometry_msgs/PoseStamped "{'pose':{'position':{'x': 3.0, 'y': 3.0, 'z': 0.0},'orientation':{'x': 3.0,'y': 3.0, 'z': 0, 'w': 0}}}"'''
		cmd = '''rostopic pub --once /traffic_waypoints_array autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': 50.0, 'y': 15.0, 'z': 15.0},'angular':{'x':15.0,'y':15.0,'z':15.0}}}]]}"'''
		os.system(cmd)
		time.sleep(33)

		for t in pid:
			os.kill(t,signal.SIGINT)
		
		folder = target[4:] + '_' + 'attack' + str(i)
		cmd = 'mkdir ' + folder
		os.system(cmd)
		cmd = 'mv *.txt ' + folder
		os.system(cmd)
		time.sleep(5)
		os.system('rosnode kill -a')


if __name__ == '__main__':
	main()
