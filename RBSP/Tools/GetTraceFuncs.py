import numpy as np
from scipy.interpolate import interp1d
from .. import Globals
from ..Pos.ReadFieldTraces import ReadAllFieldTraces

def GetTraceFuncs(sc='a'):
	
	if not sc in list(Globals.TraceFuncs.keys()):
		#create a dictionary
		TF = {}
		
		#load the traces
		traces = ReadAllFieldTraces(sc)
		
		#list the fields to create interpolation objects for
		fields = ['MlatN','MlatS','GlatN','GlatS','MlonN','MlonS','GlonN','GlonS',
		'MltN','MltS','GltN','GltS','MltE','Lshell','FlLen','Rmax','Rnorm',
		'Tilt','Xgse','Ygse','Zgse','Xgsm','Ygsm','Zgsm','Xsm','Ysm','Zsm']	
		
		for f in fields:
			print('Creating interpolation object for {:s}'.format(f))
			TF[f] = interp1d(traces.utc,traces[f],bounds_error=False,fill_value=np.nan)
			
		Globals.TraceFuncs[sc] = TF
			
	return Globals.TraceFuncs[sc]
