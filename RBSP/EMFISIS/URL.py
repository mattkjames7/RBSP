import numpy as np
import DateTimeTools as TT

def URL(sc,L):
	'''
	Returns a function which works out the URLs for a given date
	
	Inputs
	======
	sc: str
		'a' or 'b'
	L: str
		Data level 'l4'|'l3'|'l2'

	'''
	#the level string
	Lu = L.upper()
		
	#sc string
	scu = sc.upper()
	
	def URLFunction(Date):
	
		#get the date
		Year,Month,Day = TT.DateSplit(Date)

		url0 = 'https://emfisis.physics.uiowa.edu/Flight/RBSP-{:s}/{:s}/{:4d}/{:02d}/{:02d}/'.format(scu,Lu,Year[0],Month[0],Day[0])

		return url0
	
	return URLFunction
	# #set up a temporary file/path 
	# tmppath = Globals.DataPath+'tmp/'
	# if not os.path.isdir(tmppath):
		# os.system('mkdir -pv '+tmppath)
	# tmpfname = tmppath + '{:17.7f}.tmp'.format(time.time())
	
	# #wget the file
	# os.system('wget '+url0+' -O '+tmpfname)
	
	# #read it
	# f = open(tmpfname,'r')
	# lines = f.readlines()
	# n = np.size(lines)
	# f.close()
	
	# #delete it
	# os.system('rm -v '+tmpfname)
	
	
	# #now search for the line with the substring '.cdf"'
	# urls = []
	# fnames = []
	# for i in range(0,n):
		# if '.cdf"' in lines[i]:
			# s = lines[i].split('"')
			# for ss in s:
				# if '.cdf' in ss:
					# urls.append(url0+ss)
					# fnames.append(ss)
					# break
					
	# return urls,fnames
	
