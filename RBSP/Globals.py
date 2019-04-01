import os

#try and find the RBSP_PATH variable - this is where data will be stored
ModulePath = os.path.dirname(__file__)+'/'
try:
	DataPath = os.getenv('RBSP_PATH')+'/'
except:
	print('Please set RBSP_PATH environment variable')
	DataPath = ''
