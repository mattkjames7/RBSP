import numpy as np
from .. import Globals
import RecarrayTools as RT
from . import _EFW
import os

def _ReadPotential(Date,sc,Size=False):
	
	fname = Globals.DataPath + 'Potential/{:s}/'.format(sc) + '{:08d}.bin'.format(Date)

	if not os.path.isfile(fname):
		if Size:
			return 0
		else:
			return np.recarray(0,dtype=_EFW.pdtype)
			
	if Size:
		f = open(fname,'rb')
		out = np.fromfile(f,dtype='int32',count=1)[0]
		f.close()
	else:
		out = RT.ReadRecarray(fname,_EFW.pdtype)
	
	return out
