import numpy as np
import DateTimeTools as TT
from ._ReadPotential import _ReadPotential
from . import _EFW

def GetPotential(Date,sc):
	
	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = TT.ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	#find the number of records
	n = 0
	for i in range(0,dates.size):
		n += _ReadPotential(Date,sc,Size=True)
		
	#create the output array
	out = np.recarray(n,dtype=_EFW.pdtype)
	
	#read the data in
	p = 0
	for i in range(0,dates.size):
		tmp = _ReadPotential(Date,sc,Size=False)
		out[p:p+tmp.size] = tmp
		p += tmp.size
		
	return out
