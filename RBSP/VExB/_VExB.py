import numpy as np
from .. import Globals

datapath = Globals.DataPath + 'VExB/{:s}/' #.format(sc)


dtype = [	('Date','int32'),
			('ut','float32'),
			('utc','float64'),
			('Bx','float32'),
			('By','float32'),
			('Bz','float32'),
			('Ex','float32'),
			('Ey','float32'),
			('Ez','float32'),
			('mEx','float32'),
			('mEy','float32'),
			('mEz','float32'),
			('VxExB','float32'),
			('VyExB','float32'),
			('VzExB','float32'),
			('mVxExB','float32'),
			('mVyExB','float32'),
			('mVzExB','float32'),
			('x','float32'),
			('y','float32'),
			('z','float32'),
			('Vx','float32'),
			('Vy','float32'),
			('Vz','float32'),]
