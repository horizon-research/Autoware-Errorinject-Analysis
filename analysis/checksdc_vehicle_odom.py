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
	pdb_xp = {}
	pdb_yp = {}
	pdb_zp = {}
	pdb_xo = {}
	pdb_yo = {}
	pdb_zo = {}
	pdb_wo = {}
	pdb_xl = {}
	pdb_yl = {}
	pdb_zl = {}
	pdb_xa = {}
	pdb_ya = {}
	pdb_za = {}

	for i in range(len(data['xp'])):
		for j in range(180,204):
			#pdb.set_trace()
			tmp = round((data['xp'][i][j]),1)
			if tmp not in pdb_xp:
				pdb_xp[tmp] = 1
			else:
				pdb_xp[tmp] += 1
			tmp = round((data['yp'][i][j]),1)
			if tmp not in pdb_yp:
				pdb_yp[tmp] = 1
			else:
				pdb_yp[tmp] += 1
			tmp = round((data['zp'][i][j]),1)
			if tmp not in pdb_zp:
				pdb_zp[tmp] = 1
			else:
				pdb_zp[tmp] += 1
			tmp = round((data['xo'][i][j]),1)
			if tmp not in pdb_xo:
				pdb_xo[tmp] = 1
			else:
				pdb_xo[tmp] += 1
			tmp = round((data['yo'][i][j]),1)
			if tmp not in pdb_yo:
				pdb_yo[tmp] = 1
			else:
				pdb_yo[tmp] += 1
			tmp = round((data['zo'][i][j]),1)
			if tmp not in pdb_zo:
				pdb_zo[tmp] = 1
			else:
				pdb_zo[tmp] += 1
			tmp = round((data['wo'][i][j]),1)
			if tmp not in pdb_wo:
				pdb_wo[tmp] = 1
			else:
				pdb_wo[tmp] += 1

			tmp = round((data['xl'][i][j]),1)
			if tmp not in pdb_xl:
				pdb_xl[tmp] = 1
			else:
				pdb_xl[tmp] += 1
			tmp = round((data['yl'][i][j]),1)
			if tmp not in pdb_yl:
				pdb_yl[tmp] = 1
			else:
				pdb_yl[tmp] += 1
			tmp = round((data['zl'][i][j]),1)
			if tmp not in pdb_zl:
				pdb_zl[tmp] = 1
			else:
				pdb_zl[tmp] += 1
			tmp = round((data['xa'][i][j]),1)
			if tmp not in pdb_xa:
				pdb_xa[tmp] = 1
			else:
				pdb_xa[tmp] += 1
			tmp = round((data['ya'][i][j]),1)
			if tmp not in pdb_ya:
				pdb_ya[tmp] = 1
			else:
				pdb_ya[tmp] += 1
			tmp = round((data['za'][i][j]),1)
			if tmp not in pdb_za:
				pdb_za[tmp] = 1
			else:
				pdb_za[tmp] += 1
	#pdb.set_trace()
	
	pdb_xp = sorted(pdb_xp.keys())
	pdb_yp = sorted(pdb_yp.keys())
	pdb_zp = sorted(pdb_zp.keys())
	pdb_xo = sorted(pdb_xo.keys())
	pdb_yo = sorted(pdb_yo.keys())
	pdb_zo = sorted(pdb_zo.keys())
	pdb_wo = sorted(pdb_wo.keys())
	pdb_xl = sorted(pdb_xl.keys())
	pdb_yl = sorted(pdb_yl.keys())
	pdb_zl = sorted(pdb_zl.keys())
	pdb_xa = sorted(pdb_xa.keys())
	pdb_ya = sorted(pdb_ya.keys())
	pdb_za = sorted(pdb_za.keys())
	#pdb.set_trace()
	f = []
	for (dirpath, dirnames, filenames) in walk('/localdisk/attack_autoware_regis/'+args.base):
		f=filenames
	file_name = []
	xp_large = 0
	xp_min = 0
	yp_large = 0
	yp_min = 0
	zp_large = 0
	zp_min = 0
	xo_large = 0
	xo_min = 0
	yo_large = 0
	yo_min = 0
	zo_large = 0
	zo_min = 0
	wo_large = 0
	wo_min = 0
	xl_large = 0
	xl_min = 0
	yl_large = 0
	yl_min = 0
	zl_large = 0
	zl_min = 0
	xa_large = 0
	xa_min = 0
	ya_large = 0
	ya_min = 0
	za_large = 0
	za_min = 0

	for i in range(1,len(f)):
		cmd = 'unzip /localdisk/attack_autoware_regis/'+ args.base + '/' + f[i]
		#pdb.set_trace()
		os.system(cmd)
		xp,yp,zp,xo,yo,zo,wo,xl,yl,zl,xa,ya,za = parse_vodometry(f[i][:-4]+'/vehicle_odom.txt')
		cmd = 'rm -r '+ f[i][:-4]
		os.system(cmd)
		for j in range(len(xp)):
			if j >= 180 and j < 210:
				if xp[j] > pdb_xp[-1]:
					if i not in file_name:
						file_name.append(i)
					if (xp[j] - pdb_xp[-1]) > xp_large:
						xp_large = xp[j] - pdb_xp[-1]
				if xp[j] < pdb_xp[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_xp[0] - xp[j]) > xp_min:
						xp_min = pdb_xp[0] - xp[j]
				if yp[j] > pdb_yp[-1]:
					if i not in file_name:
						file_name.append(i)
					if (yp[j] - pdb_yp[-1]) > yp_large:
						yp_large = yp[j] - pdb_yp[-1]
				if yp[j] < pdb_yp[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_yp[0] - yp[j]) > yp_min:
						yp_min = pdb_yp[0] - yp[j]
				if zp[j] > pdb_zp[-1]:
					if i not in file_name:
						file_name.append(i)
					if (zp[j] - pdb_zp[-1]) > zp_large:
						zp_large = zp[j] - pdb_zp[-1]
				if zp[j] < pdb_zp[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_zp[0] - zp[j]) > zp_min:
						zp_min = pdb_zp[0] - zp[j]
				if xo[j] > pdb_xo[-1]:
					if i not in file_name:
						file_name.append(i)
					if (xo[j] - pdb_xo[-1]) > xo_large:
						xo_large = xo[j] - pdb_xo[-1]
				if xo[j] < pdb_xo[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_xo[0] - xo[j]) > xo_min:
						xo_min = pdb_xo[0] - xo[j]
				if yo[j] > pdb_yo[-1]:
					if i not in file_name:
						file_name.append(i)
					if (yo[j] - pdb_yo[-1]) > yo_large:
						yo_large = yo[j] - pdb_yo[-1]
				if yo[j] < pdb_yo[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_yo[0] - yo[j]) > yo_min:
						yo_min = pdb_yo[0] - yo[j]
				if zo[j] > pdb_zo[-1]:
					if i not in file_name:
						file_name.append(i)
					if (zo[j] - pdb_zo[-1]) > zo_large:
						zo_large = zo[j] - pdb_zo[-1]
				if zo[j] < pdb_zo[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_zo[0] - zo[0]) > zo_min:
						zo_min = pdb_zo[0] - zo[j]
				if wo[j] > pdb_wo[-1]:
					if i not in file_name:
						file_name.append(i)
					if (wo[j] - pdb_wo[-1]) > wo_large:
						wo_large = wo[j] - pdb_wo[-1]
				if wo[j] < pdb_wo[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_wo[0] - wo[j]) > wo_min:
						wo_min = pdb_wo[0] - wo[j]
				if xl[j] > pdb_xl[-1]:
					if i not in file_name:
						file_name.append(i)
					if (xl[j] - pdb_xl[-1]) > xl_large:
						xl_large = xl[j] - pdb_xl[-1]
				if xl[j] < pdb_xl[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_xl[0] - xl[j]) > xl_min:
						xl_min = pdb_xl[0] - xl[j]
				if yl[j] > pdb_yl[-1]:
					if i not in file_name:
						file_name.append(i)
					if (yl[j] - pdb_yl[-1]) > yl_large:
						yl_large = yl[j] - pdb_yl[-1]
				if yl[j] < pdb_yl[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_yl[0] - yl[j]) > yl_min:
						yl_min = pdb_yl[0] - yl[j]
				if zl[j] > pdb_zl[-1]:
					if i not in file_name:
						file_name.append(i)
					if (zl[j] - pdb_zl[-1]) > zl_large:
						zl_large = zl[j] - pdb_zl[-1]
				if zl[j] < pdb_zl[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_zl[0] - zl[j]) > zl_min:
						zl_min = pdb_zl[0] - zl[j]
				if xa[j] > pdb_xa[-1]:
					if i not in file_name:
						file_name.append(i)
					if (xa[j] - pdb_xa[-1]) > xa_large:
						xa_large = xa[j] - pdb_xa[-1]
				if xa[j] < pdb_xa[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_xa[0] - xa[j]) > xa_min:
						xa_min = pdb_xa[0] - xa[j]
				if ya[j] > pdb_ya[-1]:
					if i not in file_name:
						file_name.append(i)
					if (ya[j] - pdb_ya[-1]) > ya_large:
						ya_large = ya[j] - pdb_ya[-1]
				if ya[j] < pdb_ya[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_ya[0] - ya[j]) > ya_min:
						ya_min = pdb_ya[0] - ya[j]
				if za[j] > pdb_za[-1]:
					if i not in file_name:
						file_name.append(i)
					if (za[j] - pdb_za[-1]) > za_large:
						za_large = za[j] - pdb_za[-1]
				if za[j] < pdb_za[0]:
					if i not in file_name:
						file_name.append(i)
					if (pdb_za[0] - za[j]) > za_min:
						za_min = pdb_za[0] - za[j]				
		print(file_name)
	pdb.set_trace()		

if __name__ == '__main__':
	main()