import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from ..Tools.ReadCDF import ReadCDF as RCDF
from . import _ECT
import os


def ReadCDF(Date,sc='a',Inst='hope',L='l3.moments'):
	'''
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
	
	#read the data index
	idx = _ReadDataIndex(_ECT.idxfname.format(Inst,L,sc))
	
	#check the index for the appropriate date
	use = np.where(idx.Date == Date)[0]
	if use.size == 0:
		print('Date not found, run RBSP.EFW.DownloadData() to check for updates.')
		return None,None
	idx = idx[use]
	mx = np.where(idx.Version  == np.max(idx.Version))[0]
	mx = mx[0]
	
	#get the file name
	fname = _ECT.datapath.format(Inst,L,sc) + idx[mx].FileName


	#check file exists
	if not os.path.isfile(fname):
		print('Index is broken: Update the data index')
		return None,None
		
	#read the file
	return RCDF(fname)
