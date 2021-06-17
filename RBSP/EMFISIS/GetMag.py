import numpy as np
import DateTimeTools as TT
from .ReadCDF import ReadCDF
from ._MagRecarray import _MagRecarray
from .DataAvailability import DataAvailability

def GetMag(Date,sc,ut=[0.0,24.0],Coord='GSM',Res='1sec'):
	'''
	Get the magnetometer data for a given time period.
	
	Inputs
	======
	Date : int
		Date e.g 20130101 or date range e.g. [20130101,20130204]
	sc : str
		'a'|'b'
	ut : float
		Start and end times in hours.
	Coord : str
		'GSE'|'GSM'|'SM'|'GEO'|'GEI'
	Res : str
		'1sec'|'4sec'|'hires'
		
	Returns
	=======
	data : numpy.recarray
		Array containing the magnetometer data
		
	
	'''

	#get a list of dates
	if np.size(Date) == 1:
		dates = np.array([Date]).flatten()
	else:
		dates = TT.ListDates(Date[0],Date[1])
	
	#prod string
	prod = Res + '-' + Coord.lower()
	
	#check availability
	adates = DataAvailability(sc,'l3',prod)
	good = np.zeros(dates.size,dtype='bool')
	for i in range(0,dates.size):
		good[i] = dates[i] in adates
	use = np.where(good)[0]
	dates = dates[good]
	
	#read each one in
	datal = []
	n = 0
	for i in range(0,dates.size):
		cdf,_ = ReadCDF(dates[i],sc,'l3',prod)
		tmp = _MagRecarray(cdf)
		datal.append(tmp)
		n += tmp.size

	#define the dtype of the output
	dtype = [	('Date','int32'),
				('ut','float32'),
				('utc','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64'),
				('Bm','float64'),
				('Bad','bool8'),
				('RangeFlag','int8'),
				('CalState','bool8'),
				('Invalid','bool8'),
				('Filled','bool8'),]
	
	#create output array
	data = np.recarray(n,dtype=dtype)
	
	#fill it
	p = 0
	for i in range(0,dates.size):
		data[p:p+datal[i].size] = datal[i]
		p += datal[i].size
		
	#restrict to ut range
	utc0 = TT.ContUT(dates[0],ut[0])[0]
	utc1 = TT.ContUT(dates[-1],ut[1])[0]
	use = np.where(( data.utc >= utc0) & (data.utc <= utc1))[0]
	
	return data[use]
