import numpy as np

def CDFtoRecarray(cdf):
	'''
	Converts a pysatCDF object to a numpy recarray.
	
	'''
	
	#get list of dtypes
	dtype = []
	keys = list(cdf.data.keys())
	nk = np.size(keys)
	
	dtkey = ''
	
	for i in range(0,nk):
		if isinstance(cdf.data[keys[i]][0],np.datetime64):
			#convert to Date and ut
			dtkey = keys[i]
			dtype.append(('Date','int32'))
			dtype.append(('ut','float32'))
			break
		else:
			dtype.append((keys[i],cdf.data[keys[i]].dtype,cdf.data[keys[i]].shape[1:]))
			
	
	#find the length
	n = cdf.data[keys[i]].shape[0]
	
	#create the output array
	data = np.recarray(n,dtype=dtype)
	
	for k in keys:
		if k == dtkey:
			#convert to Date and ut
			datestr = cdf.data[k].astype('U')
			for i in range(0,n):
				s = datestr[i].split('T')
				d = np.array(s[0].split('-')).astype('int32')
				t = np.array(s[1].split(':')).astype('float32')
				data.Date[i] = d[0]*10000 + d[1]*100 + d[2]
				data.ut[i] = t[0] + t[1]/60.0 + t[2]/3600.0
		else:
			data[k] = cdf.data[k]
			
	return data,cdf.meta
