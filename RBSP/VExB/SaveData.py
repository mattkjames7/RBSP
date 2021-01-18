import numpy as np
from ..Fields.GetData import GetData
from ..Fields.DataAvailability import DataAvailability
from ..Pos.GetVelocity import GetVelocity
import DateTimeTools as TT
from scipy.interpolate import interp1d
from . import _VExB
import kpindex
from .VExB import VExB
import RecarrayTools as RT
import os
from ..Fields.ConvertEFieldDay import ConvertEFieldDay
import vsmodel
import pyomnidata as omni

def SaveData(Date,sc,Overwrite=False):
	'''
	Save the ExB drift velocity in SM coords.
	
	'''
	
	#get the output file name and check if it exists
	outdir = _VExB.datapath.format(sc)
	if not os.path.isdir(outdir):
		os.system('mkdir -pv '+outdir)
	fname = outdir + '{:08d}.bin'.format(Date)
	if os.path.isfile(fname) and not Overwrite:
		print('File Exists')
		return
	
	#read in the data
	try:
		data = GetData(Date,sc=sc,Verbose=False)
	except:
		print('Resaving Field Data')
		ConvertEFieldDay(Date,sc)
		data = GetData(Date,sc=sc,Verbose=False)
		
	#calculate the velocities
	vel = GetVelocity(sc,'SM')
	date0 = TT.MinusDay(Date)
	date1 = TT.PlusDay(Date)
	use = np.where((vel.Date >= date0) & (vel.Date <= date1))[0]
	
	#create interpolation objects
	fvx = interp1d(vel.utc,vel.Vx,bounds_error=False,fill_value=np.nan)
	fvy = interp1d(vel.utc,vel.Vy,bounds_error=False,fill_value=np.nan)
	fvz = interp1d(vel.utc,vel.Vz,bounds_error=False,fill_value=np.nan)

	#create the output array
	out = np.recarray(data.size,dtype=_VExB.dtype)
	
	#copy some fields across
	out.Date = data.Date
	out.ut = data.ut
	out.utc = data.utc
	out.Bx = data.BxSM
	out.By = data.BySM
	out.Bz = data.BzSM
	out.Ex = data.ExSM
	out.Ey = data.EySM
	out.Ez = data.EzSM
	out.x = data.Xsm
	out.y = data.Ysm
	out.z = data.Zsm
	
	#get the spacecraft velocity!
	out.Vx = fvx(out.utc)
	out.Vy = fvy(out.utc)
	out.Vz = fvz(out.utc)
	
	#get the kp index and a function which describes it with utc
	kp = kpindex.GetKp([date0,date1])
	utc0 = TT.ContUT(kp.Date,kp.ut0)
	utc1 = TT.ContUT(kp.Date,kp.ut1)
	utc = 0.5*(utc0 + utc1)
	fkp = interp1d(utc,kp.Kp,bounds_error=False,fill_value=np.nan)
	k = fkp(out.utc)
	
	#get the electric field data
	odata = omni.GetOMNI(Date//10000)
	#bad = np.where(np.isfinite(odata.E) == False)[0]
	good = np.where(np.isfinite(odata.E))[0]
	E = odata.E
	#E = odata.E.clip(min=0.1)
	#E[bad] = 0.1
	outc = TT.ContUT(odata.Date,odata.ut)
	fE = interp1d(outc[good],E[good],bounds_error=False,fill_value=np.nan)
	Esw = fE(out.utc).clip(min=0.1)
	
	
	#get the model electric field
	out.mEx,out.mEy,out.mEz = vsmodel.ModelECart(out.x,out.y,Kp=k,Esw=Esw)
	
	#now calculate the ExB drift using model E
	out.mVxExB,out.mVyExB,out.mVzExB = VExB(out.mEx*1e-3,out.mEy*1e-3,out.mEz*1e-3,out.Bx*1e-9,out.By*1e-9,out.Bz*1e-9)
	
	#and using the E data
	out.VxExB,out.VyExB,out.VzExB = VExB(out.Ex*1e-3,out.Ey*1e-3,out.Ez*1e-3,out.Bx*1e-9,out.By*1e-9,out.Bz*1e-9)
	
	#save the file
	print('Saving: {:s}'.format(fname))
	RT.SaveRecarray(out,fname)


def SaveAllData(sc,Overwrite=False):
	'''
	Save all ExB drifts for a given spacecraft
	
	'''
	#get the dates
	dates = DataAvailability(sc)
	
	#loop through each one
	for i in range(0,dates.size):
		print('Saving date {0} of {1}'.format(i+1,dates.size))
		SaveData(dates[i],sc,Overwrite)
