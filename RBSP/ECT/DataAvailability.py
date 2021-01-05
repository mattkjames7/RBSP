import numpy as np
from .ReadIndex import ReadIndex

def DataAvailability(sc='a',Inst='hope',L='l3.moments'):
	'''
	Provide a list of dates for which there are data.

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
	idx = ReadIndex(sc,Inst,L)
	return np.unique(idx.Date)
