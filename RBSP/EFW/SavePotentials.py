import numpy as np
from .ReadCDF import ReadCDF
import DateTimeTools as TT
from .. import EMFISIS
from scipy.interpolate import interp1d
from . import _EFW
import os
import RecarrayTools as RT
from .. import Globals


params = {	'a'	: (3513.1800108505913,  31.834661688271133,  2.4391288968749882,  0.20718165654912396),
			'b' : (6427.5386984329,  176.00272766473574,  4.773851664050161,  0.7559620237662504)}

def _DensityFunction(v,A1,A2,b,c):
	
	ne = A1*np.exp(b*v) + A2*np.exp(c*v)
	
	return ne
	
def _SavePotential(Date,sc):
	'''
	Save the spacecraft potentials and equivalent electron densities.
	
	Bad densities will be replaced with those from emfisis and if there 
	are bad potentials, then they will be replaced with potentials 
	calculated from EMFISIS electron densities.
	
	
	'''
	
	#get the parameters for the conversion
	A1,A2,b,c = params[sc]
	
	#create a spline for the ne ->  Vsc conversion
	Vsc = np.linspace(-6.0,0.0,100)
	ne = _DensityFunction(Vsc,A1,A2,b,c)
	fVsc = interp1d(ne,Vsc,fill_value=(Vsc[0],Vsc[-1]),bounds_error=False)
	
	try:
		#read in the data from EFW
		efw,_ = ReadCDF(Date,sc,'l3')
		
		#create the output array
		n = efw['epoch'].size
		out = np.recarray(n,dtype=_EFW.pdtype)
		
		#get the dates/times etc
		out.Date,out.ut = TT.CDFEpochtoDate(efw['epoch'])
		out.utc = TT.ContUT(out.Date,out.ut)
		
		#copy the efw parameters across
		out.Vsc = efw['Vavg']
		out.VscFlag = 0.0
		out.ne = efw['density']
		out.neFlag = 0.0
	except:
		#create an empty array
		ut = np.arange(0.0,86400.0,11.0)
		n = ut.size
		out = np.recarray(n,dtype=_EFW.pdtype)
		
		out.Date[:] = Date
		out.ut = ut
		out.utc = TT.ContUT(out.Date,out.ut)
		out.VscFlag = 0.0
		out.neFlag = 0.0

		out.Vsc = np.nan
		out.ne = np.nan
		
	#flag the bad data
	badv = np.where((np.isfinite(out.Vsc) == False) | (out.Vsc < -10000.0) | (out.Vsc > 10000.0))[0]
	badn = np.where((np.isfinite(out.ne) == False) | (out.ne < 10.0) | (out.ne > 3000.0))[0]
	out.Vsc[badv] = np.nan
	out.ne[badn] = np.nan
	out.VscFlag[badv] = 1
	out.neFlag[badn] = 1
	
	try:
		#read in the data from EMFISIS
		emf,_ = EMFISIS.ReadCDF(Date,sc,'l4')
		
		#get emfisis dates and times
		d,t = TT.CDFEpochtoDate(emf['Epoch'])
		utc = TT.ContUT(d,t)	
		ne = emf['density']
		
		#create an interpolation object
		use = np.where((ne > 0.0) & np.isfinite(ne))[0]
		femf = interp1d(utc[use],ne[use],bounds_error=False,fill_value=np.nan)
		
		#interpolate bad densities
		out.ne[badn] = femf(out.utc[badn])
		
		
	except:
		print('EMFISIS fail')
		pass
	
	#fill in the bad potentials
	out.Vsc[badv] = fVsc(out.utc[badv])
	
	#save the file
	outdir = Globals.DataPath + 'Potential/{:s}/'.format(sc)
	if not os.path.isdir(outdir):
		os.system('mkdir -pv '+outdir)
	fname = outdir + '{:08d}.bin'.format(Date)
	RT.SaveRecarray(out,fname)
	
	
	
def SavePotentials(sc):
	'''
	
	
	'''
	if sc == 'a':
		dates = TT.ListDates(20120915,20190629)
	else:
		dates = TT.ListDates(20120915,20190830)
		
	for i in range(0,dates.size):
		print('\rSaving Date {0} of {1}'.format(i+1,dates.size),end='')
		
		_SavePotential(dates[i],sc)
		
	print()
	
	
