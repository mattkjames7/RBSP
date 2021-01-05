import RecarrayTools as RT
from .. import Globals
from .TraceFieldDay import TraceFieldDay
import DateTimeTools as TT
from .GetPos import GetPos
import os
import numpy as np
from ._ReadDataIndex import _ReadDataIndex

def SaveFieldTraces(sc='a',Model='T96',StartDate=20120830,EndDate=20191017,Verbose=True,Overwrite=False,Combine=False):
	'''
	Saves the Tsyganenko field trace footprints for RBSP within a range 
	of dates.
	
	'''
	#populate the list of dates to trace first
	idx = _ReadDataIndex(sc)
	dates = np.unique(idx.Date)
	use = np.where((dates >= StartDate) & (dates <= EndDate))[0]
	dates = dates[use]
	n = np.size(dates)
	
	#now to load the position data
	pos = GetPos(sc)

	#set the output path
	outpath = Globals.DataPath + 'Traces/{:s}/{:s}/'.format(Model,sc)
	if not os.path.isdir(outpath):
		os.system('mkdir -pv '+outpath)
	
	#loop throught the dates doing the traces
	for i in range(0,n):
		fname = outpath + '{:08d}.bin'.format(dates[i])
		if Overwrite or (not os.path.isfile(fname)):
			print('Tracing date {:8d} ({:d} of {:d})'.format(dates[i],i+1,n))
			T = TraceFieldDay(dates[i],sc,Model,Verbose)
			RT.SaveRecarray(T,fname)
		else:
			print('File {:s} exists'.format(fname))

	if Combine:
		#combine files
		dtype=[('Date','int32'),('ut','float32'),('utc','float64'),('MlatN','float32'),('MlatS','float32'),
				('GlatN','float32'),('GlatS','float32'),('MlonN','float32'),('MlonS','float32'),
				('GlonN','float32'),('GlonS','float32'),('MltN','float32'),('MltS','float32'),
				('GltN','float32'),('GltS','float32'),('MltE','float32'),('Lshell','float32'),
				('FlLen','float32'),('Rmax','float32'),('Rnorm','float32'),('Tilt','float32'),
				('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
				('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
				('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
		

		nr = 0
		for i in range(0,n):
			f = open(outpath+'{:08d}.bin'.format(dates[i]),'rb')
			nr += np.fromfile(f,dtype='int32',count=1)[0]
			f.close()
		
		out = np.recarray(nr,dtype=dtype)
		p = 0
		for i in range(0,n):
			print('Combining file {0} of {1}'.format(i+1,n))
			fname = outpath + '{:08d}.bin'.format(dates[i])
			tmp = RT.ReadRecarray(fname,dtype)
			out[p:p+tmp.size] = tmp
			p += tmp.size
		
		outfile = Globals.DataPath + 'Traces/{:s}-{:s}.bin'.format(Model,sc)
		RT.SaveRecarray(out,outfile)
