from ... import Globals
import numpy as np
import DateTimeTools as TT
from ._GetCDFURL import _GetCDFURL
import os
import re
from ._ReadDataIndex import _ReadDataIndex
from ._UpdateDataIndex import _UpdateDataIndex
import RecarrayTools as RT
from ._ExtractDateVersion import _ExtractDateVersion
from ._ReduceDownloadList import _ReduceDownloadList
from ..ListDates import ListDates

def _DownloadData(url0,fname,outpath,Date=[20170101,20200101],vfmt=['v','.'],Overwrite=False,Progress=False):
	'''
	Downloads Arase data

	Inputs
	======
	url0 : string
		Base URL of the data repository
	fname : string
		Full path and file name of index file
	outpath : string
		Path to download the data to
	Date : int
		Date to download data for in format yyyymmdd
		If single date - only data from that one day will be fetched
		If 2-element array - dates from Date[0] to Date[1] will be downloaded
		If > 2 elements - this is treated as a specific list of dates to download
	vfmt : list
		2 element list containing characters which split the version
		numbers, by default	it is ['v','_']
	Overwrite : bool
		If True then existing files will be overwritten
	'''
	#populate the list of dates to download
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
	
	#populate the list of dates to trace first
	yymm = dates//100
	yymm = np.unique(yymm)
	Years = yymm//100
	Months = yymm % 100
	n = yymm.size

	
	#create output path if it doesn't exist
	if not os.path.isdir(outpath):
		os.system('mkdir -pv '+outpath)
		
	#loop through each remaining date and start downloading
	for i in range(0,n):
		print('Year {0}'.format(Years[i]))
		urls,fnames = _GetCDFURL(Years[i],Months[i],url0)

		
		
		nu = np.size(urls)
		
		if nu > 0:
			idx = _ReadDataIndex(fname)
			new_idx = np.recarray(nu,dtype=idx.dtype)
			new_idx.Date[:] = -1

			fDate,Ver = _ExtractDateVersion(fnames,vfmt)
			urls,fnames,fDate,Ver = _ReduceDownloadList(urls,fnames,fDate,Ver,idx,dates,Overwrite)
			nu = np.size(urls)

			p = 0
			for j in range(0,nu):
				print('Downloading file {0} of {1} ({2})'.format(j+1,nu,fnames[j]))

				if Progress:
					os.system('wget '+urls[j]+' -O '+outpath+fnames[j])
				else:
					os.system('wget --no-verbose '+urls[j]+' -O '+outpath+fnames[j])

				new_idx.Date[p] = fDate[j]
				new_idx.FileName[p] = fnames[j]
				new_idx.Version[p] = Ver[j]
				p+=1
					
			new_idx = new_idx[:p]
			
			
			#check for duplicates within old index
			usen = np.ones(p,dtype='bool')
			useo = np.ones(idx.size,dtype='bool')
				
			for j in range(0,p):
				match = np.where(idx.Date == new_idx.Date[j])[0]
				if match.size > 0:
					if idx.Version[match[0]] > new_idx.Version[j]:
						#old one is newer (unlikely)
						usen[j] = False
					else:
						#new one is newer
						useo[match[0]] = False

			usen = np.where(usen)[0]
			new_idx = new_idx[usen]
			useo = np.where(useo)[0]
			idx = idx[useo]					
			
			#join indices together and update file
			idx_out = RT.JoinRecarray(idx,new_idx)
			srt = np.argsort(idx_out.Date)
			idx_out = idx_out[srt]
			_UpdateDataIndex(idx_out,fname)
			
			
