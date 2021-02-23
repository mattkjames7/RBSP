import numpy as np
from .ReadCDF import ReadCDF
from .DownloadData import DownloadData
from .ReadIndex import ReadIndex
from .RebuildDataIndex import RebuildDataIndex
import os
from . import _EMFISIS

def _CheckFile(Date,fname,sc,L,Prod):
	'''
	This will check an individual file.
	
	Inputs
	======
	Date: list 
		Integer date(s) , format yyyymmdd.
	fname : str
		File name with full path
	sc: str
		'a' or 'b'
	L: str
		Data level, see below
	Prod: str
		Data product
		
	Returns
	=======
	exists : bool
		True if the file exists
	loads : bool
		True if the file loads successfully
	
	'''
	
	#firstly, check the file is there
	exists = os.path.isfile(fname)
	
	#is if is then chekc it loads
	loads = False
	if exists:
		try:
			data,cdf = ReadCDF(Date,sc,L,Prod)
			if not data is None:
				loads = True
		except:
			pass
			
	return exists,loads


def CheckData(sc='a',L='l4',Prod=None,Repair=False):
	'''
	This will loop through all of the stored datafiles and check each 
	one loads - optionally it will also redownload broken CDFs.
	
	Inputs
	======
	sc: str
		'a' or 'b'
	L: str
		Data level, see below
	Prod: str
		Data product
	Repair : bool
		If True, then broken CDF files will be redownloaded.
					
	Available Data Products
	=======================
	Level 		Prod		Description
	'l4' 		None		densities
	'l3'	 	'1sec-***'	1-second resolution magnetic fields
	'l3'	 	'4sec-***'	4-second resolution magnetic fields
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
	
	#start by rebuilding the data index to find any files which may be 
	#missing from it
	print('Rebuilding data index')
	RebuildDataIndex(sc,L,Prod)
	
	#read the index to get the list of files
	print('Reading data index')
	idx = ReadIndex(sc,L,Prod)
	
	#sort by date
	srt = np.argsort(idx.Date)
	idx = idx[srt]

	#get the name of the path we are searching
	if L == 'l4':
		datapath = _EMFISIS.datapathl4.format(L,sc)
	else:
		datapath = _EMFISIS.datapath.format(L,sc,Prod)

	#loop through each one
	n = idx.size
	exists = np.zeros(n,dtype='bool')
	loads = np.zeros(n,dtype='bool')
	ne = 0	#number of existing files
	nl = 0	#number of loadable files
	nm = 0	#number of missing files
	nb = 0	#number of broken files
	for i in range(0,n):
		print('\rChecking {:04d} of {:04d} - Exists: {:04d} - Missing {:04d} - Loadable: {:04d} - Broken {:04d}'.format(i+1,n,ne,nm,nl,nb),end='')
		#check the file
		exists[i],loads[i] = _CheckFile(idx.Date[i],datapath + idx.FileName[i],sc,L,Prod)
		
		#update the counts
		if exists[i]:
			ne += 1
			if loads[i]:
				nl += 1
			else:
				nb += 1
		else:
			nm += 1
		print('\rChecking {:04d} of {:04d} - Exists: {:04d} - Missing {:04d} - Loadable: {:04d} - Broken {:04d}'.format(i+1,n,ne,nm,nl,nb),end='')
	print()
	
	#deal with missing first
	nd = 0
	if nm > 0:
		missing = np.where(exists == False)[0]
		midx = idx[missing]
		
		for i in range(0,nm):
			print('Downloading missing file {:04d} of {:04d}'.format(i+1,nm))
			DownloadData(sc,L,Prod,midx.Date[i],Overwrite=True)
			e,l = _CheckFile(midx.Date[i],datapath + midx.FileName[i],sc,L,Prod)
			
			if e and l:
				nd += 1
	
	#now fix the broken ones
	nf = 0
	if nb > 0:
		broken = np.where(loads == False)[0]
		bidx = idx[broken]
		
		for i in range(0,nb):
			print('Redownloading broken file {:04d} of {:04d}'.format(i+1,nb))
			DownloadData(sc,L,Prod,bidx.Date[i],Overwrite=True)
			e,l = _CheckFile(bidx.Date[i],datapath + bidx.FileName[i],sc,L,Prod)
			
			if e and l:
				nf += 1			

	
	print('Started with')
	print('============')
	print('{:04d} Dates'.format(n))
	print('{:04d} Existing files'.format(ne))
	print('{:04d} Loadable files'.format(nl))
	print('{:04d} Missing files'.format(nm))
	print('{:04d} Broken files'.format(nb))
	print()
	print('Ended with')
	print('============')
	print('{:04d} Downloaded missing files'.format(nd))
	print('{:04d} Replaced broken files'.format(nf))
	print('{:04d} Missing files'.format(nm-nd))
	print('{:04d} Broken files'.format(nb-nf))	
