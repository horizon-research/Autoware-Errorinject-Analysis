from struct import *
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
#!/usr/bin/env python
import rosnode
import rosgraph
import sys
import argparse

# lots of things 'borrowed' from rosnode

try:
	from xmlrpc.client import ServerProxy
except ImportError:
	from xmlrpclib import ServerProxy

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

def main():

	graphs = pydot.graph_from_dot_file("rosgraph.dot")
	graph = graphs[0]
	ntx = networkx.drawing.nx_pydot.from_pydot(graph)
	target = 't___vehicle__odom'
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
	for i in range(1,301):
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
		'''
		for node in nodes:
			if node == '/can_odometry':
				node = ServerProxy(node_api)
				pid = rosnode._succeed(node.getPid(ID))
				print ("    PID    : {}".format(pid))
				f = open('pid.txt','w')
				f.write(str(pid))
				f.close()
		'''
		fuck = open('pidckpt','w')
		fuck.write(str(i))
		fuck.close()
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
		cmd = 'zip -r ' + folder + '.zip ' + folder
		os.system(cmd)
		cmd = 'rm -r ' + folder
		os.system(cmd)
	f = open('pidckpt','w')
	f.write('-1')
	f.close()
if __name__ == '__main__':
	main()
