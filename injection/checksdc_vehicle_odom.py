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
	parser.add_argument('--base', default='vehicle_odom_attack_generalregis')
	parser.add_argument('--save', default='vehicle_odom.pkl')
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
	pdb_xl = [{} for i in range(30)]
	pdb_yl = [{} for i in range(30)]
	pdb_zl = [{} for i in range(30)]
	pdb_xa = [{} for i in range(30)]
	pdb_ya = [{} for i in range(30)]
	pdb_za = [{} for i in range(30)]    

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

			tmp = round((data['xl'][i][j]),1)
			if tmp not in pdb_xl[j-180]:
				pdb_xl[j-180][tmp] = 0.005
			else:
				pdb_xl[j-180][tmp] += 0.005
			tmp = round((data['yl'][i][j]),1)
			if tmp not in pdb_yl[j-180]:
				pdb_yl[j-180][tmp] = 0.005
			else:
				pdb_yl[j-180][tmp] += 0.005
			tmp = round((data['zl'][i][j]),1)
			if tmp not in pdb_zl[j-180]:
				pdb_zl[j-180][tmp] = 0.005
			else:
				pdb_zl[j-180][tmp] += 0.005
			tmp = round((data['xa'][i][j]),1)
			if tmp not in pdb_xa[j-180]:
				pdb_xa[j-180][tmp] = 0.005
			else:
				pdb_xa[j-180][tmp] += 0.005
			tmp = round((data['ya'][i][j]),1)
			if tmp not in pdb_ya[j-180]:
				pdb_ya[j-180][tmp] = 0.005
			else:
				pdb_ya[j-180][tmp] += 0.005
			tmp = round((data['za'][i][j]),1)
			if tmp not in pdb_za[j-180]:
				pdb_za[j-180][tmp] = 0.005
			else:
				pdb_za[j-180][tmp] += 0.005
	for i in range(len(pdb_xp)):
		pdb_xp[i] = sorted(pdb_xp[i].keys())
		pdb_yp[i] = sorted(pdb_yp[i].keys())
		pdb_zp[i] = sorted(pdb_zp[i].keys())
		pdb_xo[i] = sorted(pdb_xo[i].keys())
		pdb_yo[i] = sorted(pdb_yo[i].keys())
		pdb_zo[i] = sorted(pdb_zo[i].keys())
		pdb_wo[i] = sorted(pdb_wo[i].keys())
		pdb_xl[i] = sorted(pdb_xl[i].keys())
		pdb_yl[i] = sorted(pdb_yl[i].keys())
		pdb_zl[i] = sorted(pdb_zl[i].keys())
		pdb_xa[i] = sorted(pdb_xa[i].keys())
		pdb_ya[i] = sorted(pdb_ya[i].keys())
		pdb_za[i] = sorted(pdb_za[i].keys())
	f = []
	for (dirpath, dirnames, filenames) in walk('vehicle_odom_attack_genralregis'):
		f=filenames
	frame = []
	for i in range(1,len(f)):
		cmd = 'unzip vehicle_odom_attack_fpregis/' + f[i]
		os.system(cmd)
		xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za = parse_vodometry(f[i][:-4]+'/vehicle_odom.txt')
		cmd = 'rm -r '+ f[i][:-4]
		os.system(cmd)
		for j in range(len(xp)):
			if j >= 180 and j < 210:
				if round(xp[j],1) < pdb_xp[j-180][0] or round(xp[j],1) > pdb_xp[j-180][-1]:
					print(str(j) + 'frame' + 'xp')
					if j not in frame:
						frame.append(j)
					print(xp[j], pdb_xp[j-180])
				if round(yp[j],1) < pdb_yp[j-180][0] or round(yp[j],1) > pdb_yp[j-180][-1]:
					print(str(j) + 'frame' + 'yp')
					if j not in frame:
						frame.append(j)
					print(yp[j], pdb_yp[j-180])
				if round(zp[j],1) < pdb_zp[j-180][0] or round(zp[j],1) > pdb_zp[j-180][-1]:
					print(str(j) + 'frame'+ 'zp')
					if j not in frame:
						frame.append(j)
					print(zp[j], pdb_zp[j-180])
				if round(xo[j],1) < pdb_xo[j-180][0] or round(xo[j],1) > pdb_xo[j-180][-1]:
					print(str(j) + 'frame'+ 'xo')
					if j not in frame:
						frame.append(j)
					print(xo[j], pdb_xo[j-180])
				if round(yo[j],1) < pdb_yo[j-180][0] or round(yo[j],1) > pdb_yo[j-180][-1]:
					print(str(j) + 'frame'+ 'yo')
					if j not in frame:
						frame.append(j)
					print(yo[j], pdb_yo[j-180])
				if round(zo[j],1) < pdb_zo[j-180][0] or round(zo[j],1) > pdb_zo[j-180][-1]:
					print(str(j) + 'frame'+ 'zo')
					if j not in frame:
						frame.append(j)
					print(zo[j], pdb_zo[j-180])
				if round(wo[j],1) < pdb_wo[j-180][0] or round(wo[j],1) > pdb_wo[j-180][-1]:
					print(str(j) + 'frame'+ 'wo')
					if j not in frame:
						frame.append(j)
					print(wo[j], pdb_wo[j-180])
				if round(xl[j],1) < pdb_xl[j-180][0] or round(xl[j],1) > pdb_xl[j-180][-1]:
					print(str(j) + 'frame' + 'xp')
					if j not in frame:
						frame.append(j)
					print(xl[j], pdb_xl[j-180])
				if round(yl[j],1) < pdb_yl[j-180][0] or round(yl[j],1) > pdb_yl[j-180][-1]:
					print(str(j) + 'frame' + 'yp')
					if j not in frame:
						frame.append(j)
					print(yl[j], pdb_yl[j-180])
				if round(zl[j],1) < pdb_zl[j-180][0] or round(zl[j],1) > pdb_zl[j-180][-1]:
					print(str(j) + 'frame'+ 'zp')
					if j not in frame:
						frame.append(j)
					print(zl[j], pdb_zl[j-180])
				if round(xa[j],1) < pdb_xa[j-180][0] or round(xa[j],1) > pdb_xa[j-180][-1]:
					print(str(j) + 'frame'+ 'xo')
					if j not in frame:
						frame.append(j)
					print(xa[j], pdb_xa[j-180])
				if round(ya[j],1) < pdb_ya[j-180][0] or round(ya[j],1) > pdb_ya[j-180][-1]:
					print(str(j) + 'frame'+ 'yo')
					if j not in frame:
						frame.append(j)
					print(ya[j], pdb_ya[j-180])
				if round(za[j],1) < pdb_za[j-180][0] or round(za[j],1) > pdb_za[j-180][-1]:
					print(str(j) + 'frame'+ 'zo')
					if j not in frame:
						frame.append(j)
					print(za[j], pdb_za[j-180])
			else:
				continue
	print(len(frame))
if __name__ == '__main__':
	main()