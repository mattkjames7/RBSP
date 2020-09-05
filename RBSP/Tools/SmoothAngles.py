import numpy as np

def SmoothAngles(A0,Units='deg'):
	A = np.copy(A0)
	if Units == 'rad':
		A = A*180.0/np.pi
	
	n = np.size(A)
	for i in range(1,n):
		if ((A[i]-A[i-1]) > 180.0):
			A[i:]-=360.0 
		if ((A[i-1]-A[i]) > 180.0):
			A[i:]+=360.0 
	
	if Units == 'rad':
		A = A*np.pi/180.0
	
	return A
