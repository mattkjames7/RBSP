import numpy as np
from .. import EFW
from .. import EMFISIS



def DataAvailability(sc='a',Split=False):
	'''
	Return a list of the dates when both sets of field data are available
	
	'''
	edates = EFW.DataAvailability(sc,'l3')
	bdates = EMFISIS.DataAvailability(sc,'l3','1sec-gse')
	
	if Split:
		return edates,bdates
	
	good = np.zeros(edates.size,dtype='bool8')
	for i in range(0,edates.size):
		if edates[i] in bdates:
			good[i] = True
	
	use = np.where(good)[0]
	return edates[good]
