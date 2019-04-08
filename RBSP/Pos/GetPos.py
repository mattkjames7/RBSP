from .ReadPos import ReadPos
from .. import Globals

def GetPos(sc='a'):
	'''
	Reads the binary files containing positional information about RBSP.

	Input:
		sc: 'a' or 'b'
		
	Returns:
		numpy.recarray
	'''
	
	if sc == 'b':
		pos = Globals.bPos
	else:
		pos = Globals.aPos
		
	if pos is None:
		pos = ReadPos(sc)
		
	return pos
