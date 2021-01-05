import numpy as np

def ProcessEnergyBins(E,dE=None):
	'''
	Convert the energy bins given in the file to E0, E1 and Emid (min,
	max and middle, respectively)
	
	Inputs
	======
	E : numpy.ndarray
		This can either be 1-D, containing the energy bins for all time,
		or it can be 2-D, where there is a different set of energy bins 
		for each step in time, with a shape (nt,nE).
	dE : Set this to define the half width of the energy bin (such that
		E0 = E - dE and E1 - E + dE). If set to None, then half of the 
		log difference between each energy bin will be used.
		
	Returns
	=======
	E0 : numpy.ndarray
		Minimum energy bins.
	E1 : numpy.ndarray
		Maximum energy bins.
	Emid : numpy.ndarray
		Middle of energy bins in log-space.
	
	'''
	
	#firstly we need to determine the number of dimensions
	nd = len(E.shape)

	#get the log of the energy
	E = np.array(E)
	lE = np.log10(E)
	
	if nd == 1:
		#In this case, we have a one dimensional E array and we assume 
		#that, if supplied, the dE array is also 1-D
		
		#sort the energy
		srt = np.argsort(lE)
		E = E[srt]
		lE = lE[srt]
		
		#check if we need to calculate dE
		if dE is None:
			#use the mid-point in log-space
			dlE = (lE[1:] - lE[:-1])/2
			dlE = np.concatenate(([lE[0]],0.5*(lE[:-1] + lE[1:]),[lE[-1]]))
			lE0 = lE - dlE
			lE1 = lE + dlE
			E0 = 10**lE0
			E1 = 10**lE1
		else:
			dE = dE[srt]
			
			#use provided dE
			E0 = E - dE
			E1 = E + dE
		
		#return to original order
		E[srt] = E
		E0[srt] = E0
		E1[srt] = E1
		
	else:
		#here we have a 2-D E array and either a 1-D or 2-D dE array
		
		
		#sort the arrays	
		srt = np.argsort(np.nanmean(E,axis=0))
		E = E[:,srt]
		lE = lE[:,srt]
		
		#check if we need to calculate dE
		if dE is None:
			#use the mid-point in log-space
			dlE = (lE[:,1:] - lE[:,:-1])/2
			dlE = np.concatenate((np.array([dlE[:,0]]).T,0.5*(dlE[:,:-1] + dlE[:,1:]),np.array([dlE[:,-1]]).T),axis=1)
			lE0 = lE - dlE
			lE1 = lE + dlE
			E0 = 10**lE0
			E1 = 10**lE1
		else:
			if len(dE.shape) == 2:
				dE = dE[:,srt]
			else:		
				dE = dE[srt]
			
			#use provided dE
			E0 = E - dE
			E1 = E + dE
		
		#return to original order
		E[:,srt] = E
		E0[:,srt] = E0
		E1[:,srt] = E1		
		
		
	Emid = E

	return E0,E1,Emid

def ProcessEnergyBinsOld(E,nE=None,dE=None):
	'''
	Convert the energy bins given in the file to E0, E1 and Emid (min,
	max and middle, respectively)
	
	Inputs
	======
	E : numpy.ndarray
		This can either be 1-D, containing the energy bins for all time,
		or it can be 2-D, where there is a different set of energy bins 
		for each step in time, with a shape (nt,nE).
	nE : Use this to set the number of desired energy bins; if None then
		nE is assumed to be the number of energy bins in E, where E will
		be assumed to be the lower limit of the bin.
		
	Returns
	=======
	E0 : numpy.ndarray
		Minimum energy bins.
	E1 : numpy.ndarray
		Maximum energy bins.
	Emid : numpy.ndarray
		Middle of energy bins in log-space.
	
	'''
	
	#firstly we need to determine the number of dimensions
	nd = len(E.shape)

	#get the log of the energy
	lE = np.log10(E)
	
	if nd == 1:
		sE = np.size(E)
		if nE is None:
			nE = np.size(E)
		

		if sE == nE:
			srt = np.argsort(lE)
			lE = lE[srt]
			lE0 = lE
			dlE = lE[1:] - lE[:-1]
			dlE = np.append(dlE,dlE[-1])
			lE1 = lE0 + dlE
			lE0[srt] = lE0
			lE1[srt] = lE1
		else:
			lE0 = lE[:-1]
			lE1 = lE[1:]
			
	else:
		sE = E.shape[1]
		if nE is None:
			nE = E.shape[1]
		
		if sE == nE:
			srt = np.argsort(lE[0,:])
			lE = lE[:,srt]			
			lE0 = lE
			dlE = lE[:,1:] - lE[:,:-1]
			dlE = np.concatenate((dlE,np.array([dlE[:,-1]]).T),axis=1)
			lE1 = lE0 + dlE
			lE0[:,srt] = lE0
			lE1[:,srt] = lE1			
		else:
			lE0 = lE[:,:-1]
			lE1 = lE[:,1:]		
		
		
	lEmid = 0.5*(lE0 + lE1)
	
	Emid = 10**lEmid
	E0 = 10**lE0
	E1 = 10**lE1

	return E0,E1,Emid
