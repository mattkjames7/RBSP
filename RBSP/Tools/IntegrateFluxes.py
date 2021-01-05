import numpy as np

def IntegrateFluxes(E,E0,E1,Flux,m,Omega,Vsc,Erange=(0.0,np.inf)):
	'''
	Integrate the differential number flux as in Genestreti et al 2017
	in order to get a partial energy number density PEND
	
	'''

	#convert keV to J
	e = np.float64(1.6022e-19)
	Ej = np.float64(1000*e*E)
	Ej0 = np.float64(1000*e*E0)
	Ej1 = np.float64(1000*e*E1)

	#shift the energy by the spacecraft potential
	Eprime = np.float64(E + np.abs(Vsc))
	Ejprime = np.float64(1000*e*Eprime)
	
	#calculate the energy fractions
	dEE = np.float64((E1-E0)/E)
	
	#convert Flux to SI units
	J = Flux*10.0 # times 10,000 to convert cm^-2 to m^-2, divide by 1000 for keV^-1 to eV^-1
	J = J/e # divide by electron charge to go from eV^-1 to J^-1
	
	#now the sum
	S = np.zeros(J.shape[0],dtype='float32')
	for i in range(0,J.shape[0]):
		use = np.where((Ejprime[i] >= Erange[0]) & (Ejprime[i] <= Erange[1]))[0]
		S[i] = np.sum(np.sqrt(Ejprime[i][use])*dEE[i][use]*np.float64(J[i][use]))
	
	#now get the density estimate
	ns = Omega*np.sqrt(m/2)*S/1e6
	
	return ns
