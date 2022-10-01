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

def main():
	parser = argparse.ArgumentParser(description="base folder, save dir and database query")
	parser.add_argument('--base', default='base0136')
	parser.add_argument('--save', default='vehicle_cmd.pkl')
	parser.add_argument('--signal', default='vehicle_cmd')

	args = parser.parse_args()
	if os.path.exists(args.save):
		file = gzip.GzipFile(args.save, 'rb')
		data = pickle.load(file, -1)
		file.close()
		if args.signal == 'gnss_pose':
			f = []
			for (dirpath, dirnames, filenames) in walk(args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + args.base + '/' + f[i]
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
			f = []
			for (dirpath, dirnames, filenames) in walk(args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + args.base + '/' + f[i]
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
	else:
		if args.signal == 'gnss_pose':
			data = {'xp':[],'yp':[],'zp':[],'xo':[],'yo':[],'zo':[],'wo':[]}
			f = []
			for (dirpath, dirnames, filenames) in walk(args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + args.base + '/' + f[i]
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
			for (dirpath, dirnames, filenames) in walk(args.base):
				f = filenames
			#pdb.set_trace()
			for i in range(len(f)):
				cmd = 'unzip ' + args.base + '/' + f[i]
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
	file = gzip.GzipFile(args.save, 'wb')
	pickle.dump(data,file, -1)
	file.close()
	
if __name__ == '__main__':
	main()