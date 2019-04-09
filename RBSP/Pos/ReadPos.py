import numpy as np
import os
from .. import Globals
import RecarrayTools as RT

def ReadPos(sc='a'):
	'''
	Reads the binary files containing positional information about RBSP.
	
	Input:
		sc: 'a' or 'b'
		
	Returns:
		numpy.recarray
	'''
	fname = Globals.DataPath+'Pos/'+'rbsp'+sc+'.bin'

	dtype = [('Date','int32'),('ut','float32'),
			('Xgeo','float32'),('Ygeo','float32'),('Zgeo','float32'),
			('Xgm','float32'),('Ygm','float32'),('Zgm','float32'),
			('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
			
	if not os.path.isfile(fname):
		print('file {:s} not found'.format(fname))
		return np.recarray(0,dtype=dtype)
		
	return RT.ReadRecarray(fname,dtype)
	
