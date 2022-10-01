from struct import *
import signal
import subprocess
import pdb
import numpy as np
import argparse
import pickle
import gzip
import os
from os import walk

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
		if 'x:' in a[i]:
			if 'linear:' in a[i-1]:
				xl.append(float(a[i][7:-1]))
			elif 'angular:' in a[i-1]:
				xa.append(float(a[i][7:-1]))
		elif 'y:' in a[i]:
			if 'linear:' in a[i-2]:
				yl.append(float(a[i][7:-1]))
			elif 'angular:' in a[i-2]:
				ya.append(float(a[i][7:-1]))	
		elif 'z:' in a[i]:
			if 'linear:' in a[i-3]:
				zl.append(float(a[i][7:-1]))
			elif 'angular:' in a[i-3]:
				za.append(float(a[i][7:-1]))		

	return xl,yl,zl,xa,ya,za

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
		if 'x:' in a[i]:
			if 'linear:' in a[i-1]:
				xl.append(float(a[i][7:-1]))
			elif 'angular:' in a[i-1]:
				xa.append(float(a[i][7:-1]))
		elif 'y:' in a[i]:
			if 'linear:' in a[i-2]:
				yl.append(float(a[i][7:-1]))
			elif 'angular:' in a[i-2]:
				ya.append(float(a[i][7:-1]))	
		elif 'z:' in a[i]:
			if 'linear:' in a[i-3]:
				zl.append(float(a[i][7:-1]))
			elif 'angular:' in a[i-3]:
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
			lamp_cmd_l.append(float(a[i][5:-1]))
		elif 'r:' in a[i] and 'header' not in a[i] and 'steer' not in a[i] and 'gear' not in a[i] and 'linear' not in a[i] and 'angular' not in a[i]:
			#pdb.set_trace()
			lamp_cmd_r.append(float(a[i][5:-1]))
		elif 'gear:' in a[i]:
			gear_cmd.append(float(a[i][8:-1]))
		elif 'mode:' in a[i]:
			mode.append(float(a[i][6:-1]))
		elif 'x' in a[i]:
			if 'linear' in a[i-1]:
				#pdb.set_trace()
				xl.append(float(a[i][9:-1]))
			elif 'angular' in a[i-1]:
				xa.append(float(a[i][9:-1]))
		elif 'y' in a[i] and 'emergency'not in a[i]:
			if 'linear' in a[i-2]:
				#pdb.set_trace()
				yl.append(float(a[i][9:-1]))
			elif 'angular' in a[i-2]:
				ya.append(float(a[i][9:-1]))
		elif 'z' in a[i]:
			if 'linear' in a[i-3]:
				zl.append(float(a[i][9:-1]))
			elif 'angular' in a[i-3]:
				za.append(float(a[i][9:-1]))

	return steer_cmd, accel_cmd, brake_cmd, lamp_cmd_l, lamp_cmd_r, gear_cmd, mode, xl, xa, yl, ya, zl, za

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

def main():
	parser = argparse.ArgumentParser(description="base folder, save dir and database query")
	parser.add_argument('--base', default='base0125')
	parser.add_argument('--save', default='vehicle_cmd.pkl')
	parser.add_argument('--signal', default='vehicle_cmd')
	#pdb.set_trace()
	args = parser.parse_args()
	if os.path.exists(args.save):
		file = gzip.GzipFile(args.save, 'rb')
		data = pickle.load(file)
		file.close()
		if args.signal == 'gnss_pose':
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo = parse_curr_pose(f[i][:-4]+'/gnss_pose.txt')
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()
		if args.signal == 'vehicle_odom':
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				#cmd = 'unzip ' + args.base + '/' + f[i]
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za = parse_vodometry(f[i][:-4]+'/vehicle_odom.txt')
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				data['xl'].append(xl)
				data['yl'].append(yl)
				data['zl'].append(zl)
				data['xa'].append(xa)
				data['ya'].append(ya)
				data['za'].append(za)
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
		if args.signal == 'ndt_pose':
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo = parse_ndt(f[i][:-4]+'/ndt_pose.txt')
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()
		if args.signal == 'vehicle_cmd':
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				pdb.set_trace()
				os.system(cmd)
				rawfile = []
				steer_cmd, accel_cmd, brake_cmd, lamp_cmd_l, lamp_cmd_r, gear_cmd, mode, xl, xa, yl, ya, zl, za = parse_vehiclecmd(f[i][:-4]+'/vehicle_cmd.txt')
				data['steer_cmd'].append(steer_cmd)
				data['accel_cmd'].append(accel_cmd)
				data['brake_cmd'].append(brake_cmd)
				data['lamp_cmd_l'].append(lamp_cmd_l)
				data['lamp_cmd_r'].append(lamp_cmd_r)
				data['gear_cmd'].append(gear_cmd)
				data['mode'].append(mode)
				data['xl'].append(xl)
				data['yl'].append(yl)
				data['zl'].append(zl)
				data['xa'].append(xa)
				data['ya'].append(ya)
				data['za'].append(za)
	else:
		if args.signal == 'gnss_pose':
			data = {'xp':[],'yp':[],'zp':[],'xo':[],'yo':[],'zo':[],'wo':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo = parse_curr_pose(f[i][:-4]+'/gnss_pose.txt')
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()
		if args.signal == 'vehicle_odom':
			data = {'xp':[],'yp':[],'zp':[],'xo':[],'yo':[],'zo':[],'wo':[],'xl':[],'yl':[],'zl':[],'xa':[],'ya':[],'za':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				#cmd = 'unzip ' + args.base + '/' + f[i]
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za = parse_vodometry(f[i][:-4]+'/vehicle_odom.txt')
				#pdb.set_trace()
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				data['xl'].append(xl)
				data['yl'].append(yl)
				data['zl'].append(zl)
				data['xa'].append(xa)
				data['ya'].append(ya)
				data['za'].append(za)
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
		if args.signal == 'ndt_pose':
			data = {'xp':[],'yp':[],'zp':[],'xo':[],'yo':[],'zo':[],'wo':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo = parse_ndt(f[i][:-4]+'/ndt_pose.txt')
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()
		if args.signal == 'es_twist':
			data = {'xa':[],'ya':[],'za':[],'xl':[],'yl':[],'zl':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xa,ya,za,xl,yl,zl = parse_es_twist(f[i][:-4]+'/estimate_twist.txt')
				data['xa'].append(xa)
				data['ya'].append(ya)
				data['za'].append(za)
				data['xl'].append(xl)
				data['yl'].append(yl)
				data['zl'].append(zl)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()
		if args.signal == 'localizer_pose':
			data = {'xp':[],'yp':[],'zp':[],'xo':[],'yo':[],'zo':[],'wo':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo = parse_curr_pose(f[i][:-4]+'/localizer_pose.txt')
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()
		if args.signal == 'pose_relay':
			data = {'xp':[],'yp':[],'zp':[],'xo':[],'yo':[],'zo':[],'wo':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xp,yp,zp,xo,yo,zo,wo = parse_curr_pose(f[i][:-4]+'/current_pose.txt')
				data['xp'].append(xp)
				data['yp'].append(yp)
				data['zp'].append(zp)
				data['xo'].append(xo)
				data['yo'].append(yo)
				data['zo'].append(zo)
				data['wo'].append(wo)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()	
		if args.signal == 'vel_relay':
			data = {'xa':[],'ya':[],'za':[],'xl':[],'yl':[],'zl':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				xa,ya,za,xl,yl,zl = parse_es_twist(f[i][:-4]+'/current_velocity.txt')
				data['xa'].append(xa)
				data['ya'].append(ya)
				data['za'].append(za)
				data['xl'].append(xl)
				data['yl'].append(yl)
				data['zl'].append(zl)
				#pdb.set_trace()
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
				#pdb.set_trace()
		if args.signal == 'vehicle_cmd':
			data = {'steer_cmd':[], 'accel_cmd':[], 'brake_cmd':[], 'lamp_cmd_l':[], 'lamp_cmd_r':[], 'gear_cmd':[], 'mode':[], 'xl':[], 'xa':[],'yl':[], 'ya':[], 'zl':[], 'za':[]}
			for (dirpath, dirnames, filenames) in walk('/localdisk/autoware_base/' + args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + '/localdisk/autoware_base/' + args.base + '/' + f[i]
				#pdb.set_trace()
				os.system(cmd)
				rawfile = []
				steer_cmd, accel_cmd, brake_cmd, lamp_cmd_l, lamp_cmd_r, gear_cmd, mode, xl, xa, yl, ya, zl, za = parse_vehiclecmd(f[i][:-4]+'/vehicle_cmd.txt')
				data['steer_cmd'].append(steer_cmd)
				data['accel_cmd'].append(accel_cmd)
				data['brake_cmd'].append(brake_cmd)
				data['lamp_cmd_l'].append(lamp_cmd_l)
				data['lamp_cmd_r'].append(lamp_cmd_r)
				data['gear_cmd'].append(gear_cmd)
				data['mode'].append(mode)
				data['xl'].append(xl)
				data['yl'].append(yl)
				data['zl'].append(zl)
				data['xa'].append(xa)
				data['ya'].append(ya)
				data['za'].append(za)
				cmd = 'rm -r '+str(f[i][:-4])
				os.system(cmd)
	file = gzip.GzipFile(args.save, 'wb')
	pickle.dump(data,file, -1)
	file.close()
	
if __name__ == '__main__':
	main()