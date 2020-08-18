import numpy as np
from .. import Globals

#this just stores a few variables for this particular instrument

#data path and index file name:
idxfnamel4 = Globals.DataPath + 'EMFISIS/{:s}.{:s}.dat'
datapathl4 = Globals.DataPath + 'EMFISIS/{:s}/{:s}/'
idxfname = Globals.DataPath + 'EMFISIS/{:s}.{:s}.{:s}.dat'
datapath = Globals.DataPath + 'EMFISIS/{:s}/{:s}/{:s}/'

#file version format
vfmt = 'v\d.\d.\d+'
