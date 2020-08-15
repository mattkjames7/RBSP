from ... import Globals 
import time
import os
import numpy as np

def _GetCDFURL(Year,Month,url0):
	'''
	Retrieves the url(s) of the cdf file to be downloaded.
	
	Inputs:
		Year: year
		Month: month
	Returns:
		urls,fnames
	'''
	#first let's get the url which will contain the link to the cdf files
	url = url0.format(Year,Month)
	
	#set up a temporary file/path 
	tmppath = Globals.DataPath+'tmp/'
	if not os.path.isdir(tmppath):
		os.system('mkdir -pv '+tmppath)
	tmpfname = tmppath + '{:17.7f}.tmp'.format(time.time())
	
	#wget the file
	ret = os.system('wget --no-verbose '+url+' -O '+tmpfname)
	
	if ret != 0:
		return [],[]
	
	#read it
	f = open(tmpfname,'r')
	lines = f.readlines()
	n = np.size(lines)
	f.close()

	#now search for the line with the substring '.cdf"'
	urls = []
	fnames = []
	yearstr = '{:04d}'.format(Year)
	for i in range(0,n):
		if '.cdf"' in lines[i] and yearstr in lines[i]:
			s = lines[i].replace('<a','"').replace('</a>','"').replace('>','"').split('"')
			for ss in s:
				if '.cdf' in ss and not 'http' in ss:
					urls.append(url+ss)
					fnames.append(ss)
					break
					
	return np.array(urls),np.array(fnames)
	
