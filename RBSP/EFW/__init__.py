'''
EFW: Electric Field and Waves
Wygant et al. 2013, doi:10.1007/s11214-013-0013-7

Data Products
=============
Electric Field
Wave spectra
'''

from .DownloadData import DownloadData
from .ReadCDF import ReadCDF
from . import _EFW
from .ReadIndex import ReadIndex
from .URL import URL
from .DataAvailability import DataAvailability
from .RebuildDataIndex import RebuildDataIndex
from .DeleteDate import DeleteDate
