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
	dtype=[('Date','int32'),('ut','float32'),('utc','float64'),('MlatN','float32'),('MlatS','float32'),
			('GlatN','float32'),('GlatS','float32'),('MlonN','float32'),('MlonS','float32'),
			('GlonN','float32'),('GlonS','float32'),('MltN','float32'),('MltS','float32'),
			('GltN','float32'),('GltS','float32'),('MltE','float32'),('Lshell','float32'),
			('FlLen','float32'),('Rmax','float32'),('Rnorm','float32'),('Tilt','float32'),
			('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
	
	if use.size == 0:
		print('No position data for rbsp{:s} on {:d}'.format(sc,Date))
		return np.recarray(0,dtype=dtype)
	pos = pos[use]
	n = pos.size
	out = np.recarray(n,dtype=dtype)
	print(pos[-1])
	#do the tracing
	T = gp.TraceField(pos.Xsm,pos.Ysm,pos.Zsm,pos.Date,pos.ut,Model=Model,CoordIn='SM',Verbose=Verbose)
	print(T.MlatN)
	#insert data into output array
	out.Date = pos.Date
	out.ut = pos.ut
	out.utc = pos.utc
	out.MlatN = T.MlatN
	out.MlatS = T.MlatS
	out.GlatN = T.GlatN
	out.GlatS = T.GlatS
	out.MlonN = T.MlonN
	out.MlonS = T.MlonS
	out.GlonN = T.GlonN
	out.GlonS = T.GlonS
	out.MltN = T.MltN
	out.MltS = T.MltS
	out.GltN = T.GltN
	out.GltS = T.GltS
	out.MltE = T.MltE
	out.Lshell = T.Lshell
	out.FlLen = T.FlLen
	out.Xgse = pos.Xgse
	out.Ygse = pos.Ygse
	out.Zgse = pos.Zgse
	out.Xgsm = pos.Xgsm
	out.Ygsm = pos.Ygsm
	out.Zgsm = pos.Zgsm
	out.Xsm = pos.Xsm
	out.Ysm = pos.Ysm
	out.Zsm = pos.Zsm
	out.Tilt = gp.GetDipoleTilt(out.Date,out.ut)
	
	Rs = np.sqrt(pos.Xsm**2 + pos.Ysm**2 + pos.Zsm**2)
	Rt = np.sqrt(T.x**2 + T.y**2 + T.z**2)
	
	# for i in range(0,n):
		# if np.isfinite(T.MltE[i]):
			# xsm,ysm,zsm = gp.GSMtoSM(T.x[i],T.y[i],T.z[i],out.Date[i],out.ut[i])
			# if np.nanmin(T.x[i]) < -10.0:
				# R = np.sqrt(T.x[i]**2 + T.y[i]**2 + T.z[i]**2)
			# else:
				# R = np.sqrt(xsm**2 + ysm**2)
			# u = np.where(R == np.nanmax(R))[0][0]
			# out.Rmax[i] = R[u]
		# else:
			# out.Rmax[i] = np.nan
	
#	out.Rmax = np.nanmax(Rt,axis=1)
	out.Rmax = out.Lshell
	out.Rnorm = Rs/out.Rmax
	
	return out
