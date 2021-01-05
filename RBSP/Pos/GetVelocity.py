import numpy as np
from .GetPos import GetPos
from .CalculateVelocity import CalculateVelocity
from .. import Globals

def GetVelocity(sc='a',Coord='GSE'):
	'''
	Get the spacecraft velocity for the entire mission.
	
	Inputs
	======
	sc : str
		'a'|'b', the spacecraft.
	Coord : str
		Coordinate system wanted, can be one of the following:
		'GSE'|'GSM'|'SM'|'GEO'
		
	Return
	======
	vel : numpy.recarray
		Recarray containing the position and velocity for the requested 
		coordinate system.
	
	'''
	
	#get the position
	pos = GetPos(sc)
	
	#check if the velocity exists in memory already
	label = sc.lower() + Coord.lower()
	if label in list(Globals.Vel.keys()):
		vel = Globals.Vel[label]
	else:
		#create the output array
		dtype = [	('Date','int32'),
					('ut','float32'),
					('utc','float64'),
					('x','float32'),
					('y','float32'),
					('z','float32'),
					('Vx','float32'),
					('Vy','float32'),
					('Vz','float32') ]
					
		vel = np.recarray(pos.size,dtype=dtype)
		
		#Get the positions for the requested coordinate system
		vel.Date = pos.Date
		vel.ut = pos.ut
		vel.utc = pos.utc
		vel.x = pos['X'+Coord.lower()]
		vel.y = pos['Y'+Coord.lower()]
		vel.z = pos['Z'+Coord.lower()]
		
		#get the velocity
		vel.Vx,vel.Vy,vel.Vz = CalculateVelocity(vel.utc,vel.x,vel.y,vel.z)
		
		#add to the global dict
		Globals.Vel[label] = vel
		
	return vel
