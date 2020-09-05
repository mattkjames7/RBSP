import os

#try and find the RBSP_PATH variable - this is where data will be stored
ModulePath = os.path.dirname(__file__)+'/'
try:
	DataPath = os.getenv('RBSP_PATH')+'/'
except:
	print('Please set RBSP_PATH environment variable')
	DataPath = ''

#RBSP position
aPos = None
bPos = None


#functions which will interpolate the positions/traces of each spacecraft
TraceFuncs = {}
