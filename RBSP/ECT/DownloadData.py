from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData
from . import _ECT
from .URL import URL

def DownloadData(sc='a',Inst='hope',L='l3.moments',Date=[20120901,20200101],Overwrite=False,Verbose=True):
	'''
	Downloads ECT data.

	
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
	URLF = URL(sc,Inst,L)
	_DownloadData(URLF,_ECT.idxfname.format(Inst,L,sc),_ECT.datapath.format(Inst,L,sc),
			Date,_ECT.vfmt,None,Overwrite,Verbose)
	
	
