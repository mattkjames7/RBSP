import numpy as np
from .. import Globals

#this just stores a few variables for this particular instrument

#data path and index file name:
idxfname = Globals.DataPath + 'EFW/{:s}.{:s}.dat'
datapath = Globals.DataPath + 'EFW/{:s}/{:s}/'

#file version format
vfmt = 'v\d\d'


#potential dtype
pdtype = [	('Date','int32'),		
			('ut','float32'),
			('utc','float64'),
			('Vsc','float32'),
			('VscFlag','int8'),
			('ne','float32'),
			('neFlag','int8')]
