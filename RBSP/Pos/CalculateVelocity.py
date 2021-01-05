import numpy as np

def CalculateVelocity(utc,x,y,z):
	'''
	Estimate the velocity using the position.
	
	Inputs
	======
	utc : float
		Continuous time array, hours since 1950
	x : float
		Array of x-coordinate (Re)
	y : float
		Array of y-coordinate (Re)
	z : float
		Array of z-coordinate (Re)
	
	Returns
	=======
	Vx : float
		x-component of velocity, m/s
	Vy : float
		y-component of velocity, m/s
	Vz : float
		z-component of velocity, m/s
	
	'''
	
	#create the output arrays
	Vx = np.zeros(utc.size,dtype='float32')
	Vy = np.zeros(utc.size,dtype='float32')
	Vz = np.zeros(utc.size,dtype='float32')
	
	#calculate the dt array and dx,dy,dz
	dt = utc[1:] - utc[:-1]
	dx = x[1:] - x[:-1]
	dy = y[1:] - y[:-1]
	dz = z[1:] - z[:-1]
	
	#now the velocities for all but the end elements
	dt2 = dt[:-1] + dt[1:]
	Vx[1:-1] = (dx[:-1] + dx[1:])/dt2
	Vy[1:-1] = (dy[:-1] + dy[1:])/dt2
	Vz[1:-1] = (dz[:-1] + dz[1:])/dt2

	#now the end elements
	Vx[0] = dx[0]/dt[0]
	Vx[-1] = dx[-1]/dt[-1]
	Vy[0] = dy[0]/dt[0]
	Vy[-1] = dy[-1]/dt[-1]	
	Vz[0] = dz[0]/dt[0]
	Vz[-1] = dz[-1]/dt[-1]
	
	#the units will be in Re/h, this needs to be m/s
	Re = 6371000.0
	Vx *= Re/3600.0
	Vy *= Re/3600.0
	Vz *= Re/3600.0
	
	return Vx,Vy,Vz
	
