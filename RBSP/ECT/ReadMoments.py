import numpy as np
from .. import Globals
import RecarrayTools as RT
from . import _ECT
import os

def ReadMoments(Date,sc,Species='H'):
	'''
	
	
	'''
		
	fname = Globals.DataPath + 'Moments/{:s}/{:s}/{:08d}.bin'.format(sc,Species,Date)

	if not os.path.isfile(fname):
		return np.recarray(0,dtype=_ECT.mdtype)
	else:
		return RT.ReadRecarray(fname,_ECT.mdtype)
	
	
	
	
	
