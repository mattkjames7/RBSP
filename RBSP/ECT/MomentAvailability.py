import numpy as np
from .. import Globals
import os
from ..Tools.ListFiles import ListFiles

def MomentAvailability(sc='a'):
	'''
	Get the availability of ion moments.
	
	'''
	
	#the path
	path = Globals.DataPath + 'Moments/Ions/{:s}/'.format(sc)

	#list the files in the folder
	_,files = ListFiles(path,ReturnNames=True)
	
	#extract dates
	dates = np.array([np.int32(f[:8]) for f in files],dtype='int32')
	
	#sort
	srt = np.argsort(dates)
	
	return dates[srt]
