from .. import Globals 
import time
import os
import numpy as np

def _GetCDFURL(Year,sc,L):
	'''
	Retrieves the url(s) of the cdf file to be downloaded.
	
	Inputs:
		Year: integer year.
		sc: 'a' or 'b'
		L: data type, one of the following options:
			'l3' (Spin-fit Electric field in modified-GSE (MGSE) coord, density, and other products)
			'l2.spec' (8 second FFT power spectra)
			'l2.e-spinfit-mgse' (Spin-fit E12 Electric field in modified-GSE (MGSE) coordinates)
			'l2.fbk' (8 sample/sec filterbank peak, average wave amplitude)
			'l2.esvy_despun' (32 sample/sec despun electric field in modified-GSE (MGSE) coordinates)
			'l2.vsvy-hires' (16 sample/sec single-ended V1-V6 probe potentials)
			'l1.eb1' (EB1 in UVW coordinates)
			'l1.eb2' (EB2 in UVW coordinates)
			'l1.mscb1' (MSCB1 in UVW coordinates)
			'l1.mscb2' (MSCB2 in UVW coordinates)
			'l1.vb1' (VB1 in UVW coordinates)
			'l1.vb2'(VB2 in UVW coordinates)
			
	Returns:
		urls,fnames
	'''
	#first let's get the url which will contain the link to the cdf file
	if L == 'l3':
		url0 = 'http://rbsp.space.umn.edu/data/rbsp/rbsp{:s}/l3/{:4d}/'.format(sc,Year)
	elif 'l1' in L:
		l = L.split('.')
		url0 = 'http://themis.ssl.berkeley.edu/data/rbsp/rbsp{:s}/{:s}/{:s}/{:4d}/'.format(sc,l[0],l[1],Year)
	else:
		l = L.split('.')
		url0 = 'http://rbsp.space.umn.edu/data/rbsp/rbsp{:s}/{:s}/{:s}/{:4d}/'.format(sc,l[0],l[1],Year)
	
	#set up a temporary file/path 
	tmppath = Globals.DataPath+'tmp/'
	if not os.path.isdir(tmppath):
		os.system('mkdir -pv '+tmppath)
	tmpfname = tmppath + '{:17.7f}.tmp'.format(time.time())
	
	#wget the file
	os.system('wget '+url0+' -O '+tmpfname)
	
	#read it
	f = open(tmpfname,'r')
	lines = f.readlines()
	n = np.size(lines)
	f.close()
	
	#delete it
	os.system('rm -v '+tmpfname)
	
	
	#now search for the line with the substring '.cdf"'
	urls = []
	fnames = []
	for i in range(0,n):
		if '.cdf"' in lines[i]:
			s = lines[i].split('"')
			for ss in s:
				if '.cdf' in ss:
					urls.append(url0+ss)
					fnames.append(ss)
					break
					
	return urls,fnames
	
