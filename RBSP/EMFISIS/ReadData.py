from .. import Globals
import numpy as np
import pysatCDF
import fnmatch as fnm
import os as os
from ..Tools.CDFtoRecarray import CDFtoRecarray

def ReadData(Date,sc='a',L=4):
	'''
	This routine should read the CDF file downloaded.
	'''
	
	path = Globals.DataPath+'EMFISIS/L{:d}/{:s}/'.format(L,sc)
	pattern = '*{:08d}*.cdf'.format(Date)
	
	#list the files in the path first
	files = np.array(os.listdir(path))
	files.sort()
	
	#look for a match with the date
	matches = np.zeros(np.size(files),dtype='bool')
	for i in range(0,np.size(files)):
		if fnm.fnmatch(files[i],pattern):
			matches[i] = True
	
	if not (matches == True).any():
		return None,'nofile'
	good = np.where(matches == True)[0][-1]
	
	#read the data
	try:
		cdf = pysatCDF.CDF(path+files[good])
	except:
		print('Failed to read CDF file')
		return None,'badfile'
	#convert to recarray
	data,meta = CDFtoRecarray(cdf)
	
	return data,meta
	
