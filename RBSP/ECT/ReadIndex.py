import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from . import _ECT

def ReadIndex(sc='a',Inst='hope',L='l3.moments'):
	'''
	Reads the index file for a given data product.
	
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
	
	
	Returns
	=======
	numpy.recarray
	
	'''
	return _ReadDataIndex(_ECT.idxfname.format(Inst,L,sc))
