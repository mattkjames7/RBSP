import numpy as np
from .RelVelocity import RelVelocity

def IntegrateSpectrum(E,PSD,m,Omega,Erange=(0.0,np.inf)):
	'''
	Integrate the phase space density to get the partial density.
	
	Inputs
	======
	E : float
		Energy in keV.
	PSD : float
		Phase space density s^3 m^-6. (this includes density)
	m : float
		Mass in kg.
	Erange : tuple
		2-element tuple specifying the energy range over which to 
		integrate.
		
	Returns
	=======
	n : float
		Partial density.
		
	NOTE: This probably won't work for reletavistic particles, so I 
	should probably rewrite this in terms of E instead of V
	'''

	#firstly work out the number of spectra
	if len(PSD.shape) == 1:
		ns = 1
	else:
		ns = PSD.shape[0]
	
	#limit E and PSD to within the energy range
	if len(E.shape) == 1:
		e = np.array([E]*ns)
	else:
		e = np.array(E)

	etmp = np.nanmean(e,axis=0)
	use = np.where((etmp >= Erange[0]) & (etmp <= Erange[1]))[0]
	e = e[:,use]
		
	if len(PSD.shape) == 1:
		p = np.array([PSD[use]]).astype('float64')
	else:
		p = PSD[:,use].astype('float64')
		
	
	
	#convert E to V
	v = RelVelocity(e,m).astype('float64')
	
	#integrate, convert to cm^-2
	n = np.zeros(ns,dtype='float64')
	pv2 = p*v**2

	for i in range(0,ns):
		use = np.where(p[i] > 0)[0]
		
		if use.size > 1:	
			n[i] = 1e-6*np.trapz(pv2[i,use],v[i,use])*Omega
		else:
			n[i] = np.nan
	return n
