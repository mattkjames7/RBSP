import numpy as np


def CalculateEx(Ey,Ez,Bx,By,Bz):
	'''
	This routine is for calculating the x mGSE component of the electric
	field based upon the y and z components with the magnetic field
	assuming that E x B = 0
	
	'''
	Ex = -(Ez*Bz + Ey*By)/Bx
	return Ex
