import numpy as np
import PyGeopack as gp
import DateTimeTools as TT


def ModelField(x,y,z,Date,ut):
	mx,my,mz = gp.ModelField(x,y,z,Date,ut,Model='T96',CoordIn='GSE',CoordOut='GSE')
	
	inter = 11
	low = 90
	mx = TT.lsfilter(mx,inter,low,inter,True) 
	my = TT.lsfilter(my,inter,low,inter,True) 
	mz = TT.lsfilter(mz,inter,low,inter,True) 	
	
	
	return mx,my,mz
