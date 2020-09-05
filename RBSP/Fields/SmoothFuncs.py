import numpy as np
import DateTimeTools as TT
from scipy.ndimage import uniform_filter
from scipy.signal import savgol_filter
from ..Tools.SmoothAngles import SmoothAngles
import PyGeopack as gp

def cart2pol(x,y,z):
	
	r = np.sqrt(x**2 + y**2 + z**2)
	phi = np.arctan2(y,x)
	theta = np.arccos(z/r)

	return r,phi,theta
	
def pol2cart(r,phi,theta):
	
	x = r*np.sin(theta)*np.cos(phi)
	y = r*np.sin(theta)*np.sin(phi)
	z = r*np.cos(theta)

	return x,y,z

def FilterSmooth(x,y,z,inter=11.0,low=1800):
	'''
	Use low pass filter
	
	'''
	
	
	newx = TT.lsfilter(x,inter,low,inter,True) 
	newy = TT.lsfilter(y,inter,low,inter,True) 
	newz = TT.lsfilter(z,inter,low,inter,True) 

	return newx,newy,newz
	
def UniformSmooth(x,y,z,size=600):
	'''
	Use the uniform filter
	
	'''
	newx = uniform_filter(x,size=size)
	newy = uniform_filter(y,size=size)
	newz = uniform_filter(z,size=size)	
	
	
	return newx,newy,newz
	
def SavgolSmooth(x,y,z,Window=163,Order=4):
	'''
	Use the savgol filter
	
	'''
	newx = savgol_filter(x,Window,Order)
	newy = savgol_filter(y,Window,Order)
	newz = savgol_filter(z,Window,Order)
	
	return newx,newy,newz
	

def SavgolSmoothPol(x,y,z,Window=163,rOrder=4,tOrder=2,pOrder=2):
	'''
	Savgol filter on polar coords
	
	'''
	
	#convert to polar
	r,p,t = cart2pol(x,y,z)
	
	#filter
	newr = np.sinh(savgol_filter(np.arcsinh(r),Window,rOrder))
	newp = savgol_filter(SmoothAngles(p,Units='rad'),Window,pOrder)
	newt = savgol_filter(t,Window,tOrder)
	
	#return to cartesian
	newx,newy,newz = pol2cart(newr,newp,newt)
	
	return newx,newy,newz

