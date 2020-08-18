from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData
from . import _EMFISIS
from .URL import URL


def DownloadData(sc='a',L=4,Prod=None,Date=[20120830,20200101],Overwrite=False,Verbose=True):
	'''
	Downloads EMFISIS data.

	Inputs
	======
	Date: list 
		Integer date(s) , format yyyymmdd.
	sc: str
		'a' or 'b'
	L: str
		Data level, see below
	Prod: str
		Data product
			
	Available Data Products
	=======================
	Level 		Prod		Description
	'l4' 		None		densities
	'l3'	 	'1sec-***'	1-second resolution magnetic fields
	'l3'	 	'1sec-***'	4-second resolution magnetic fields
	'l3'	 	'hires-***'	High resolution magnetic fields
	'l2'		'HFR-spectra'
	'l2'		'HFR-spectra-merged'
	'l2'		'HFR-spectra-burst'
	'l2'		'HFR-waveform'
	'l2'		'WFR-spectral-matrix'
	'l2'		'WFR-spectral-matrix-burst'
	'l2'		'WFR-spectral-matrix-burst-diagonal'
	'l2'		'WFR-spectral-matrix-diagonal-merged'
	'l2'		'WFR-spectral-matrix-diagonal'
	'l2'		'WFR-waveform'
	'l2'		'WFR-waveform-continuous-burst'
	There may be others - they should download given the appropriate Prod string
			
	*** can be either 'gei','geo','gse','gsm' or 'sm'
	
	'''
	
	
	if L == 'l4':
		fc = None
		idxfname = _EMFISIS.idxfnamel4.format(L,sc)
		datapath = _EMFISIS.datapathl4.format(L,sc)
	else:
		fc = Prod + '_emfisis'
		idxfname = _EMFISIS.idxfname.format(L,sc,Prod)
		datapath = _EMFISIS.datapath.format(L,sc,Prod)
	
	URLF = URL(sc,L)
	_DownloadData(URLF,idxfname,datapath,Date,_EMFISIS.vfmt,fc,Overwrite,Verbose)


	# #populate the list of dates to trace first
	# date = StartDate
	# dates = []
	# while date <= EndDate:
		# dates.append(date)
		# date = TT.PlusDay(date)
	# n = np.size(dates)
	# dates = np.array(dates)
	
	# #create output path if it doesn't exist
	# outpath = Globals.DataPath+'EMFISIS/L{:d}/{:s}/'.format(L,sc)
	# if not os.path.isdir(outpath):
		# os.system('mkdir -pv '+outpath)
		
	
	# #list the files within outpath
	# files = os.listdir(outpath)
	# files = np.array(files)
	# files.sort()
	# nf = np.size(files)
	
	# #check if any of the dates already exist
	# if not Overwrite:
		# exists = np.zeros(n,dtype='bool')
		# date_str = np.array(dates).astype('U8')
		# p = 0
		# for i in range(0,nf):
			# for j in range(p,n):
				# if date_str[j] in files[i]:
					# p = j
					# exists[j] = True
					
		# use = np.where(exists == False)[0]
		# dates = dates[use]
		# n = dates.size
		
	# #loop through each remaining date and start downloading
	# for i in range(0,n):
		# print('Date {0} of {1}'.format(i+1,n))
		# urls,fnames = _GetCDFURL(dates[i],sc,L)
		# nu = np.size(urls)
		
		# for j in range(0,nu):
			# print('Downloading file {0} of {1}'.format(j+1,nu))
			# os.system('wget '+urls[j]+' -O '+outpath+fnames[j])
