import numpy as np
from . import _Fields
import RecarrayTools as RT
import os

def ReadData(Date,sc='a',Size=False):
	'''
	Read in a single day of field data
	
	'''
	path = _Fields.datapath.format(sc)
	fname = path + '{:08d}.bin'.format(Date)

	if not os.path.isfile(fname):
		if Size:
			return 0
		else:
			return np.recarray(0,dtype=_Fields.dtype)
		
	if Size:
		f = open(fname,'rb')
		s = np.fromfile(f,dtype='int32',count=1)[0]
		f.close()
		return s
	else:
		return RT.ReadRecarray(fname,_Fields.dtype)
