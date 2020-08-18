import numpy as np
from ..Tools.Downloading._DeleteDate import _DeleteDate
from . import _EFW

def DeleteDate(Date,sc,L,Confirm=True):
	'''
	delete all of the files from a given date
	
	'''
	idxfname = _EWF.idxfname.format(L,sc)
	datapath = _EWF.datapath.format(L,sc)

	_DeleteDate(Date,idxfname,datapath,Confirm)
