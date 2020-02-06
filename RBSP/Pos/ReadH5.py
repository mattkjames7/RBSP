import numpy as np
from .. import Globals
from ..Tools.CDFtoRecarray import CDFtoRecarray
from ._ReadDataIndex import _ReadDataIndex
import h5py

def ReadH5(Date,sc='a'):
	'''
	Reads the data from a H5 file.
	
	'''
	
	idx = _ReadDataIndex(sc)
	path = Globals.DataPath+'MagEph/{:s}/'.format(sc)

	use = np.where(idx.Date == Date)[0]
	if use.size == 0:
		print('Date not found')
		return None
	
	fname = path + idx[use[0]].FileName
	data = h5py.File(fname,'r')
	return data
