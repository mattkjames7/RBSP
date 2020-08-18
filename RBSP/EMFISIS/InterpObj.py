import numpy as np
from .ReadCDF import ReadCDF
from scipy.interpolate import interp1d
from scipy.ndimage import uniform_filter
from ..Tools.ContUT import ContUT
import cdflib 

def InterpObj(Date,sc='a',Coords='GSE',Res='1sec',Smooth=None):
	'''
	Return interpolation objects for MGF data.
	
	'''
	#get the product string
	Prod = Res + '-' + Coords.lower()
	L = 'l3'
		
	#read the data in
	mag,meta = ReadCDF(Date,sc,L,Prod)
	
	#get the date and time
	dt = np.array(cdflib.cdfepoch.breakdown(mag['Epoch']))
	Date = dt[:,0]*10000 + dt[:,1]*100 + dt[:,2]
	ut = np.float32(dt[:,3]) + np.float32(dt[:,4])/60.0 + np.float32(dt[:,5])/3600.0 + np.float32(dt[:,6])/3.6e6 + np.float32(dt[:,7])/3.6e9
	
	#get continuous time
	mutc = ContUT(Date,ut)
	
	#interpolate the bad data
	good = np.isfinite(mag['Mag']).all(axis=1) & (mag['magInvalid'] == 0)
	good = np.where(good)[0]
	bad = np.where(good == False)[0]

	fx = interp1d(mutc[good],mag['Mag'][good,0],bounds_error=False,fill_value='extrapolate')
	fy = interp1d(mutc[good],mag['Mag'][good,1],bounds_error=False,fill_value='extrapolate')
	fz = interp1d(mutc[good],mag['Mag'][good,2],bounds_error=False,fill_value='extrapolate')
	
	if not Smooth is None:
	
		mag['Mag'][bad,0] = fx(mutc[bad])
		mag['Mag'][bad,1] = fy(mutc[bad])
		mag['Mag'][bad,2] = fz(mutc[bad])
			


		#interpolation objects
		fx = interp1d(mutc,uniform_filter(mag['Mag'][:,0],Smooth),bounds_error=False,fill_value='extrapolate')
		fy = interp1d(mutc,uniform_filter(mag['Mag'][:,1],Smooth),bounds_error=False,fill_value='extrapolate')
		fz = interp1d(mutc,uniform_filter(mag['Mag'][:,2],Smooth),bounds_error=False,fill_value='extrapolate')
		
		
	return fx,fy,fz
