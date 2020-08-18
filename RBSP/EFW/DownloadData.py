from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData
from . import _EFW
from .URL import URL

def DownloadData(sc='a',L='l3',Date=[20120901,20200101],Overwrite=False,Verbose=True):
	'''
	Downloads EFW data.

	Inputs
	======
	Date: int
		Date in format yyyymmdd
	sc: str
		'a' or 'b'
	L: str
		Data level, see below

	Available data products
	=======================
	'l3' (Spin-fit Electric field in modified-GSE (MGSE) coord, density, and other products)
	'l2.spec' (8 second FFT power spectra)
	'l2.e-spinfit-mgse' (Spin-fit E12 Electric field in modified-GSE (MGSE) coordinates)
	'l2.fbk' (8 sample/sec filterbank peak, average wave amplitude)
	'l2.esvy_despun' (32 sample/sec despun electric field in modified-GSE (MGSE) coordinates)
	'l2.vsvy-hires' (16 sample/sec single-ended V1-V6 probe potentials)
	'l1.eb1' (EB1 in UVW coordinates)
	'l1.eb2' (EB2 in UVW coordinates)
	'l1.mscb1' (MSCB1 in UVW coordinates)
	'l1.mscb2' (MSCB2 in UVW coordinates)
	'l1.vb1' (VB1 in UVW coordinates)
	'l1.vb2'(VB2 in UVW coordinates)
	
	'''
	URLF = URL(sc,L)
	_DownloadData(URLF,_EFW.idxfname.format(L,sc),_EFW.datapath.format(L,sc),
			Date,_EFW.vfmt,None,Overwrite,Verbose)
	
	
	
	
	# #populate the list of dates to trace first
	# Years = np.arange(StartYear,EndYear+1)
	# n = Years.size
	
	# #create output path if it doesn't exist
	# outpath = Globals.DataPath+'EFW/{:s}/{:s}/'.format(L,sc)
	# if not os.path.isdir(outpath):
		# os.system('mkdir -pv '+outpath)
		
	# #loop through each remaining date and start downloading
	# dp = re.compile('\d\d\d\d\d\d\d\d')
	# vp = re.compile('v\d\d')
	# for i in range(0,n):
		# print('Year {0}'.format(Years[i]))
		# urls,fnames = _GetCDFURL(Years[i],sc,L)
		# nu = np.size(urls)
		
		# idx = _ReadDataIndex(sc,L)
		# new_idx = np.recarray(nu,dtype=idx.dtype)
		# new_idx.Date[:] = -1
		# p = 0
		# for j in range(0,nu):
			# print('Downloading file {0} of {1} ({2})'.format(j+1,nu,fnames[j]))
			# Date = np.int32(dp.search(fnames[j]).group())
			# Ver	= np.int32(vp.search(fnames[j]).group()[1:])
			
			# match = ((idx.Date == Date) & (idx.Version == Ver)).any()
			
			# if (not match) or Overwrite:
				# if not os.path.isfile(outpath+fnames[j]) or Overwrite:
					# os.system('wget '+urls[j]+' -O '+outpath+fnames[j])

				# new_idx.Date[p] = Date
				# new_idx.FileName[p] = fnames[j]
				# new_idx.Version[p] = Ver
				# p+=1
				
		# new_idx = new_idx[:p]
		
		# #check for duplicates within new_idx (different versions)
		# use = np.ones(p,dtype='bool')
		# for j in range(0,p):
			# match = np.where(new_idx.Date == new_idx.Date[j])[0]
			# if match.size > 1:
				# #compare versions
				# mxVer = np.max(new_idx.Version[match])
				# lose = np.where(new_idx.Version[match] != mxVer)[0]
				# use[match[lose]] = False
		# use = np.where(use)[0]
		# new_idx = new_idx[use]
		# p = new_idx.size
		
		# #check for duplicates within old index
		# usen = np.ones(p,dtype='bool')
		# useo = np.ones(idx.size,dtype='bool')
			
		# for j in range(0,p):
			# match = np.where(idx.Date == new_idx.Date[j])[0]
			# if match.size > 0:
				# if idx.Version[match[0]] > new_idx.Version[j]:
					# #old one is newer (unlikely)
					# usen[j] = False
				# else:
					# #new one is newer
					# useo[match[0]] = False

		# usen = np.where(usen)[0]
		# new_idx = new_idx[usen]
		# useo = np.where(useo)[0]
		# idx = idx[useo]					
		
		# #join indices together and update file
		# idx_out = RT.JoinRecarray(idx,new_idx)
		# srt = np.argsort(idx_out.Date)
		# idx_out = idx_out[srt]
		# _UpdateDataIndex(idx_out,sc,L)
		
			
