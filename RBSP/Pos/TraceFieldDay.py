from .. import Globals 
import PyGeopack as gp
import numpy as np
from .GetPos import GetPos

def TraceFieldFootprintsDay(Date,sc='a',Model='T96',Verbose=True):
	'''
	Traces the Tsyganenko model field looking for the magnetic 
	footprints of RBSP for one day at 1-minute resolution.
	
	'''
	#Read the position data in first of all
	pos = GetPos(sc)
	
	#find the appropriate date
	use = np.where(pos.Date == Date)[0]

	#define the dtype
	dtype=[('Date','int32'),('ut','float32'),('MlatN','float32'),('MlatS','float32'),
			('GlatN','float32'),('GlatS','float32'),('MlonN','float32'),('MlonS','float32'),
			('GlonN','float32'),('GlonS','float32'),('MltN','float32'),('MltS','float32'),
			('GltN','float32'),('GltS','float32'),('MltE','float32'),('Lshell','float32'),
			('FlLen','float32'),('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32'),
			('Bx','float32'),('By','float32'),('Bz','float32')]
	
	if use.size == 0:
		print('No position data for rbsp{:s} on {:d}'.format(sc,Date))
		return np.recarray(0,dtype=dtype)
	pos = pos[use]
	n = pos.size
	out = np.recarray(n,dtype=dtype)
	
	#do the tracing
	T = gp.TraceField(pos.Xsm,pos.Ysm,pos.Zsm,pos.Date,pos.ut,Model=Model,CoordIn='SM',Verbose=Verbose)
	
	#insert data into output array
	
	return T
	
