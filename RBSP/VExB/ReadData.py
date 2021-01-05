import numpy as np
from . import _VExB 
import os
import RecarrayTools as RT

def ReadData(Date,sc):
	'''
	Read the file which contains the ExB drift velocities.
	
	'''
	#get the file name
	fname = _VExB.datapath.format(sc) + '{:08d}.bin'.format(Date)
	
	#check if it exists
	if not os.path.isfile(fname):
		return np.recarray(0,dtype=_VExB.dtype)
	else:
		return RT.ReadRecarray(fname,_VExB.dtype)
