import numpy as np
import matplotlib.pyplot as plt
from .MaxwellBoltzmannDist import MaxwellBoltzmannDist
from .RelVelocity import RelVelocity
from .IntegrateFluxes import IntegrateFluxesDensity,IntegrateFluxesPressure,IntegrateFluxesTemperature
from .PSDtoFlux import PSDtoFlux
from scipy.special import erfinv

def TestIntegrate(fig=None,maps=[1,1,0,0],ncm=500.0,TeV=0.25,ueff=8000.0,Emin=1.0,Vsc=0.0,necm=500.0):
	
	'''
	Emin is the minimum energy of HOPE
	Vsc = spacecraft charging
	
	'''
	
	
	e = np.float64(1.602e-19)
	kB = np.float64(1.381e-23)

		
	#density in m^-3
	n = ncm*1e6
	
	#temperature in K (converted from eV)
	T = np.float64(TeV*e)/kB
	
	#pressure in Pa
	p = kB*T*n
	
	#create a velocity array (m/s)
	v = np.linspace(0.0,100000.0,1000)
	
	#mass of proton in kg
	m = 1.6726219e-27

	#calcualte Ebulk (eV)
	Ebulk = (0.5*m*ueff**2)/e
	print('Ebulk (eV): ',Ebulk)
	print('1.25Ebulk (eV): ',1.25*Ebulk)
	
	#now the psd
	F = 4*np.pi*MaxwellBoltzmannDist(n,v,T,m)*v**2
	
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
	else:
		ax = fig

	ax.plot(v,F)
	R = ax.axis()
	ax.axis(R)
	ax.plot([ueff,ueff],[R[2],R[3]],color='blue',linestyle='--')
	
	#integrate to get density
	ni = np.trapz(F,v)
	print('n (cm^-3): ',n/1e6)
	print('ni (cm^-3): ',ni/1e6)
	
	#integrate to get pressure
	pi = np.trapz(m*F*v**2,v)/3
	print('p (nPa): ',p*1e9)
	print('pi (nPa): ',pi*1e9)	
	
	#calculate temperature
	Ti = (pi/ni)/kB
	print('T (K): ',T)
	print('Ti (K): ',Ti)
	
	#estimate HOPE energy bins
	lEH = np.linspace(np.log10(0.001),np.log10(50.0),72)
	EH = 10**lEH
	dlE = 0.5*(lEH[1:] - lEH[:-1])
	lE0 = np.append(lEH[:-1]-dlE,lEH[-1]-dlE[-1])
	lE1 = np.append(lEH[1:]-dlE,lEH[-1]+dlE[-1])
	E0 = 10**lE0
	E1 = 10**lE1
	vH = RelVelocity(EH,m)
	
	#get the maxwellian dist at each point
	FH = 4*np.pi*MaxwellBoltzmannDist(n,vH,T,m)*vH**2
	
	#scatter the points where the bins are
	ax.scatter(vH,FH)
	
	#Calculate the flux
	fH = FH/(4*np.pi*vH**2)
	FluxH = PSDtoFlux(vH,fH,m)
	Ebulk=0.0
	#calcualte nPEND
	nPEND = IntegrateFluxesDensity(np.array([EH]),np.array([E0]),np.array([E1]),np.array([FluxH]),m,4*np.pi,Vsc,Ebulk)[0]
	print('nPEND (cm^-3): ',nPEND)
	
	#get the pressure and temperature
	TPEND = IntegrateFluxesTemperature(np.array([EH]),np.array([E0]),np.array([E1]),np.array([FluxH]),m,4*np.pi,Vsc,Ebulk)[0]
	print('TPEND (K): ',TPEND)	
	pPEND = IntegrateFluxesPressure(np.array([EH]),np.array([E0]),np.array([E1]),np.array([FluxH]),m,4*np.pi,Vsc,Ebulk)[0]
	print('pPEND (nPa): ',pPEND*1e9)
	
	#another TPEND from genestreti et al
	TPENDGeV = (np.sqrt(2)*((Emin + Vsc)-Ebulk))/(erfinv(1-nPEND/necm))
	TPENDG = TPENDGeV*e/kB
	
	print('TPEND (G2017) (eV) : ',TPENDGeV)
	print('TPEND (G2017) (K) : ',TPENDG)
	
	return ax
