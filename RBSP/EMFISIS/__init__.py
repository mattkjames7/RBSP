'''
EMFISIS: Electric and Magnetic Field Instrument Suite and Integrated Science
Kletzing et al. 2013, doi:10.1007/s11214-013-9993-6

Data products
=============
Magnetic Field
High frequency waves
Electron densities (using UHR)

'''


from .DownloadData import DownloadData
from . import _EMFISIS
from .ReadIndex import ReadIndex
from .URL import URL
from .RebuildDataIndex import RebuildDataIndex
from .DeleteDate import DeleteDate
from .ReadCDF import ReadCDF
from .InterpObj import InterpObj
from .DataAvailability import DataAvailability
from .CheckData import CheckData
from .ReadElectronDensity import ReadElectronDensity
from .GetMag import GetMag
