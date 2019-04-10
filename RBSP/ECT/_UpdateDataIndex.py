import os 
from .. import Globals
import PyFileIO as pf

def _UpdateDataIndex(idx,sc='a',Inst='hope',L='l3.moments'):
	'''
	Updates the data index file.
	
	Input:
		idx: numpy.recarray containing the file names.
	'''
	
	fname = Globals.DataPath+'ECT/{:s}.{:s}.{:s}.dat'.format(Inst,L,sc)
	pf.WriteASCIIData(fname,idx)
