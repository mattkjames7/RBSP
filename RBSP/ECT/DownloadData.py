from .. import Globals
import numpy as np
import DateTimeTools as TT
from ._GetCDFURL import _GetCDFURL
import os
import re
from ._ReadDataIndex import _ReadDataIndex
from ._UpdateDataIndex import _UpdateDataIndex
import RecarrayTools as RT

def DownloadData(sc='a',Inst='hope',L='l3.moments',StartYear=2012,EndYear=2019,Overwrite=False):
	'''
	Downloads EFW data.

		Year: integer year.
		sc: 'a' or 'b'
		Inst: 'hope', 'mageis' or 'rept' 
		L: data type, one of the following options:
			for hope: 'l2.sectors'|'l2.spinaverage'|'l3.moments'|'l3.pitchangle'
			for mageis: 'l2'|'l3'
			for rept: 'l2'|'l3'
			
	
	'''
	#populate the list of dates to trace first
	Years = np.arange(StartYear,EndYear+1)
	n = Years.size
	
	#create output path if it doesn't exist
	outpath = Globals.DataPath+'ECT/{:s}/{:s}/{:s}/'.format(Inst,L,sc)
	if not os.path.isdir(outpath):
		os.system('mkdir -pv '+outpath)
		
	#loop through each remaining date and start downloading
	dp = re.compile('\d\d\d\d\d\d\d\d')
	vp = re.compile('v\d.\d.\d')
	for i in range(0,n):
		print('Year {0}'.format(Years[i]))
		urls,fnames = _GetCDFURL(Years[i],sc,Inst,L)
		nu = np.size(urls)
		
		idx = _ReadDataIndex(sc,L)
		new_idx = np.recarray(nu,dtype=idx.dtype)
		new_idx.Date[:] = -1
		p = 0
		for j in range(0,nu):
			print('Downloading file {0} of {1} ({2})'.format(j+1,nu,fnames[j]))
			Date = np.int32(dp.search(fnames[j]).group())
			Ver	= np.int32(vp.search(fnames[j]).group()[1:].replace('.',''))
			
			match = ((idx.Date == Date) & (idx.Version == Ver)).any()
			
			if (not match) or Overwrite:
				if not os.path.isfile(outpath+fnames[j]) or Overwrite:
					os.system('wget --no-check-certificate '+urls[j]+' -O '+outpath+fnames[j])

				new_idx.Date[p] = Date
				new_idx.FileName[p] = fnames[j]
				new_idx.Version[p] = Ver
				p+=1
				
		new_idx = new_idx[:p]
		
		#check for duplicates within new_idx (different versions)
		use = np.ones(p,dtype='bool')
		for j in range(0,p):
			match = np.where(new_idx.Date == new_idx.Date[j])[0]
			if match.size > 1:
				#compare versions
				mxVer = np.max(new_idx.Version[match])
				lose = np.where(new_idx.Version[match] != mxVer)[0]
				use[match[lose]] = False
		use = np.where(use)[0]
		new_idx = new_idx[use]
		p = new_idx.size
		
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
		_UpdateDataIndex(idx_out,sc,L)
		
			
