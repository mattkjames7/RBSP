import numpy as np
from ..Tools.Downloading._DeleteDate import _DeleteDate
from .. import Globals

def DeleteDate(Date,sc,L,prod,Confirm=True):
	'''
	delete all of the files from a given date
	
	'''
	if L == 'l4':
		idxfname = _EMFISIS.idxfnamel4.format(L,sc)
		datapath = _EMFISIS.datapathl4.format(L,sc)
	else:
		idxfname = _EMFISIS.idxfname.format(L,sc,Prod)
		datapath = _EMFISIS.datapath.format(L,sc,Prod)

	
	_DeleteDate(Date,idxfname,datapath,Confirm)
