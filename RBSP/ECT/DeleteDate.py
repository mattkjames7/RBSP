import numpy as np
from ..Tools.Downloading._DeleteDate import _DeleteDate
from . import _ECT

def DeleteDate(Date,sc,Inst,L,Confirm=True):
	'''
	delete all of the files from a given date
	
	'''
	idxfname = _EWF.idxfname.format(Inst,L,sc)
	datapath = _EWF.datapath.format(Inst,L,sc)

	_DeleteDate(Date,idxfname,datapath,Confirm)
