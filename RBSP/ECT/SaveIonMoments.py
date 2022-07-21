import numpy as np
from . import _ECT
from .ReadHOPEOmni import ReadHOPEOmni
from .ReadCDF import ReadCDF
from ..EFW.GetPotential import GetPotential
from ..VExB.ReadData import ReadData
from .. import Globals
import os
import RecarrayTools as RT
import DateTimeTools as TT
from ..Tools.RelEnergy import RelEnergy
from ..Tools.IntegrateSpectra import IntegrateSpectra
from .. import EMFISIS
from .. import EFW
from scipy.special import erfinv
from scipy.interpolate import interp1d
from .CalculateIonMoments import CalculateIonMoments


def SaveIonMoments(Date,sc,Overwrite=False,MaxE=0.02):	
	'''
	Save some new moments for the HOPE data.
	
	'''

	#create the output directory
	outdir = Globals.DataPath + 'Moments/Ions/{:s}/'.format(sc)
	if not os.path.isdir(outdir):
		os.system('mkdir -pv '+outdir)
	
	fname = outdir + '{:08d}.bin'.format(Date)
	if os.path.isfile(fname) and not Overwrite:
		print('File exists')
		return
	
	out = CalculateIonMoments(Date,sc,MaxE)
	
	print('Saving')
	RT.SaveRecarray(out,fname)
