import numpy as np

def GSMtoDipolar(Bx,By,Bz,mBx,mBy,mBz,x,y,z):
	'''
	Convert magnetic/electric field data to dipolar coords
	
	Inputs
	======
	Bx,By,Bz : float
		Magnetic or electric field vectors to be rotated - not sure if 
		GSM or SM is best for this, whichever system is used - make sure
		it's the same as for the other variables
	mBx,mBy,mBz : float
		Model or long term average field vectors
	x,y,z : float
		Position vectors
		
	Returns
	=======
	P,T,C : float
		Poloidal, toroidal and compressional components
	
	'''
	
	#original field
	x0 = np.array(Bx)
	y0 = np.array(By)
	z0 = np.array(Bz)

	#original model field
	mx0 = np.array(mBx)
	my0 = np.array(mBy)
	mz0 = np.array(mBz)	

	#position
	px = np.array(x)
	py = np.array(y)
	pz = np.array(z)
	
	#find MLT and transform x and y such that x1 points 
	#away from Earth in the equatorial plane
	a = np.arctan2(py,-px)
	
	x1 = x0*np.cos(a) - y0*np.sin(a)
	y1 = x0*np.sin(a) + y0*np.cos(a)
	z1 = z0

	mx1 = mx0*np.cos(a) - my0*np.sin(a)
	my1 = mx0*np.sin(a) + my0*np.cos(a)
	mz1 = mz0
	
	
	#find tilt angle of the field line (-b) and rotate z1 
	#and x1 around y1 such that x2 = 0 and z2 = sqrt(x1^2 + z1^2)
	b = -np.arctan2(mx1,mz1)
	
	x2 = z1*np.sin(b) + x1*np.cos(b)
	y2 = y1
	z2 = z1*np.cos(b) - x1*np.sin(b)

	mx2 = mz1*np.sin(b) + mx1*np.cos(b)
	my2 = my1
	mz2 = mz1*np.cos(b) - mx1*np.sin(b)	
	
	
	#finally, rotate z2 and y2 around x2 such that z3 is pointed
	#along the field line (hopefully)
	c = np.arctan2(my2,mz2)
	
	x3 = x2
	y3 = y2*np.cos(c) - z2*np.sin(c)
	z3 = y2*np.sin(c) + z2*np.cos(c)
	

	return (x3,y3,z3)


def _RotationMatrix(A,B):
	'''
	get rotation matrix R which maps vector A to B
	
	'''

	
	K = np.dot(B,A.T) - np.dot(A,B.T)
	K2 = np.dot(K,K)
	
	IP = np.sum(A*B)
	
	I = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
	
	R = K + I + (1.0/(1.0 + IP))*K2
	
	return R
	

def GSMtoDipolar2(Bx,By,Bz,mBx,mBy,mBz,x,y,z):
	'''
	Convert magnetic/electric field data to dipolar coords
	
	Inputs
	======
	Bx,By,Bz : float
		Magnetic or electric field vectors to be rotated - not sure if 
		GSM or SM is best for this, whichever system is used - make sure
		it's the same as for the other variables
	mBx,mBy,mBz : float
		Model or long term average field vectors
	x,y,z : float
		Position vectors
		
	Returns
	=======
	P,T,C : float
		Poloidal, toroidal and compressional components
	
	'''
	
	#original field
	Bx0 = np.array(Bx)
	By0 = np.array(By)
	Bz0 = np.array(Bz)

	#original model field
	mx0 = np.array(mBx)
	my0 = np.array(mBy)
	mz0 = np.array(mBz)	

	#position
	x0 = np.array(x)
	y0 = np.array(y)
	z0 = np.array(z)
	
	#find MLT and transform x and y such that x1 points 
	#away from Earth in the equatorial plane
	a = np.arctan2(y0,-x0)
	
	Bx1 = Bx0*np.cos(a) - By0*np.sin(a)
	By1 = Bx0*np.sin(a) + By0*np.cos(a)
	Bz1 = Bz0

	mx1 = mx0*np.cos(a) - my0*np.sin(a)
	my1 = mx0*np.sin(a) + my0*np.cos(a)
	mz1 = mz0
	
	#loop through each vector and transform into coords which should
	#be field aligned
	n = Bx0.size
	Bx2 = np.zeros(n,dtype='float32')
	By2 = np.zeros(n,dtype='float32')
	Bz2 = np.zeros(n,dtype='float32')
	mx2 = np.zeros(n,dtype='float32')
	my2 = np.zeros(n,dtype='float32')
	mz2 = np.zeros(n,dtype='float32')
	
	for i in range(0,n):
		B = np.array([[0.0],[0.0],[1.0]])
		M = np.array([[mx1[i]],[my1[i]],[mz1[i]]])
		A = M/np.linalg.norm(M)
		
		R = _RotationMatrix(A,B)
		X = np.array([[Bx1[i]],[By1[i]],[Bz1[i]]])
		
		Br = np.dot(R,X)
		Bx2[i] = Br[0,0]
		By2[i] = Br[1,0]
		Bz2[i] = Br[2,0]
		
		mr = np.dot(R,M)
		mx2[i] = mr[0,0]
		my2[i] = mr[1,0]
		mz2[i] = mr[2,0]
		

	return Bx2,By2,Bz2
