import os
from .. import Globals



'''
Should change this function to download the position from
https://emfisis.physics.uiowa.edu/Flight/RBSP-A/LANL/MagEphem/
'''
def _DownloadPos():
	'''
	Downloads position data and extracts it to RBSP_PATH/Pos. 
	'''

	arch = ['https://github.com/mattkjames7/RBSP/raw/master/DATA/rbspa.bin.bz2',
			'https://github.com/mattkjames7/RBSP/raw/master/DATA/rbspb.bin.bz2']
	
	#firstly, let's check what exists
	Path = Globals.DataPath+'Pos/'
	path_exists = os.path.isdir(Path)
	fname = ['rbspa','rbspb']
	
	data_exists = [os.path.isfile(Path+fname[0]+'.bin'),
					os.path.isfile(Path+fname[1]+'.bin')]
	
	arch_exists =  [os.path.isfile(Path+fname[0]+'.bin.bz2'),
					os.path.isfile(Path+fname[1]+'.bin.bz2')]
	

	#create the directory if needed
	if not path_exists:
		os.system('mkdir -pv '+Path)
		
	for i in range(0,2):
		if not data_exists[i] and not arch_exists[i]:
			#neither data nor archive exists, download then extract
			print('Downloading position data for {:s}...'.format(fname[i]))
			os.system('wget '+arch[i]+' -O '+Path+fname[i]+'.bin.bz2')
			print('Extracting archive...')
			os.system('bunzip2 '+Path+fname[i]+'.bin.bz2')
		elif arch_exists[i] and not data_exists[i]:
			#just need to extract the archive
			print('Extracting archive...')
			os.system('bunzip2 '+Path+fname[i]+'.bin.bz2')
		else:
			#data must already exist
			print('Data for {:s} already exists, nothing to do'.format(fname[i]))			
			
			
