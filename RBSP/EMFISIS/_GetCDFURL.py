from .. import Globals 
import time
import os
import numpy as np

def _GetCDFURL(Date,sc,L):
	'''
	Retrieves the url(s) of the cdf file to be downloaded.
	
	Inputs:
		Date: 32-bit integer date with format yyyymmdd.
		sc: 'a' or 'b'
		L: Level of the data 2, 3 or 4 (integer)
		
	Returns:
		urls,fnames
	'''
	#first let's get the url which will contain the link to the cdf file
	yy = Date // 10000
	mm = (Date % 10000) // 100
	dd = Date % 100
	
	url0 = 'https://emfisis.physics.uiowa.edu/Flight/RBSP-{:s}/L{:1d}/{:4d}/{:02d}/{:02d}/'.format(sc.upper(),L,yy,mm,dd)
	
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
	
