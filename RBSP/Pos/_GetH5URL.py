from .. import Globals 
import time
import os
import numpy as np

def _GetH5URL(Year,sc):
	'''
	Retrieves the url(s) of the cdf file to be downloaded.
	
	Inputs:
		Year: integer year.
		sc: 'a' or 'b'

	Returns:
		urls,fnames
	'''
	#first let's get the url which will contain the link to the cdf file
	#the emfisis one is a bit dodgy
	#url0 = 'https://emfisis.physics.uiowa.edu/Flight/RBSP-{:s}/LANL/MagEphem/{:4d}/'.format(sc.upper(),Year)
	url0 = 'https://rbsp-ect.newmexicoconsortium.org/data_pub/rbsp{:s}/MagEphem/definitive/{:4d}/'.format(sc.lower(),Year)
	
	#set up a temporary file/path 
	tmppath = Globals.DataPath+'tmp/'
	if not os.path.isdir(tmppath):
		os.system('mkdir -pv '+tmppath)
	tmpfname = tmppath + '{:17.7f}.tmp'.format(time.time())
	
	#wget the file
	os.system('wget --no-check-certificate '+url0+' -O '+tmpfname)
	
	#read it
	f = open(tmpfname,'r')
	lines = f.readlines()
	n = np.size(lines)
	f.close()
	
	#delete it
	#os.system('rm -v '+tmpfname)
	
	
	#now search for the line with the substring '.cdf"'
	urls = []
	fnames = []
	for i in range(0,n):
		if '.h5"' in lines[i] and 'OP77Q' in lines[i]:
			s = lines[i].split('"')
			for ss in s:
				if '.h5' in ss:
					urls.append(url0+ss)
					fnames.append(ss)
					break
					
	return urls,fnames
	
