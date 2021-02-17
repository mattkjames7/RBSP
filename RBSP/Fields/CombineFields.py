import numpy as np
from ..EMFISIS.InterpObj import InterpObj
from ..EFW.ReadCDF import ReadCDF
from ..Tools.ContUT import ContUT
from ..Tools.mGSEtoGSE import mGSEtoGSE,GSEtomGSE
import PyGeopack as gp
from ..Tools.GSMtoDipolar import GSMtoDipolar
from ..Tools.GetTraceFuncs import GetTraceFuncs
import cdflib
from . import _Fields
from .CalculateEx import CalculateEx
from .ModelField import ModelField
import os
import RecarrayTools as RT
from .. import EMFISIS
from ..Tools.ConvertTime import ConvertTime
import DateTimeTools as TT

def CombineFields(Date,sc,Overwrite=False):
	'''
	Combine the electric and magnetic fields together (where possible).
	The electric field will be rotated from the mGSE coordinate system 
	provided by the EFW data files to GSE, GSM and SM coordinates.
	
	In cases where there are EFW data, the magnetic field will be 
	interpolated to the EFW time line. When there are no EFW data, then
	an artificial time axis with ~10s resolution will be used.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	sc : str
		'a' or 'b'
		
		
	'''
	#check it exists
	outdir = _Fields.datapath.format(sc)
	if not os.path.isdir(outdir):
		os.system('mkdir -pv '+outdir)
	fname = outdir + '{:08d}.bin'.format(Date)
	if os.path.isfile(fname) and not Overwrite:
		print('File exists, use "Overwrite" option to update the file')
		return
	
	#read the E data in
	print('Reading E field data')
	data,_ = ReadCDF(Date,sc,'l3')

	if data is None:
		n = 8640
		ut = np.arange(n)/360.0
		eDate = np.zeros(n,dtype='int32') + Date
		utc = TT.ContUT(eDate,ut)
	else:
		#get date and time and continuous time
		print('Calculating time')
		eDate,ut,utc = ConvertTime(data['epoch'])
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
	
	#calculate the Model field
	print('Calculating model field')
	mx,my,mz = ModelField(out.Xgse,out.Ygse,out.Zgse,out.Date,out.ut)
	out.mBxSM,out.mBySM,out.mBzSM = gp.GSEtoSM(mx,my,mz,out.Date,out.ut)
	
	#get the magnetic field interpolation objects
	print('Obtaining magnetic field interpolation objects')
	fx,fy,fz = InterpObj(Date,sc,Coords='GSE')
	mag,_ = EMFISIS.ReadCDF(Date,sc=sc,L='l3',Prod='4sec-gse')
	mDate,mut,mutc = ConvertTime(mag['Epoch'])
	mbad = mag['magInvalid']
	mbadi = np.where(mbad)[0]
	
	#get the magnetic field
	print('Interpolating magnetic field')
	out.BxGSE = fx(utc)
	out.ByGSE = fy(utc)
	out.BzGSE = fz(utc)
	

	
	#get mGSE E field and GSE spin axis
	if not data is None:
		print('Converting mGSE to GSE')
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
	else:
		out.ExGSE[:] = np.nan
		out.EyGSE[:] = np.nan
		out.EzGSE[:] = np.nan
	
		out.ExGSM[:] = np.nan
		out.EyGSM[:] = np.nan
		out.EzGSM[:] = np.nan
	
		out.ExSM[:] = np.nan
		out.EySM[:] = np.nan
		out.EzSM[:] = np.nan
	
		out.EP[:] = np.nan
		out.ET[:] = np.nan
		out.EC[:] = np.nan
	
	#convert to other coordinate systems
	#GSM
	print('Calculating GSM vectors')
	if not data is None:
		out.ExGSM,out.EyGSM,out.EzGSM = gp.GSEtoGSM(out.ExGSE,out.EyGSE,out.EzGSE,out.Date,out.ut)
	out.BxGSM,out.ByGSM,out.BzGSM = gp.GSEtoGSM(out.BxGSE,out.ByGSE,out.BzGSE,out.Date,out.ut)
	
	#SM
	print('Calculating SM vectors')
	if not data is None:
		out.ExSM,out.EySM,out.EzSM = gp.GSMtoSM(out.ExGSM,out.EyGSM,out.EzGSM,out.Date,out.ut)
	out.BxSM,out.BySM,out.BzSM = gp.GSMtoSM(out.BxGSM,out.ByGSM,out.BzGSM,out.Date,out.ut)
	
	#ptc (poloidal,toroidal,compressional)
	print('Calculating PTC vectors')
	if not data is None:
		out.EP,out.ET,out.EC = GSMtoDipolar(out.ExSM,out.EySM,out.EzSM,out.mBxSM,out.mBySM,out.mBzSM,out.Xsm,out.Ysm,out.Zsm)
	out.BP,out.BT,out.BC = GSMtoDipolar(out.BxSM,out.BySM,out.BzSM,out.mBxSM,out.mBySM,out.mBzSM,out.Xsm,out.Ysm,out.Zsm)
	
	#scan for bad data flags
	out.Step[:] = 0
	for b in mbadi:
		#before the step
		try:
			use0 = np.where(out.utc <= mutc[b])[0][-1]
			out.Step[use0] = 1
		except:
			pass
		#after the step
		try:
			use1 = np.where(out.utc > mutc[b])[0][0]
			out.Step[use1] = 2
		except:
			pass
	
	#save the file
	print('Saving: {:s}'.format(fname))
	RT.SaveRecarray(out,fname)
	
	
	
	
