import numpy as np
from .. import Globals
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from ..Tools.ReadCDF import ReadCDF as RCDF
from . import _EFW
import os

def ReadCDF(Date,sc='a',L='l3'):
	'''
	Reads the data from a CDF file.
	
	'''
	
	#read the data index
	idx = _ReadDataIndex(_EFW.idxfname.format(L,sc))
	
	#check the index for the appropriate date
	use = np.where(idx.Date == Date)[0]
	if use.size == 0:
		print('Date not found, run RBSP.EFW.DownloadData() to check for updates.')
		return None,None
	idx = idx[use]
	mx = np.where(idx.Version  == np.max(idx.Version))[0]
	mx = mx[0]
	
	#get the file name
	fname = _EFW.datapath.format(L,sc) + idx[mx].FileName


	#check file exists
	if not os.path.isfile(fname):
		print('Index is broken: Update the data index')
		return None,None
		
	#read the file
	return RCDF(fname)

