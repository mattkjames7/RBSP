import numpy as np
from ..Tools.Downloading._RebuildDataIndex import _RebuildDataIndex
from . import _ECT


def RebuildDataIndex(sc,Inst,L):
	'''
	Rebuilds the data index for a data product.

	Inputs
	======
	sc : str
		'a' or 'b'
	Inst: str
		'hope', 'mageis' or 'rept' 
	L : str
		Level of data to download



	Available data products
	=======================
	hope: 'l2.sectors'|'l2.spinaverage'|'l3.moments'|'l3.pitchangle'
	mageis: 'l2'|'l3'
	rept: 'l2'|'l3'
	'''		
	idxfname = _ECT.idxfname.format(Inst,L,sc)
	datapath = _ECT.datapath.format(Inst,L,sc)

	vfmt = _ECT.vfmt

	
	_RebuildDataIndex(datapath,idxfname,vfmt)
