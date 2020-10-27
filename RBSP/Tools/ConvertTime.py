import numpy as np
from .ContUT import ContUT
import cdflib

def ConvertTime(epoch):
	
	dt = np.array(cdflib.cdfepoch.breakdown(epoch))
	Date = dt[:,0]*10000 + dt[:,1]*100 + dt[:,2]
	ut = np.float32(dt[:,3]) + np.float32(dt[:,4])/60.0 + np.float32(dt[:,5])/3600.0 + np.float32(dt[:,6])/3.6e6 + np.float32(dt[:,7])/3.6e9
	utc = ContUT(Date,ut)	
	return Date,ut,utc
	
	
	
