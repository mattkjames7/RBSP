import numpy as np
import DateTimeTools as TT
from .ReadCDF import ReadCDF

def ReadElectronDensity(Date,sc):
	'''
	Read the level-3 electron density measurements derived from 
	spacecaft potential.
	
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
				('Vsc','float32')]
	
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
		cdf,_ = ReadCDF(d,sc,L='l3')
		cdfs.append(cdf)
		
	#get the length of the data
	n = 0 
	for c in cdfs:
		if not c is None:
			n += np.size(c['epoch'])

	#create the output array
	data = np.recarray(n,dtype=dtype)
	
	#fill it
	p = 0
	for c in cdfs:
		if not c is None:
			d,t = TT.CDFEpochtoDate(c['epoch'])
			nt = d.size
			utc = TT.ContUT(d,t)

			data[p:p+nt].Date = d
			data[p:p+nt].ut = t
			data[p:p+nt].utc = utc

			bad = np.where((c['density'] <= 0) | (np.isfinite(c['density']) == False))[0]
			data[p:p+nt].density = c['density']
			data[p:p+nt].density[bad] = np.nan
			
			bad = np.where((c['Vavg'] < -100) | (np.isfinite(c['Vavg']) == False))[0]
			data[p:p+nt].Vsc = c['Vavg']
			data[p:p+nt].Vsc[bad] = np.nan		
			p+= nt

	#sort
	srt = np.argsort(data.utc)
	data = data[srt]
	
	return data
