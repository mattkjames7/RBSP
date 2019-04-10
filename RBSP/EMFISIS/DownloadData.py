from .. import Globals
import numpy as np
import DateTimeTools as TT
from ._GetCDFURL import _GetCDFURL
import os


def DownloadData(sc='a',L=4,StartDate=20120830,EndDate=20190408,Overwrite=False):
	'''
	Downloads EMFISIS data.
	
	'''
	#populate the list of dates to trace first
	date = StartDate
	dates = []
	while date <= EndDate:
		dates.append(date)
		date = TT.PlusDay(date)
	n = np.size(dates)
	dates = np.array(dates)
	
	#create output path if it doesn't exist
	outpath = Globals.DataPath+'EMFISIS/L{:d}/{:s}/'.format(L,sc)
	if not os.path.isdir(outpath):
		os.system('mkdir -pv '+outpath)
		
	
	#list the files within outpath
	files = os.listdir(outpath)
	files = np.array(files)
	files.sort()
	nf = np.size(files)
	
	#check if any of the dates already exist
	if not Overwrite:
		exists = np.zeros(n,dtype='bool')
		date_str = np.array(dates).astype('U8')
		p = 0
		for i in range(0,nf):
			for j in range(p,n):
				if date_str[j] in files[i]:
					p = j
					exists[j] = True
					
		use = np.where(exists == False)[0]
		dates = dates[use]
		n = dates.size
		
	#loop through each remaining date and start downloading
	for i in range(0,n):
		print('Date {0} of {1}'.format(i+1,n))
		urls,fnames = _GetCDFURL(dates[i],sc,L)
		nu = np.size(urls)
		
		for j in range(0,nu):
			print('Downloading file {0} of {1}'.format(j+1,nu))
			os.system('wget '+urls[j]+' -O '+outpath+fnames[j])
