import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from . import _EFW

def ReadIndex(sc='a',L='l3'):
	'''
	Reads the index file for a given data product.
	
	Inputs
	======
	sc : str
		'a' or 'b'
	L : str
		Level of data to download



	Available data products
	=======================
	'l3' (Spin-fit Electric field in modified-GSE (MGSE) coord, density, and other products)
	'l2.spec' (8 second FFT power spectra)
	'l2.e-spinfit-mgse' (Spin-fit E12 Electric field in modified-GSE (MGSE) coordinates)
	'l2.fbk' (8 sample/sec filterbank peak, average wave amplitude)
	'l2.esvy_despun' (32 sample/sec despun electric field in modified-GSE (MGSE) coordinates)
	'l2.vsvy-hires' (16 sample/sec single-ended V1-V6 probe potentials)
	'l1.eb1' (EB1 in UVW coordinates)
	'l1.eb2' (EB2 in UVW coordinates)
	'l1.mscb1' (MSCB1 in UVW coordinates)
	'l1.mscb2' (MSCB2 in UVW coordinates)
	'l1.vb1' (VB1 in UVW coordinates)
	'l1.vb2'(VB2 in UVW coordinates)
	
	
	Returns
	=======
	numpy.recarray
	
	'''
	return _ReadDataIndex(_EFW.idxfname.format(L,sc))
