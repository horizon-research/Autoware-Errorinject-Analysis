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

def parse_ctrlcmd(filepath):


	return 0 

def parse_twistcmd(filepath):

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
			if 'linear' in a[i-1]:
				xl.append(float(a[i][7:-1]))
			elif 'angular' in a[i-1]:
				xa.append(float(a[i][7:-1]))
		elif 'y' in a[i]:
			if 'linear' in a[i-2]:
				yl.append(float(a[i][7:-1]))
			elif 'angular' in a[i-2]:
				ya.append(float(a[i][7:-1]))
		elif 'z' in a[i]:
			if 'linear' in a[i-3]:
				zl.append(float(a[i][7:-1]))
			elif 'angular' in a[i-3]:
				za.append(float(a[i][7:-1]))

	return xl,yl,zl,xa,ya,za 

def parse_twistraw(filepath):

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
			if 'linear' in a[i-1]:
				xl.append(float(a[i][7:-1]))
			elif 'angular' in a[i-1]:
				xa.append(float(a[i][7:-1]))
		elif 'y' in a[i]:
			if 'linear' in a[i-2]:
				yl.append(float(a[i][7:-1]))
			elif 'angular' in a[i-2]:
				ya.append(float(a[i][7:-1]))
		elif 'z' in a[i]:
			if 'linear' in a[i-3]:
				zl.append(float(a[i][7:-1]))
			elif 'angular' in a[i-3]:
				za.append(float(a[i][7:-1]))

	return xl,yl,zl,xa,ya,za

def parse_vehiclecmd(filepath):

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

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'steer:' in a[i]:
			steer_cmd.append(float(a[i][9:-1]))
		elif 'accel:' in a[i]:
			accel_cmd.append(float(a[i][9:-1]))
		elif 'brake:' in a[i]:
			brake_cmd.append(float(a[i][9:-1]))
		elif 'l:' in a[i] and 'accel:' not in a[i]:
			#pdb.set_trace()
			lamp_cmd_l.append(float(a[i][5:-1]))
		elif 'r:' in a[i] and 'l' in a[i-1] and 'der' not in a[i]:
			#pdb.set_trace()
			lamp_cmd_r.append(float(a[i][5:-1]))
		elif 'gear:' in a[i]:
			gear_cmd.append(float(a[i][8:-1]))
		elif 'mode:' in a[i]:
			mode.append(float(a[i][6:-1]))
		elif 'x' in a[i]:
			if 'linear' in a[i-1]:
				xl.append(float(a[i][9:-1]))
			elif 'angular' in a[i-1]:
				xa.append(float(a[i][9:-1]))
		elif 'y' in a[i] and 'emergency' not in a[i]:
			if 'linear' in a[i-2]:
				yl.append(float(a[i][9:-1]))
			elif 'angular' in a[i-2]:
				ya.append(float(a[i][9:-1]))
		elif 'z' in a[i]:
			if 'linear' in a[i-3]:
				zl.append(float(a[i][9:-1]))
			elif 'angular' in a[i-3]:
				za.append(float(a[i][9:-1]))

	return steer_cmd, accel_cmd, brake_cmd, lamp_cmd_l, lamp_cmd_r, gear_cmd, mode, xl, xa, yl, ya, zl, za

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

def parse_stopwp(filepath):

	data = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'data:' in a[i]:
			data.append(float(a[i][6:-1]))

	return data

def parse_redwp(filepath):

	return 0

def parse_occp(filepath):

	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	data = []
	width = []
	height = []
	reso = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x:' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(float(a[i][9:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][9:-1]))
		elif 'y:' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(float(a[i][9:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][9:-1]))
		elif 'z:' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(float(a[i][9:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][9:-1]))
		elif 'w:' in a[i]:
			wo.append(float(a[i][9:-1]))
		elif 'data:' in a[i]:
			li = a[i][7:-2].split(',')
			temp = []
			for j in li:
				temp.append(float(j))
			data.append(temp)
		elif 'width:' in a[i]:
			width.append(float(a[i][9:-1]))
		elif 'height' in a[i]:
			height.append(float(a[i][9:-1]))
		elif 'resolution:' in a[i]:
			reso.append(float(a[i][14:-1]))

	return xp,yp,zp,xo,yo,zo,wo	

def parse_obstacle(filepath):

	data = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'data:' in a[i]:
			data.append(float(a[i][6:-1]))

	return data

def parse_ndt(filepath):

	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(float(a[i][7:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][7:-1]))
		elif 'y' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(float(a[i][7:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][7:-1]))
		elif 'z' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(float(a[i][7:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][7:-1]))
		elif 'w:' in a[i]:
			wo.append(float(a[i][7:-1]))

	return xp,yp,zp,xo,yo,zo,wo

def parse_ltcol(filepath):

	return 0

def parse_lpcmd(filepath):

	l = []
	r = []

	file = open(filepath,'r')
	a = file.readlines()
	for i in range(len(a)):
		if 'r:' in a[i] and 'header:' not in a[i]:
			r.append(float(a[i][3:-1]))
		if 'l:' in a[i]:
			l.append(float(a[i][3:-1]))
	return l,r

def parse_lp(filepath):

	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(float(a[i][7:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][7:-1]))
		elif 'y' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(float(a[i][7:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][7:-1]))
		elif 'z' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(float(a[i][7:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][7:-1]))
		elif 'w:' in a[i]:
			wo.append(float(a[i][7:-1]))

	return xp,yp,zp,xo,yo,zo,wo	

def parse_lidar_track(filepath):

	label = []
	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []
	xd = []
	yd = []
	zd = []
	xva = []
	yva = []
	zva = []
	xlv = []
	ylv = []
	zlv = []
	xav = []
	yav = []
	zav = []
	xla = []
	yla = []
	zla = []
	xaa = []
	yaa = []
	zaa = []
	data = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x:' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-1]:
				xd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-1]:
				xa.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-1] and 'velocity:' in a[i-2]:
				xlv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-1] and 'velocity:' in a[i-6]:
				xav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-1] and 'acceleration:' in a[i-2]:
				xla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-1] and 'acceleration:' in a[i-6]:
				xaa.append(float(a[i][11:-1]))
		elif 'y:' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-2]:
				yd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-2]:
				ya.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-2] and 'velocity:' in a[i-3]:
				ylv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-2] and 'velocity:' in a[i-7]:
				yav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-2] and 'acceleration:' in a[i-3]:
				yla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-2] and 'acceleration:' in a[i-7]:
				yaa.append(float(a[i][11:-1]))
		elif 'z:' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-3]:
				zd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-3]:
				za.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-3] and 'velocity:' in a[i-4]:
				zlv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-3] and 'velocity:' in a[i-8]:
				zav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-3] and 'acceleration:' in a[i-4]:
				zla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-3] and 'acceleration:' in a[i-8]:
				zaa.append(float(a[i][11:-1]))	
		elif 'w:' in a[i]:
			wo.append(float(a[i][11:-1]))
		elif 'data:' in a[i]:
			li = a[i][12:-2].split(',')
			temp = []
			for j in li:
				temp.append(float(j))
			data.append(temp)


	return xp, yp, zp, xo, yo, zo, wo, xd, yd, zd, xva, yav, zva, xlv, ylv, zlv, xav, yav, zav, xla, yla, zla, xaa, yaa, zaa, data

def parse_lidar_detect(filepath):

	label = []
	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []
	xd = []
	yd = []
	zd = []
	xva = []
	yva = []
	zva = []
	xlv = []
	ylv = []
	zlv = []
	xav = []
	yav = []
	zav = []
	xla = []
	yla = []
	zla = []
	xaa = []
	yaa = []
	zaa = []
	data = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x:' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-1]:
				xd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-1]:
				xa.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-1] and 'velocity:' in a[i-2]:
				xlv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-1] and 'velocity:' in a[i-6]:
				xav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-1] and 'acceleration:' in a[i-2]:
				xla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-1] and 'acceleration:' in a[i-6]:
				xaa.append(float(a[i][11:-1]))
		elif 'y:' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-2]:
				yd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-2]:
				ya.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-2] and 'velocity:' in a[i-3]:
				ylv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-2] and 'velocity:' in a[i-7]:
				yav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-2] and 'acceleration:' in a[i-3]:
				yla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-2] and 'acceleration:' in a[i-7]:
				yaa.append(float(a[i][11:-1]))
		elif 'z:' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-3]:
				zd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-3]:
				za.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-3] and 'velocity:' in a[i-4]:
				zlv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-3] and 'velocity:' in a[i-8]:
				zav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-3] and 'acceleration:' in a[i-4]:
				zla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-3] and 'acceleration:' in a[i-8]:
				zaa.append(float(a[i][11:-1]))	
		elif 'w:' in a[i]:
			wo.append(float(a[i][11:-1]))
		elif 'data:' in a[i]:
			li = a[i][12:-2].split(',')
			temp = []
			for j in li:
				temp.append(float(j))
			data.append(temp)


	return xp, yp, zp, xo, yo, zo, wo, xd, yd, zd, xva, yav, zva, xlv, ylv, zlv, xav, yav, zav, xla, yla, zla, xaa, yaa, zaa, data


def parse_image_track(filepath):

	return 0

def parse_image_detec(filepath):

	return 0

def parse_greenwp(filepath):

	return 0

def parse_fusion(filepath):
	label = []
	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []
	xd = []
	yd = []
	zd = []
	xva = []
	yva = []
	zva = []
	xlv = []
	ylv = []
	zlv = []
	xav = []
	yav = []
	zav = []
	xla = []
	yla = []
	zla = []
	xaa = []
	yaa = []
	zaa = []
	data = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x:' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-1]:
				xd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-1]:
				xa.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-1] and 'velocity:' in a[i-2]:
				xlv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-1] and 'velocity:' in a[i-6]:
				xav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-1] and 'acceleration:' in a[i-2]:
				xla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-1] and 'acceleration:' in a[i-6]:
				xaa.append(float(a[i][11:-1]))
		elif 'y:' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-2]:
				yd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-2]:
				ya.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-2] and 'velocity:' in a[i-3]:
				ylv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-2] and 'velocity:' in a[i-7]:
				yav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-2] and 'acceleration:' in a[i-3]:
				yla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-2] and 'acceleration:' in a[i-7]:
				yaa.append(float(a[i][11:-1]))
		elif 'z:' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(float(a[i][11:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][11:-1]))
			elif 'dimensions:' in a[i-3]:
				zd.append(float(a[i][9:-1]))
			elif 'variance:' in a[i-3]:
				za.append(float(a[i][9:-1]))
			elif 'linear:' in a[i-3] and 'velocity:' in a[i-4]:
				zlv.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-3] and 'velocity:' in a[i-8]:
				zav.append(float(a[i][11:-1]))
			elif 'linear:' in a[i-3] and 'acceleration:' in a[i-4]:
				zla.append(float(a[i][11:-1]))
			elif 'angular:' in a[i-3] and 'acceleration:' in a[i-8]:
				zaa.append(float(a[i][11:-1]))	
		elif 'w:' in a[i]:
			wo.append(float(a[i][11:-1]))
		elif 'data:' in a[i]:
			li = a[i][12:-2].split(',')
			temp = []
			for j in li:
				temp.append(float(j))
			data.append(temp)


	return xp, yp, zp, xo, yo, zo, wo, xd, yd, zd, xva, yav, zva, xlv, ylv, zlv, xav, yav, zav, xla, yla, zla, xaa, yaa, zaa, data


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
	dist = []
	dir_ = []
	apara = []
	r = []
	slope = []
	cant = []
	lw = []
	rw = []
	change_flag = []
	aid = []
	lanechange_state = []
	steering_state = []
	accel_state = []
	stop_state = []
	event_state = []
	lane_id = []
	left_lane_id = []
	right_lane_id = []
	stop_line_id = []
	cost = []
	time_cost = []
	direction = []


	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x:' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(float(a[i][13:-1]))
			elif 'orientation:' in a[i-1]:
				xo.append(float(a[i][13:-1]))
			elif 'linear:' in a[i-1]:
				xl.append(a[i][13:-1])
			elif 'angular:' in a[i-1]:
				xa.append(a[i][13:-1])
		elif 'y:' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(float(a[i][13:-1]))
			elif 'orientation:' in a[i-2]:
				yo.append(float(a[i][13:-1]))
			elif 'linear:' in a[i-2]:
				yl.append(a[i][13:-1])
			elif 'angular:' in a[i-2]:
				ya.append(a[i][13:-1])
		elif 'z:' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(float(a[i][13:-1]))
			elif 'orientation:' in a[i-3]:
				zo.append(float(a[i][13:-1]))
			elif 'linear:' in a[i-3]:
				zl.append(a[i][13:-1])
			elif 'angular:' in a[i-3]:
				za.append(a[i][13:-1])
		elif 'w:' in a[i]:
			wo.append(float(a[i][13:-1]))

	return 0

def parse_es_twist(filepath):

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
				xl.append(round(float(a[i][7:-1]),1))
			elif 'angular:' in a[i-1]:
				xa.append(round(float(a[i][7:-1]),1))
		elif 'y' in a[i]:
			if 'linear:' in a[i-2]:
				yl.append(round(float(a[i][7:-1]),1))
			elif 'angular:' in a[i-2]:
				ya.append(round(float(a[i][7:-1]),1))
		elif 'z' in a[i]:
			if 'linear:' in a[i-3]:
				zl.append(round(float(a[i][7:-1]),1))
			elif 'angular:' in a[i-3]:
				za.append(round(float(a[i][7:-1]),1))	

	return xl,yl,zl,xa,ya,za

def parse_destate(filepath):
	data = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'data:' in a[i]:
			data.append((a[i][6:-1]))

	return data

def parse_curr_pose(filepath):

	xp = []
	yp = []
	zp = []
	xo = []
	yo = []
	zo = []
	wo = []

	file = open(filepath,'r')
	a = file.readlines()

	for i in range(len(a)):
		if 'x' in a[i]:
			if 'position:' in a[i-1]:
				xp.append(round(float(a[i][7:-1]),1))
			elif 'orientation:' in a[i-1]:
				xo.append(round(float(a[i][7:-1]),1))
		elif 'y' in a[i]:
			if 'position:' in a[i-2]:
				yp.append(round(float(a[i][7:-1]),1))
			elif 'orientation:' in a[i-2]:
				yo.append(round(float(a[i][7:-1]),1))
		elif 'z' in a[i]:
			if 'position:' in a[i-3]:
				zp.append(round(float(a[i][7:-1]),1))
			elif 'orientation:' in a[i-3]:
				zo.append(round(float(a[i][7:-1]),1))
		elif 'w:' in a[i]:
			wo.append(round(float(a[i][7:-1]),1))

	return xp,yp,zp,xo,yo,zo,wo

def parse_curr_velo(filepath):

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
				xl.append(round(float(a[i][7:-1]),1))
			elif 'angular:' in a[i-1]:
				xa.append(round(float(a[i][7:-1]),1))
		elif 'y' in a[i]:
			if 'linear:' in a[i-2]:
				yl.append(round(float(a[i][7:-1]),1))
			elif 'angular:' in a[i-2]:
				ya.append(round(float(a[i][7:-1]),1))
		elif 'z' in a[i]:
			if 'linear:' in a[i-3]:
				zl.append(round(float(a[i][7:-1]),1))
			elif 'angular:' in a[i-3]:
				za.append(round(float(a[i][7:-1]),1))

	return xl,yl,zl,xa,ya,za

	



	