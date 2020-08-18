import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from ..Tools.ReadCDF import ReadCDF as RCDF
from . import _EMFISIS
import os

def ReadCDF(Date,sc='a',L='l4',Prod=None):
	'''
	Reads the data from a CDF file.
	
	'''

	if L == 'l4':
		fc = None
		idxfname = _EMFISIS.idxfnamel4.format(L,sc)
		datapath = _EMFISIS.datapathl4.format(L,sc)
	else:
		fc = Prod + '_emfisis'
		idxfname = _EMFISIS.idxfname.format(L,sc,Prod)
		datapath = _EMFISIS.datapath.format(L,sc,Prod)
	
	#read the data index
	idx = _ReadDataIndex(idxfname)
	
	#check the index for the appropriate date
	use = np.where(idx.Date == Date)[0]
	if use.size == 0:
		print('Date not found, run RBSP.EMFISIS.DownloadData() to check for updates.')
		return None,None
	idx = idx[use]
	mx = np.where(idx.Version  == np.max(idx.Version))[0]
	mx = mx[0]
	
	#get the file name
	fname = datapath + idx[mx].FileName


	#check file exists
	if not os.path.isfile(fname):
		print('Index is broken: Update the data index')
		return None,None
		
	#read the file
	return RCDF(fname)

