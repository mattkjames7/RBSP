import numpy as np
from .. import Globals
import DateTimeTools as TT
import RecarrayTools as RT
def ReadFieldFootprintTraces(Date,sc='a',Model='T96'):
	'''
	Reads the footprint trace files.
	
	'''
	
	#populate the list of dates
	Date = np.array([Date]).flatten()
	if Date.size > 1:
		date = Date[0]
		dates = []
		while date <= Date[-1]:
			dates.append(date)
			date = TT.PlusDay(date)
		dates = np.array(dates)
		n = np.size(dates)
	else:
		dates = Date
		n = 1
	print(dates)
		
	#now to list the files
	path = Globals.DataPath+'Traces/{:s}/{:s}/'.format(Model,sc)
	fpatt = path + '{:08d}.bin'
	files = np.array((n,),dtype='object')
	print(files)
	for i in range(0,n):
		files[i] = fpatt.format(dates[i])
		
	#open each file to count the total number of records to load
	nt = 0
	for i in range(0,n):
		f = open(files[i],'rb')
		tmp = np.fromfile(f,dtype='int32',count=1)[0]
		f.close()
		nt += tmp
	
	#create output array
	dtype=[('Date','int32'),('ut','float32'),('MlatN','float32'),('MlatS','float32'),
			('GlatN','float32'),('GlatS','float32'),('MlonN','float32'),('MlonS','float32'),
			('GlonN','float32'),('GlonS','float32'),('MltN','float32'),('MltS','float32'),
			('GltN','float32'),('GltS','float32'),('MltE','float32'),('Lshell','float32'),
			('FlLen','float32'),('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
			('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
			('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
	out = np.recarray(nt,dtype=dtype)
	
	#load each file
	p = 0
	for i in range(0,n):
		tmp = RT.ReadRecarray(files[i],dtype)
		out[p:p+tmp.size] = tmp
		p += tmp.size

	return out
