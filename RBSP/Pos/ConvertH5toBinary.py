import numpy as np
from .ReadH5 import ReadH5
import RecarrayTools as RT
import os
from .. import Globals
import DateTimeTools as TT
from ._ReadDataIndex import _ReadDataIndex
from scipy.interpolate import InterpolatedUnivariateSpline

def _InterpParam(ut,x):
	'''
	Interpolate a parameter such that it is sampled at a 1 minute resolution
	'''
	newt = np.arange(1440.0)/60.0

	use = np.where(np.isfinite(x))[0]
	f = InterpolatedUnivariateSpline(ut[use],x[use])
	return f(newt)

def _ConvertTimes(isotime):
	'''
	Convert the time of the format 'yyyy-mm-ddThr:mn:scZ'
	'''
	n = np.size(isotime)
	date = np.zeros(n,dtype='int32')
	ut = np.zeros(n,dtype='float32')
	
	for i in range(0,n):
		#there are some dodgy dates for some reason so:
		if len(isotime[i]) == 20:
			#good time
			yy = np.int32(isotime[i][:4])
			mm = np.int32(isotime[i][5:7])
			dd = np.int32(isotime[i][8:10])
		
			hr = np.float32(isotime[i][11:13])
			mn = np.float32(isotime[i][14:16])
			dy = np.float32(isotime[i][17:19])
		
			date[i] = yy*10000 + mm*100 + dd
			ut[i] = hr + mn/60.0 + dy/3600.0
		else:
			date[i] = 0
			ut[i] = -1.0
			
	return date,ut
	

def _ConvertH5File(Date,sc,Overwrite=False):
	'''
	Converts an individual MagEph file to a simple binary file
	'''
	#check the output directory exists
	fname = Globals.DataPath + 'Pos/{:s}/'.format(sc)
	if not os.path.isdir(fname):
		os.system('mkdir -pv '+fname)
	fname += '{:08d}.bin'.format(Date)

	if os.path.isfile(fname) and not Overwrite:
		return

	#read the h5 data
	data = ReadH5(Date,sc)
	if data is None:
		return
		
	#define the dtype
	dtype = [('Date','int32'),('ut','float32'),('utc','float64'),
			('Xgeo','float32'),('Ygeo','float32'),('Zgeo','float32'),
			('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
	
	
	
	#work out the time since 19500101
	dt = np.float64(TT.DateDifference(19500101,Date))*np.float64(24.0)
	
	#turn the string date/time into the right format
	date,ut = _ConvertTimes(np.array(data['IsoTime']))
	
	#find out which indices belong to the current day
	use = np.where(date == Date)[0]
	n = use.size
	out = np.recarray(1440,dtype=dtype)
	
	#copy the fields across
	out.Date = Date
	out.ut = np.arange(1440)/60.0
	out.utc = np.float64(out.ut) + np.float64(dt)
	
	out.Xgeo = _InterpParam(ut[use],data['Rgeo'][use,0])
	out.Ygeo = _InterpParam(ut[use],data['Rgeo'][use,1])
	out.Zgeo = _InterpParam(ut[use],data['Rgeo'][use,2])
	out.Xgse = _InterpParam(ut[use],data['Rgse'][use,0])
	out.Ygse = _InterpParam(ut[use],data['Rgse'][use,1])
	out.Zgse = _InterpParam(ut[use],data['Rgse'][use,2])
	out.Xgsm = _InterpParam(ut[use],data['Rgsm'][use,0])
	out.Ygsm = _InterpParam(ut[use],data['Rgsm'][use,1])
	out.Zgsm = _InterpParam(ut[use],data['Rgsm'][use,2])
	out.Xsm = _InterpParam(ut[use],data['Rsm'][use,0])
	out.Ysm = _InterpParam(ut[use],data['Rsm'][use,1])
	out.Zsm = _InterpParam(ut[use],data['Rsm'][use,2])
	
	#save the output file
	RT.SaveRecarray(out,fname)
	
def _CombineBinaries(sc):
	'''
	Combine the binary files into a single file
	
	'''
	#read the data index to find the available dates
	idx = _ReadDataIndex(sc)
	Dates = idx.Date
	
	ud = np.unique(Dates)
	nd = ud.size
	
	#define the directory
	fpath = Globals.DataPath + 'Pos/{:s}/'.format(sc)
	
	
	
	#loop through counting records in each date
	n = 0
	for i in range(0,nd):
		print('\rCounting file {0} of {1}'.format(i+1,nd),end='')		
		fname = fpath + '{:08d}.bin'.format(ud[i])
		f = open(fname,'rb')
		n += np.fromfile(f,dtype='int32',count=1)[0]
		f.close()
	print()
	print('Total records: {:d}'.format(n))
		
	#define the dtype
	dtype = [('Date','int32'),('ut','float32'),('utc','float64'),
			('Xgeo','float32'),('Ygeo','float32'),('Zgeo','float32'),
			('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
	out = np.recarray(n,dtype=dtype)		
	
	#loop through each date and combine data
	p = 0
	for i in range(0,nd):
		print('\rCombining file {0} of {1}'.format(i+1,nd),end='')		
		fname = fpath + '{:08d}.bin'.format(ud[i])
		tmp = RT.ReadRecarray(fname,dtype)
		out[p:p+tmp.size] = tmp
		p += tmp.size
	print()
	
	
	outfile = Globals.DataPath + 'Pos/rbsp{:s}.bin'.format(sc.lower())
	RT.SaveRecarray(out,outfile)
	print('Done')
		
def ConvertH5toBinary(sc='a',Overwrite=False):
	'''
	Converts the SPDF SSCWeb text files (scraped from their HTML output)
	to binary.
	
	Input:
		sc: Spacecraft 'a' or 'b'
		
	'''	
	#read the data index to find the available dates
	idx = _ReadDataIndex(sc)
	Dates = idx.Date
	
	ud = np.unique(Dates)
	nd = ud.size
	
	#loop through converting each date
	for i in range(0,nd):
		print('\rConverting file {0} of {1} ({2})'.format(i+1,nd,ud[i]),end='')
		_ConvertH5File(ud[i],sc,Overwrite=Overwrite)
	print()
	
	#now to combine files
	_CombineBinaries(sc)
	

def RedoUTC(sc='a'):
	'''
	I screwed up the continuous time axis - hopefully this will fix it
	'''

	#read the data index to find the available dates
	idx = _ReadDataIndex(sc)
	Dates = idx.Date
	
	ud = np.unique(Dates)
	nd = ud.size

	#define the dtype
	dtype = [('Date','int32'),('ut','float32'),('utc','float64'),
			('Xgeo','float32'),('Ygeo','float32'),('Zgeo','float32'),
			('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
		
	fpath = Globals.DataPath + 'Pos/{:s}/'.format(sc)
	
	#loop through converting each date
	dtp = 0.0
	pd = 19500101
	for i in range(0,nd):
		print('\rFixing file {0} of {1} ({2})'.format(i+1,nd,ud[i]),end='')
		fname = fpath + '{:08d}.bin'.format(ud[i])
		dt = dtp + np.float64(TT.DateDifference(pd,ud[i]))*np.float64(24.0)
		
		data = RT.ReadRecarray(fname,dtype)
		data.utc = np.float64(dt) + np.float64(data.ut)
		RT.SaveRecarray(data,fname)
		dtp = np.array(dt)
		pd = ud[i]		
	print()
	
	#now to combine files
	_CombineBinaries(sc)



	
