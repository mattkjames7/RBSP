import os 
from .. import Globals
import PyFileIO as pf

def _UpdateDataIndex(idx,sc='a',L='l3'):
	'''
	Updates the data index file.
	
	Input:
		idx: numpy.recarray containing the file names.
	'''
	
	fname = Globals.DataPath+'EFW/{:s}.{:s}.dat'.format(L,sc)
	pf.WriteASCIIData(fname,idx)
