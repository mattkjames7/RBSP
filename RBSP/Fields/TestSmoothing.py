import numpy as np
import matplotlib.pyplot as plt
from ..EMFISIS.InterpObj import InterpObj
from ..EFW.ReadCDF import ReadCDF
from ..Tools.ContUT import ContUT
import cdflib
from . import _Fields
from scipy.signal import savgol_filter
from ..Tools.GetTraceFuncs import GetTraceFuncs
from scipy.ndimage import uniform_filter
import DateTimeTools as TT
from .SmoothFuncs import *
from .ModelField import ModelField

def TestSmoothing(Date,sc='a',Ind=0,Dt=300,Comp='x'):
	
	
	#read the E data in
	print('Reading E field data')
	data,_ = ReadCDF(Date,sc,'l3')

	#get date and time and continuous time
	print('Calculating time')
	dt = np.array(cdflib.cdfepoch.breakdown(data['epoch']))
	eDate = dt[:,0]*10000 + dt[:,1]*100 + dt[:,2]
	ut = np.float32(dt[:,3]) + np.float32(dt[:,4])/60.0 + np.float32(dt[:,5])/3600.0 + np.float32(dt[:,6])/3.6e6 + np.float32(dt[:,7])/3.6e9
	utc = ContUT(eDate,ut)
	n = utc.size
	
	#create the output array
	out = np.recarray(n,_Fields.dtype)
	out.Date = eDate
	out.ut = ut
	out.utc = utc

	
	#we need footprints and positions
	TF = GetTraceFuncs(sc)
	keys = list(TF.keys())
	for k in keys:
		print('\rInterpolating field: {:8s}'.format(k),end='')
		out[k] = TF[k](out.utc)
	print()	
	
	R = np.sqrt(out.Xsm**2 + out.Ysm**2 + out.Zsm**2)
	minR = (R[1:-1] <= R[:-2]) & (R[1:-1] <= R[2:]) 
	minR = np.where(minR)[0][Ind] + 1
	print(minR-Dt,minR+Dt)
	use = np.arange(R.size)[minR-Dt:minR+Dt]
	
	print('Calculating smoothed field')
#	fsx,fsy,fsz = InterpObj(Date,sc,Coords='GSE')#
#	mx,my,mz = fsx(utc),fsy(utc),fsz(utc)	
#	Bm = np.sqrt(mx**2 + my**2 + mz**2)
#	mx,my,mz = SavgolSmoothPol(mx,my,mz)
#	mx,my,mz = SavgolSmooth(mx,my,mz)
#	mx,my,mz = FilterSmooth(mx,my,mz)
	mx,my,mz = ModelField(out.Xgse,out.Ygse,out.Zgse,out.Date,out.ut)
	mx,my,mz = gp.GSEtoSM(mx,my,mz,out.Date,out.ut)


	#get the magnetic field interpolation objects
	print('Obtaining magnetic field interpolation objects')
	fx,fy,fz = InterpObj(Date,sc,Coords='GSE')
	
	#get the magnetic field
	print('Interpolating magnetic field')
	out.BxGSE = fx(utc)
	out.ByGSE = fy(utc)
	out.BzGSE = fz(utc)
	out.BzSM,out.BySM,out.BzSM = gp.GSEtoSM(out.BxGSE,out.ByGSE,out.BzGSE,out.Date,out.ut)
	
	#field magnitude
	B = np.sqrt(out.BxSM**2 + out.BySM**2 + out.BzSM**2)
		
		
	fig = plt
	fig.figure()
	ax0 = fig.subplot2grid((2,1),(0,0))
	ax1 = fig.subplot2grid((2,1),(1,0))


	if Comp == 'x':
		d = out.BxSM
		m = mx
	elif Comp == 'y':
		d = out.BySM
		m = my
	elif Comp == 'z':
		d = out.BzSM
		m = mz
	else:
		d = B
		m = Bm
		
	ax0.plot(d[use],color='black')
	ax0.plot(m[use],color='red')

	ax1.plot(d[use] - m[use],color='blue')

	return d[use],m[use],out[use]
