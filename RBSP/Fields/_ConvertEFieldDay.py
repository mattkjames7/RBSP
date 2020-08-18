import numpy as np
from ..EMFISIS.InterpObj import InterpObj
from ..EFW.ReadCDF import ReadCDF
from ..Tools.ContUT import ContUT
from ..Tools.mGSEtoGSE import mGSEtoGSE,GSEtomGSE
import PyGeopack as gp
from ..Pos.ReadFieldTraces import ReadAllFootprintTraces

def _ConvertEFieldDay(Date,sc,TraceFuncs=None):
	'''
	Convert the coordinate systems of the E field for a day of data
	
	
	'''
	
	#read the E data in
	data,_ = ReadCDF(Date,sc,'l3')

	#get date and time and continuous time
	dt = np.array(cdflib.cdfepoch.breakdown(data['epoch']))
	Date = dt[:,0]*10000 + dt[:,1]*100 + dt[:,2]
	ut = np.float32(dt[:,3]) + np.float32(dt[:,4])/60.0 + np.float32(dt[:,5])/3600.0 + np.float32(dt[:,6])/3.6e6 + np.float32(dt[:,7])/3.6e9
	utc = ContUT(Date,ut)
	n = utc.size
	
	#create the output array
	out = np.recarray(n,_EFW.dtype)
	out.Date = Date
	out.ut = ut
	out.utc = utc
	
	
	#get the magnetic field interpolation objects
	fx,fy,fz = InterpObj(Date,sc)
	
	#get the magnetic field
	out.BxGSE = fx(utc)
	out.ByGSE = fy(utc)
	out.BzGSE = fz(utc)
	
	#get mGSE E field and GSE spin axis
	Ex,Ey,Ez = data['efield_inertial_frame_mgse'].T
	bad = np.where((np.isfinite(Ey) == False) | (np.isfinite(Ez) == False) | (Ey < -1000.0) | (Ey > 1000.0) | (Ez < -1000.0) | (Ez > 1000.0))[0]
	Ey[bad] = np.nan
	Ez[bad] = np.nan
	Sx,Sy,Sz = data['spinaxis_gse'].T
	
	#convert B to mGSE
	Bx,By,Bz = GSEtomGSE(out.BxGSE,out.ByGSE,out.BzGSE,Sx,Sy,Sz)
	
	#calculate the Ex component
	Ex = CalculateEx(Ey,Ez,Bx,By,Bz)
	
	#convert back to GSE
	out.ExGSE,out.EyGSE,out.EzGSE = mGSEtoGSE(Ex,Ey,Ez,Sx,Sy,Sz)
	
	#convert to other coordinate systems
	#GSM
	
	#SM
	
	#plc (poloidal,toroidal,compressional)
	
	
	#we need footprints and positions
	
	
	#calculate the Model field
	
	
	
	
	
	#save the file
	
	
	
	
	
