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

def main():
	parser = argparse.ArgumentParser(description="base folder, save dir and database query")
	parser.add_argument('--base', default='odometry_posestamped_attack_generalregis')
	parser.add_argument('--save', default='gnss_pose.pkl')
	args = parser.parse_args()

	file = gzip.GzipFile(args.save, 'rb')
	data = pickle.load(file)
	file.close()
	pdb_xp = [{} for i in range(30)]
	pdb_yp = [{} for i in range(30)]
	pdb_zp = [{} for i in range(30)]
	pdb_xo = [{} for i in range(30)]
	pdb_yo = [{} for i in range(30)]
	pdb_zo = [{} for i in range(30)]
	pdb_wo = [{} for i in range(30)]

	for i in range(len(data['xp'])):
		for j in range(180,210):
			#pdb.set_trace()
			tmp = round((data['xp'][i][j]),1)
			if tmp not in pdb_xp[j-180]:
				pdb_xp[j-180][tmp] = 0.005
			else:
				pdb_xp[j-180][tmp] += 0.005
			tmp = round((data['yp'][i][j]),1)
			if tmp not in pdb_yp[j-180]:
				pdb_yp[j-180][tmp] = 0.005
			else:
				pdb_yp[j-180][tmp] += 0.005
			tmp = round((data['zp'][i][j]),1)
			if tmp not in pdb_zp[j-180]:
				pdb_zp[j-180][tmp] = 0.005
			else:
				pdb_zp[j-180][tmp] += 0.005
			tmp = round((data['xo'][i][j]),1)
			if tmp not in pdb_xo[j-180]:
				pdb_xo[j-180][tmp] = 0.005
			else:
				pdb_xo[j-180][tmp] += 0.005
			tmp = round((data['yo'][i][j]),1)
			if tmp not in pdb_yo[j-180]:
				pdb_yo[j-180][tmp] = 0.005
			else:
				pdb_yo[j-180][tmp] += 0.005
			tmp = round((data['zo'][i][j]),1)
			if tmp not in pdb_zo[j-180]:
				pdb_zo[j-180][tmp] = 0.005
			else:
				pdb_zo[j-180][tmp] += 0.005
			tmp = round((data['wo'][i][j]),1)
			if tmp not in pdb_wo[j-180]:
				pdb_wo[j-180][tmp] = 0.005
			else:
				pdb_wo[j-180][tmp] += 0.005
	for i in range(len(pdb_xp)):
		pdb_xp[i] = sorted(pdb_xp[i].keys())
		pdb_yp[i] = sorted(pdb_yp[i].keys())
		pdb_zp[i] = sorted(pdb_zp[i].keys())
		pdb_xo[i] = sorted(pdb_xo[i].keys())
		pdb_yo[i] = sorted(pdb_yo[i].keys())
		pdb_zo[i] = sorted(pdb_zo[i].keys())
		pdb_wo[i] = sorted(pdb_wo[i].keys())
	f = []
	for (dirpath, dirnames, filenames) in walk('odometry_posestamped_attack_fpregis'):
		f.append(dirpath)
	#pdb.set_trace()
	frame = []
	for i in range(1,len(f)):
		xp,yp,zp,xo,yo,zo,wo = parse_curr_pose(f[i]+'/gnss_pose.txt')
		for j in range(len(xp)):
			if j >= 180 and j < 210:
				if xp[j] < pdb_xp[j-180][0] or xp[j] > pdb_xp[j-180][-1]:
					print(str(j) + 'frame' + 'xp')
					if i not in frame:
						frame.append(i)
					print(xp[j], pdb_xp[j-180])
				if yp[j] < pdb_yp[j-180][0] - (pdb_yp[j-180][-1] - pdb_yp[j-180][0]) or yp[j] > pdb_yp[j-180][-1]:
					print(str(j) + 'frame' + 'yp')
					if i not in frame:
						frame.append(i)
					print(yp[j], pdb_yp[j-180])
				if zp[j] < pdb_zp[j-180][0] or zp[j] > pdb_zp[j-180][-1]:
					print(str(j) + 'frame'+ 'zp')
					if i not in frame:
						frame.append(i)
					print(zp[j], pdb_zp[j-180])
				if xo[j] < pdb_xo[j-180][0] or xo[j] > pdb_xo[j-180][-1]:
					print(str(j) + 'frame'+ 'xo')
					if i not in frame:
						frame.append(i)
					print(xo[j], pdb_xo[j-180])
				if yo[j] < pdb_yo[j-180][0] or yo[j] > pdb_yo[j-180][-1]:
					print(str(j) + 'frame'+ 'yo')
					if i not in frame:
						frame.append(i)
					print(yo[j], pdb_yo[j-180])
				if zo[j] < pdb_zo[j-180][0] or zo[j] > pdb_zo[j-180][-1]:
					print(str(j) + 'frame'+ 'zo')
					if i not in frame:
						frame.append(i)
					print(zo[j], pdb_zo[j-180])
				if wo[j] < pdb_wo[j-180][0] or wo[j] > pdb_wo[j-180][-1]:
					print(str(j) + 'frame'+ 'wo')
					if i not in frame:
						frame.append(i)
					print(wo[j], pdb_wo[j-180])
			else:
				continue
	print(frame)

	
if __name__ == '__main__':
	main()