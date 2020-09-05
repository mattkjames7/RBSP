import numpy as np
from .ReadData import ReadData
from ..Tools.ListDates import ListDates
from ..Tools.ContUT import ContUT
from . import _Fields

def GetData(Date,ut=[0.0,24.0],sc='a',Verbose=True):
	'''
	Get data from muiltiple dates
	
	'''
	#Get the list of dates
	if np.size(Date) == 1:
		dates = np.array([Date]).flatten()
		dater = [dates[0],dates[0]]
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
		dater = [dates[0],dates[-1]]
	else:
		dates = np.array(Date).flatten()
		dater = [np.min(dates),np.max(dates)]
		
	#get the time range to include
	utcr = ContUT(dater,np.array(ut))

	#now count the file sizes
	nd = dates.size
	n = 0
	for i in range(0,nd):
		if Verbose:
			print('\rCounting records from file {0} of {1} ({2})'.format(i+1,nd,n),end='')
		n += ReadData(dates[i],sc,Size=True)
		
	if Verbose:
		print('\rCounting records from file {0} of {1} ({2})'.format(i+1,nd,n))
		
	#create the output array
	out = np.recarray(n,dtype=_Fields.dtype)
	
	#load the data
	p = 0	
	for i in range(0,nd):
		if Verbose:
			print('\rReading file {0} of {1}'.format(i+1,nd),end='')
		tmp = ReadData(dates[i],sc,Size=False)
		out[p:p+tmp.size] = tmp
		p += tmp.size
		
	if Verbose:
		print('\rReading file {0} of {1}'.format(i+1,nd))

	#limit the time
	use = np.where((out.utc >= utcr[0]) & (out.utc <= utcr[1]))[0]
	out = out[use]

	return out
