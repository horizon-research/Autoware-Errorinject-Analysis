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
import random

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

def parse_vodometry(filepath):

	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []
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
			if 'linear:' in a[i-1]:
				xl.append(float(a[i][9:-1]))
			elif 'angular:' in a[i-1]:
				xa.append(float(a[i][9:-1]))
			elif 'position:' in a[i-1]:
				xp.append(float(a[i][9:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][9:-1]))
		elif 'y' in a[i]:
			if 'linear:' in a[i-2]:
				yl.append(float(a[i][9:-1]))
			elif 'angular:' in a[i-2]:
				ya.append(float(a[i][9:-1]))
			elif 'position:' in a[i-2]:
				yp.append(float(a[i][9:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][9:-1]))
		elif 'z' in a[i]:
			if 'linear:' in a[i-3]:
				zl.append(float(a[i][9:-1]))
			elif 'angular:' in a[i-3]:
				za.append(float(a[i][9:-1]))
			elif 'position:' in a[i-3]:
				zp.append(float(a[i][9:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][9:-1]))
		elif 'w:' in a[i]:
			wo.append(float(a[i][9:-1]))

	return xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za

#def bitflip(x,pos):
#	fs = pack('f',x)
#	bval = list(unpack('BBBB',fs))
#	[q,r] = divmod(pos,8)
#	bval[q] ^= 1 << r
#	fs = pack('BBBB', *bval)
#	fnew=unpack('f',fs)
#	return fnew[0]

def bitflip(ori_num,signal,i):
	if signal == 'xp':
		xp_min = ori_num - 600
		if i==32:
			return ori_num - 3.11
		elif i == 33:
			return ori_num + 1.43
		else:
			return xp_min + 1200/32*i
	if signal == 'yp':
		yp_min = ori_num - 600
		if i==32:
			return ori_num - 0.31
		elif i == 33:
			return ori_num + 2.04
		else:
			return yp_min + 1200/32*i		
	if signal == 'zp':
		zp_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return zp_min + 1200/32*i
	if signal == 'xo':
		xo_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return xo_min + 1200/32*i
	if signal == 'yo':
		yo_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return yo_min + 1200/32*i
	if signal == 'zo':
		zo_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return zo_min + 1200/32*i
	if signal == 'wo':
		wo_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return wo_min + 1200/32*i
	elif signal == 'xl':
		xl_min = ori_num - 600
		if i == 32:
			return ori_num - 5
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return xl_min + 1200/32*i 
	elif signal == 'yl':
		yl_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return yl_min + 1200/32*i
	elif signal == 'zl':
		zl_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return zl_min + 1200/32*i
	elif signal == 'xa':
		xa_min = ori_num - 600
		if i == 32:
			return ori_num - 5
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return xa_min + 1200/32*i 
	elif signal == 'ya':
		ya_min = ori_num - 600
		if i == 32:
			return ori_num - random.randint(1,600)
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return ya_min + 1200/32*i
	elif signal == 'za':
		za_min = ori_num - 600
		if i == 32:
			return ori_num - 6056
		elif i == 33:
			return ori_num + random.randint(1,600)
		else:
			return za_min + 1200/32*i

def parse_finalwp(filepath):

	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []
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
			if 'linear:' in a[i-1]:
				xl.append(float(a[i][17:-1]))
			elif 'angular:' in a[i-1]:
				xa.append(float(a[i][17:-1]))
			elif 'position:' in a[i-1]:
				#pdb.set_trace()
				xp.append(float(a[i][17:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][17:-1]))
		elif 'y' in a[i]:
			if 'linear:' in a[i-2]:
				yl.append(float(a[i][17:-1]))
			elif 'angular:' in a[i-2]:
				ya.append(float(a[i][17:-1]))
			elif 'position:' in a[i-2]:
				yp.append(float(a[i][17:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][17:-1]))
		elif 'z' in a[i]:
			if 'linear:' in a[i-3]:
				zl.append(float(a[i][17:-1]))
			elif 'angular:' in a[i-3]:
				za.append(float(a[i][17:-1]))
			elif 'position:' in a[i-3]:
				zp.append(float(a[i][17:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][17:-1]))
		elif 'w:' in a[i] and 'orientation:' in a[i-4]:
			wo.append(float(a[i][17:-1]))

	return xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za




def main():
	xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za = parse_finalwp('./baseline148/based_lane_waypoints_raw.txt')
	graphs = pydot.graph_from_dot_file("rosgraph.dot")
	graph = graphs[0]
	ntx = networkx.drawing.nx_pydot.from_pydot(graph)
	target = 't___based__lane_waypoints_raw'
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
	#pdb.set_trace()
	signal_attack = ['xp','yp','zp','xo','zo','yo','wo','xl','yl','zl','xa','ya','za']
	#signal_attack = ['yo','xl','yl','zl','xa','ya','za']
	index = int(len(xp)*18/51)
	for sig in signal_attack:
		if sig == 'xp':
			ori_num = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'xp',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (error_num,ype,zpe,xoe,yoe,zoe,woe,xle,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'yp':
			ori_num = yp[index]
			xpe = xp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'yp',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,error_num,zpe,xoe,yoe,zoe,woe,xle,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'zp':
			ori_num = zp[index]
			xpe = xp[index]
			ype = yp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'zp',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,error_num,xoe,yoe,zoe,woe,xle,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'xo':
			ori_num = xo[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'xo',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,error_num,yoe,zoe,woe,xle,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'yo':
			ori_num = yo[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'yo',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,error_num,zoe,woe,xle,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'zo':
			ori_num = zo[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'zo',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,error_num,woe,xle,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'wo':
			ori_num = wo[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'wo',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,zoe,error_num,xle,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'xl':
			ori_num = xl[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'xl',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,zoe,woe,error_num,yle,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'yl':
			ori_num = yl[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]		
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'yl',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,zoe,woe,xle,error_num,zle,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'zl':
			ori_num = zl[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			xae = xa[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'zl',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,zoe,woe,xle,yle,error_num,xae,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'xa':
			ori_num = xa[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			yae = ya[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'xa',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,zoe,woe,xle,yle,zle,error_num,yae,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'ya':
			ori_num = ya[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			zae = za[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'ya',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,zoe,woe,xle,yle,zle,xae,error_num,zae)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
		elif sig == 'za':
			ori_num = za[index]
			xpe = xp[index]
			ype = yp[index]
			zpe = zp[index]
			xoe = xo[index]
			yoe = yo[index]
			zoe = zo[index]
			woe = wo[index]
			xle = xl[index]
			yle = yl[index]
			zle = zl[index]
			xae = xa[index]
			yae = ya[index]
			for i in range(0,34):
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
				error_num = bitflip(ori_num,'za',i)
				cmd = '''rostopic pub --once /based/lane_waypoints_raw autoware_msgs/LaneArray "{'lanes':['waypoints':['twist':{'twist':{'linear':{'x': %f, 'y': %f, 'z': %f},'angular':{'x':%f,'y':%f,'z':%f}}},'pose':{'pose':{'position':{'x':%f, 'y':%f, 'z':%f},'orientation':{'x':%f,'y':%f,'z':%f,'w':%f}}}]]}"''' % (xpe,ype,zpe,xoe,yoe,zoe,woe,xle,yle,zle,xae,yae,error_num)
				os.system(cmd)
				time.sleep(33)
				for t in pid:
					os.kill(t,signal.SIGINT)
		
				folder = target[4:] + '_' + 'attack' + sig + 'bit' + str(i)
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
	

if __name__ == '__main__':
	main()
