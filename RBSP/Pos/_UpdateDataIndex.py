import os 
from .. import Globals
import PyFileIO as pf

def _UpdateDataIndex(idx,sc='a'):
	'''
	Updates the data index file.
	
	Input:
		idx: numpy.recarray containing the file names.
	'''
	
	fname = Globals.DataPath+'MagEph/{:s}.dat'.format(sc)
	pf.WriteASCIIData(fname,idx)
