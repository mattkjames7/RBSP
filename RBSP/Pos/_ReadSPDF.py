from .. import Globals
import PyFileIO as pf
import os
import numpy as np

def _ReadSPDF(sc='a'):
	'''
	Reads the SPDF SSCWeb text files (scraped from their HTML output).
	
	Input:
		sc: Spacecraft 'a' or 'b'
		
	Returns:
		numpy.recarray
	
	'''
	#set up dtype to load
	dtype = [('Year','int32'),('DOY','int32'),('ut','U9'),('Xgeo','float32'),('Ygeo','float32'),('Zgeo','float32'),('Latgeo','float32'),('Longeo','float32'),('LTgeo','U9'),
			('Xgm','float32'),('Ygm','float32'),('Zgm','float32'),('Latgm','float32'),('Longm','float32'),('LTgm','U9'),
			('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),('Latgse','float32'),('Longse','float32'),('LTgse','U9'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),('Latgsm','float32'),('Longsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32'),('Latsm','float32'),('Lonsm','float32'),('LTsm','U9'),('L','float32')]
	
	#find the file
	fname = Globals.DataPath + 'SPDF/rbsp'+sc+'.dat'

	if not os.path.isfile(fname):
		print('SPDF data for spacecraft "{:s}" not found'.format(sc))
		return np.recarray(0,dtype=dtype)

	#data = pf.ReadASCIIData(fname,False,57,dtype=dtype)
	#read the file manually
	print('Reading file')
	f = open(fname,'r')
	lines = f.readlines()
	f.close()
	
	print('Creating output array')
	skip = 57
	nl = len(lines)
	n = nl - skip
	data = np.recarray(n,dtype=dtype)
	nc = 33
	
	for i in range(0,n):
		print('\rCopying data into array {:6.2f}%'.format(100.0*(i+1)/n),end='')
		s = lines[i+skip].split()
		for j in range(0,nc):
			data[dtype[j][0]][i] = np.array(s[j]).astype(dtype[j][1])
	print()
	return data
