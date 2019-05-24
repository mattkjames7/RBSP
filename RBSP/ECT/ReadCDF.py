import numpy as np
from .. import Globals
from ..Tools.CDFtoRecarray import CDFtoRecarray
from ._ReadDataIndex import _ReadDataIndex
import pysatCDF

def ReadCDF(Date,sc='a',Inst='hope',L='l3.moments'):
	'''
	Reads the data from a CDF file.
	
	'''
	
	idx = _ReadDataIndex(sc,Inst,L)
	path = Globals.DataPath+'ECT/{:s}/{:s}/{:s}/'.format(Inst,L,sc)

	use = np.where(idx.Date == Date)[0]
	if use.size == 0:
		print('Date not found')
		return None
	
	fname = path + idx[use[0]].FileName
	cdf = pysatCDF.CDF(fname)
	return cdf.data,cdf.meta
