import numpy as np

def mGSEtoGSE(mX,mY,mZ,wX,wY,wZ):
	'''
	Using the spin axis in GSE coordinates, convert mGSE to ordinary GSE
	
	'''
	
	p = np.arctan2(wY,wX)
	cosp = np.cos(p)
	sint = wX/cosp
	sinp = wY/sint
	cost = wZ
	
	X1 = sint*mX - cost*mZ
	Y1 = mY
	Z1 = cost*mX + sint*mZ
	
	X = cosp*X1 - sinp*Y1
	Y = sinp*X1 + cosp*Y1
	Z = Z1
	
	return (X,Y,Z) 
	
def GSEtomGSE(X,Y,Z,wX,wY,wZ):
	
	p = np.arctan2(wY,wX)
	cosp = np.cos(p)
	sint = wX/cosp
	sinp = wY/sint
	cost = wZ
	
	X1 = cosp*X + sinp*Y
	Y1 =-sinp*X + cosp*Y
	Z1 = Z
	
	mX = sint*X1 + cost*Z1
	mY = Y1
	mZ =-cost*X1 + sint*Z1
	
	return (mX,mY,mZ)
