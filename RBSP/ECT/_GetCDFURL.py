from .. import Globals 
import time
import os
import numpy as np

def _GetCDFURL(Year,sc,Inst,L):
	'''
	Retrieves the url(s) of the cdf file to be downloaded.
	
	Inputs:
		Year: integer year.
		sc: 'a' or 'b'
		Inst: 'hope', 'mageis' or 'rept' 
		L: data type, one of the following options:
			for hope: 'l2.sectors'|'l2.spinaverage'|'l3.moments'|'l3.pitchangle'
			for mageis: 'l2'|'l3'
			for rept: 'l2'|'l3'
			
	Returns:
		urls,fnames
	'''
	#first let's get the url which will contain the link to the cdf file
	if Inst == 'hope':
		l = L.split('.')
	elif Inst == 'mageis':
		if L == 'l3':
			l = [L,'pitchangle']
		else:
			l = [L,'sectors']
	else:
		if L == 'l3':
			l = [L,'pitchangle']
		else:
			l = [L,'sectors']
	l[0] = l[0].replace('l','level')
	url0 = 'https://www.rbsp-ect.lanl.gov/data_pub/rbsp{:s}/{:s}/{:s}/{:s}/{:4d}/'.format(sc,Inst,l[0],l[1],Year)
	
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
		if '.cdf"' in lines[i]:
			s = lines[i].split('"')
			for ss in s:
				if '.cdf' in ss:
					urls.append(url0+ss)
					fnames.append(ss)
					break
					
	return urls,fnames
	
