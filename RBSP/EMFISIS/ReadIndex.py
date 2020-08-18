import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from . import _EMFISIS

def ReadIndex(sc='a',L='l4',Prod=None):
	'''
	Reads the index file for a given data product.
	
	Inputs
	======
	sc: str
		'a' or 'b'
	L: str
		Data level, see below
	Prod: str
		Data product
			



	Available data products
	=======================
	Level 		Prod		Description
	'l4' 		None		densities
	'l3'	 	'1sec-***'	1-second resolution magnetic fields
	'l3'	 	'1sec-***'	4-second resolution magnetic fields
	'l3'	 	'hires-***'	High resolution magnetic fields
	'l2'		'HFR-spectra'
	'l2'		'HFR-spectra-merged'
	'l2'		'HFR-spectra-burst'
	'l2'		'HFR-waveform'
	'l2'		'WFR-spectral-matrix'
	'l2'		'WFR-spectral-matrix-burst'
	'l2'		'WFR-spectral-matrix-burst-diagonal'
	'l2'		'WFR-spectral-matrix-diagonal-merged'
	'l2'		'WFR-spectral-matrix-diagonal'
	'l2'		'WFR-waveform'
	'l2'		'WFR-waveform-continuous-burst'
	
	Returns
	=======
	numpy.recarray
	
	'''
	if L == 'l4':
		idxfname = _EMFISIS.idxfnamel4.format(L,sc)
	else:
		idxfname = _EMFISIS.idxfname.format(L,sc,Prod)

	return _ReadDataIndex(idxfname)
