import numpy as np
from .. import Globals
import RecarrayTools as RT
from . import _ECT
import os

def ReadIonMoments(Date,sc):
	'''
	
	
	'''
		
	outdir = Globals.DataPath + 'Moments/Ions/{:s}/'.format(sc)
	fname = outdir + '{:08d}.bin'.format(Date)
	
	if not os.path.isfile(fname):
		return np.recarray(0,dtype=_ECT.idtype)
	else:
		return RT.ReadRecarray(fname,_ECT.idtype)
	
	
	
	
	
