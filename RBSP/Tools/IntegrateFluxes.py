import numpy as np

def IntegrateFluxesDensity(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange=(0.0,np.inf)):
	'''
	Integrate the differential number flux as in Genestreti et al 2017
	in order to get a partial energy number density PEND
	
	'''
	
	if len(np.shape(E)) == 1:
		E = np.array([E])
	if len(np.shape(E0)) == 1:
		E0 = np.array([E0])
	if len(np.shape(E1)) == 1:
		E1 = np.array([E1])
	if len(np.shape(Flux)) == 1:
		Flux = np.array([Flux])

	#convert keV to J
	e = np.float64(1.6022e-19)
	Ej = np.float64(1000*e*E)
	Ej0 = np.float64(1000*e*E0)
	Ej1 = np.float64(1000*e*E1)
	Ejrange = np.array(Erange)*e*1000.0

	#shift the energy by the spacecraft potential
	Eprime = np.float64(E + np.abs(Vsc)/1000.0 - Ebulk/1000.0)
	Ejprime = np.float64(1000*e*Eprime)

	
	#calculate the energy fractions
	dEE = np.float64((E1-E0)/E)
	
	#convert Flux to SI units
	J = Flux*10.0 # times 10,000 to convert cm^-2 to m^-2, divide by 1000 for keV^-1 to eV^-1
	J = J/e # divide by electron charge to go from eV^-1 to J^-1
	
	#now the sum
	S = np.zeros(J.shape[0],dtype='float32')
	for i in range(0,J.shape[0]):
		use = np.where((Ejprime[i] >= Ejrange[0]) & (Ejprime[i] <= Ejrange[1]))[0]
		S[i] = np.sum(np.sqrt(Ejprime[i][use])*dEE[i][use]*np.float64(J[i][use]))
	
	#now get the density estimate (convert to cm^-3)
	ns = Omega*np.sqrt(m/2)*S/1e6
	
	return ns


def IntegrateFluxesPressure(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange=(0.0,np.inf)):
	'''
	Integrate the differential number flux to calculate a pressure.
	
	'''
	if len(np.shape(E)) == 1:
		E = np.array([E])
	if len(np.shape(E0)) == 1:
		E0 = np.array([E0])
	if len(np.shape(E1)) == 1:
		E1 = np.array([E1])
	if len(np.shape(Flux)) == 1:
		Flux = np.array([Flux])


	#convert keV to J
	e = np.float64(1.6022e-19)
	Ej = np.float64(1000*e*E)
	Ej0 = np.float64(1000*e*E0)
	Ej1 = np.float64(1000*e*E1)
	Ejrange = np.array(Erange)*e*1000.0

	#shift the energy by the spacecraft potential
	Eprime = np.float64(E + np.abs(Vsc)/1000.0 - Ebulk/1000.0)
	Ejprime = np.float64(1000*e*Eprime)

	
	#calculate the energy fractions
	dEE = np.float64((E1-E0)/E)
	
	#convert Flux to SI units
	J = Flux*10.0 # times 10,000 to convert cm^-2 to m^-2, divide by 1000 for keV^-1 to eV^-1
	J = J/e # divide by electron charge to go from eV^-1 to J^-1
	
	#now the sum
	S = np.zeros(J.shape[0],dtype='float32')
	for i in range(0,J.shape[0]):
		use = np.where((Ejprime[i] >= Ejrange[0]) & (Ejprime[i] <= Ejrange[1]))[0]
		S[i] = np.sum((Ejprime[i][use]**1.5)*dEE[i][use]*np.float64(J[i][use]))
	
	#now get the density estimate (convert to cm^-3)
	ps = 2*Omega*np.sqrt(m/2)*S/3
	
	#the divide by 3 factor comes from somewhere (not sure where exactly, but it appears to correct things)
	return ps
	
def IntegrateFluxesTemperature(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange=(0.0,np.inf)):

	#get density (convert to m^-3)
	n = IntegrateFluxesDensity(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange)*1e6
	
	#get pressure in pascals (I think)
	p = IntegrateFluxesPressure(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange)
	
	#get energy
	Te = p/n
	
	#convert Joules to Kelvin
	kB = np.float64(1.38064852e-23)

	T = Te/kB

	return T
	
def IntegrateFluxesNTP(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange=(0.0,np.inf)):
	'''
	Integrate fluxes in units of (keV sr cm^2 s)^-1 to calculate the 
	density, pressure and temperature in units of m^-3, Pa and K,
	repsectively.
	
	Inputs
	======
	E : float
		1D or 2D array of energy (must match dimensions of E0, E1 and
		Flux), where E is the energy of the centre of the bin (keV).
	E0 : float
		Lower bound of the energy bin (keV).
	E1 : float
		Upper bound of the energy bin (keV).
	Flux : float
		Measured differential number flux.
	m : float
		Particle mass in kg.
	Omega : float
		Solid angle (4*pi for HOPE)
	Vsc : float
		Array of spacecraft potentials to adjust energies by.
	Erange : tuple
		(min,max) tuple of the minimum and maximum energies to integrate 
		spectra over (keV), by default Erange=(0.0,np.inf).
	
	Returns
	=======
	n : float
		Density in SI units (m^-3).
	T : float
		Temperature (K).
	p : float
		Pressure (Pa).
	
	
	'''
		

	#get density (convert to m^-3)
	n = IntegrateFluxesDensity(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange)*1e6
	
	#get pressure in pascals (I think)
	p = IntegrateFluxesPressure(E,E0,E1,Flux,m,Omega,Vsc,Ebulk,Erange)
	
	#get energy
	Te = p/n
	
	#convert Joules to Kelvin
	kB = np.float64(1.38064852e-23)

	T = Te/kB

	return n,T,p
