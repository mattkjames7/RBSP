import numpy as np
import DateTimeTools as TT
from .ReadCDF import ReadCDF

def ReadElectronDensity(Date,sc):
	'''
	Read the level-4 electron density measurements.
	
	Inputs
	======
	Date : int
		Date in format yyyymmdd
	sc : str
		'a' or 'b'
		
	Returns
	=======
	data : numpy.recarray
		Recarray containing density data.
	
	'''
	#define the dtype
	dtype = [	('Date','int32'),
				('ut','float32'),
				('utc','float64'),
				('density','float32'),
				('bmag','float32'),
				('fce','float32'),
				('fpe','float32'),
				('fuh','float32'),
				('wpe_over_wce','float32')]
	
	#get a list of dates
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = TT.ListDates(Date[0],Date[1])
	else:
		dates = np.array(Date)
	
	
	#read the cdf(s)
	cdfs = []
	for d in dates:
		cdf,_ = ReadCDF(d,sc,L='l4',Prod=None)
		cdfs.append(cdf)
		
	#get the length of the data
	n = 0 
	for c in cdfs:
		n += np.size(c['Epoch'])

	#create the output array
	data = np.recarray(n,dtype=dtype)
	
	#fill it
	p = 0
	fields = ['density','fpe','fce','fuh','bmag','wpe_over_wce']
	for c in cdfs:
		d,t = TT.CDFEpochtoDate(c['Epoch'])
		nt = d.size
		utc = TT.ContUT(d,t)

		data[p:p+nt].Date = d
		data[p:p+nt].ut = t
		data[p:p+nt].utc = utc

		bad = np.where((c['density'] <= 0) | (np.isfinite(c['density']) == False))[0]
		for f in fields:
			data[p:p+nt][f] = c[f]
			data[p:p+nt][f][bad] = np.nan
		
		p+= nt

	#sort
	srt = np.argsort(data.utc)
	data = data[srt]
	
	return data
