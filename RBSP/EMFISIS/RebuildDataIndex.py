import numpy as np
from ..Tools.Downloading._RebuildDataIndex import _RebuildDataIndex
from . import _EMFISIS


def RebuildDataIndex(sc,L,prod):
	'''
	Rebuilds the data index for a data product.

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
	'''		
	if L == 'l4':
		idxfname = _EMFISIS.idxfnamel4.format(L,sc)
		datapath = _EMFISIS.datapathl4.format(L,sc)
	else:
		idxfname = _EMFISIS.idxfname.format(L,sc,Prod)
		datapath = _EMFISIS.datapath.format(L,sc,Prod)

	vfmt = _EMFISIS.vfmt

	
	_RebuildDataIndex(datapath,idxfname,vfmt)
