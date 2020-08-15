import numpy as np
import re

def _ExtractDateVersion(files,vfmt=['v','_']):
	'''
	extract dates and file versions for each file
	
	'''
	
	dp = re.compile('\d\d\d\d\d\d\d\d')
	if len(vfmt) == 1:
		vp = re.compile(vfmt[0]+'\d\d')
	else:
		vp = re.compile(vfmt[0]+'\d\d'+vfmt[1]+'\d\d')
	
	nf = np.size(files)
	Date = np.zeros(nf,dtype='int32')
	Ver = np.zeros(nf,dtype='int16')
	
	for i in range(0,nf):
		Date[i] = np.int32(dp.search(files[i]).group())
		tmp = (vp.search(files[i]).group()[1:]).replace(vfmt[0],'')
		if len(vfmt) == 1:
			Ver[i]	= np.int32(tmp)
		else:
			Ver[i]	= np.int32(tmp.replace(vfmt[1],''))
				
	return Date,Ver
