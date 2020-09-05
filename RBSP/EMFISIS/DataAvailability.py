import numpy as np
from .ReadIndex import ReadIndex

def DataAvailability(sc='a',L='l4',Prod=None):
	'''
	Provide a list of dates for which there are data.

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
	'l3'	 	'4sec-***'	4-second resolution magnetic fields
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
	There may be others - they should download given the appropriate Prod string
			
	*** can be either 'gei','geo','gse','gsm' or 'sm'
	
	
	'''
	idx = ReadIndex(sc,L,Prod)
	return np.unique(idx.Date)
