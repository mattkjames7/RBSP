import numpy as np
import DateTimeTools as TT

def _MagRecarray(cdf):
	'''
	Convert the cdf dictionary to a numpy recarray.
	
	'''
	
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

	#get the number of elements
	n = cdf['Epoch'].size
	
	#create the output array
	data = np.recarray(n,dtype=dtype)
	
	#calculate time
	data.Date,data.ut = TT.CDFEpochtoDate(cdf['Epoch'])
	data.utc = TT.ContUT(data.Date,data.ut)
	
	#fill the rest of the fields
	data.Bx = cdf['Mag'][:,0]
	data.By = cdf['Mag'][:,1]
	data.Bz = cdf['Mag'][:,2]
	data.Bm = cdf['Magnitude']
	data.RangeFlag = cdf['range_flag']
	data.CalState = cdf['calState'].astype('bool8')
	data.Invalid = cdf['magInvalid'].astype('bool8')
	data.Filled = cdf['magFill'].astype('bool8')
	
	#determine bad data flag
	data.Bad = data.Invalid | data.CalState | data.Filled | (np.isfinite(data.Bx) == False) | (data.Bx < -1e30)
	
	#fill bad with nans
	bad = np.where(data.Bad)[0]
	data.Bx[bad] = np.nan
	data.By[bad] = np.nan
	data.Bz[bad] = np.nan
	data.Bm[bad] = np.nan

	return data
