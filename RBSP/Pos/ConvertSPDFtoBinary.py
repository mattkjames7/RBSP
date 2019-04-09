import numpy as np
from ._ReadSPDF import _ReadSPDF
import RecarrayTools as RT
import os
from .. import Globals
import DateTimeTools as TT

def ConvertSPDFtoBinary(sc='a'):
	'''
	Converts the SPDF SSCWeb text files (scraped from their HTML output)
	to binary.
	
	Input:
		sc: Spacecraft 'a' or 'b'
		
	'''	
	fname = Globals.DataPath + 'Pos/'
	if not os.path.isdir(fname):
		os.system('mkdir -pv '+fname)
	fname += 'rbsp'+sc+'.bin'
	
	data = _ReadSPDF(sc)
	n = data.size
	
	dtype = [('Date','int32'),('ut','float32'),
			('Xgeo','float32'),('Ygeo','float32'),('Zgeo','float32'),
			('Xgm','float32'),('Ygm','float32'),('Zgm','float32'),
			('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
	out = np.recarray(n,dtype=dtype)
	
	names = out.dtype.names
	nc = np.size(names)
	
	for i in range(0,nc):
		if names[i] == 'Date':
			for j in range(0,n):
				out.Date[j] = TT.DayNotoDate(data.Year[j],data.DOY[j])
		elif names[i] in ['ut','LTgeo','LTgm','LTgse','LTsm']:
			for j in range(0,n):
				tmp = data[names[i]][j]
				out[names[i]][j] = np.float32(tmp[0:2]) + np.float32(tmp[3:5])/60.0 + np.float32(tmp[6:8])/3600.0
		else:
			out[names[i]] = data[names[i]]
	
	RT.SaveRecarray(out,fname)
	
