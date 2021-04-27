import numpy as np
from .. import Globals
import RecarrayTools as RT
from . import _ECT
import os
import DateTimeTools as TT

def ReadIonMoments(Date,sc):
	'''
	Read in the corrected ion moments calculated using the HOPE spectra
	alongside EMFISIS and EFW.
	
	Inputs
	======
	Date : int
		Date in the format yyyymmdd
	sc : str
		'a' or 'b'
		
	Returns
	=======
	data : numpy.recarray
		Ion moment data
	
	'''
		
	outdir = Globals.DataPath + 'Moments/Ions/{:s}/'.format(sc)
	
	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = TT.ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()	
	
	
	#count each one
	n = 0
	for d in dates:
		fname = outdir + '{:08d}.bin'.format(d)
		if os.path.isfile(fname):
			f = open(fname,'rb')
			n += np.fromfile(f,dtype='int32',count=1)[0]
			f.close()
		
	#create output array
	out = np.recarray(n,dtype=_ECT.idtype)
	
	#read in the data
	p = 0
	for d in dates:
		fname = outdir + '{:08d}.bin'.format(d)
		if os.path.isfile(fname):
			data = RT.ReadRecarray(fname,_ECT.idtype)
			out[p:p+data.size] = data
			p += data.size
		
	return out
	
	
	
	
	
