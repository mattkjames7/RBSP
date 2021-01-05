import numpy as np
from .PSDtoCounts import PSDtoCounts
from .RelVelocity import RelVelocity

k_B = np.float64(1.38064852e-23)
e = np.float64(1.6022e-19)


def MaxwellBoltzmannDist(n,v,T,m):
	
	vth = np.sqrt(k_B*np.float64(T)/np.float64(m))
	f = n* (1.0/(vth*(np.sqrt(2.0*np.pi)))**3.0)*  np.exp(-v**2.0/(2.0*vth**2.0))
	return f

def MaxwellBoltzmannDistE(n,E,T,m):
	v = RelVelocity(E,m)
	vth = np.sqrt(k_B*T/m)
	f = n* (1.0/(vth*(np.sqrt(2.0*np.pi)))**3.0) *  np.exp(-v**2.0/(2.0*vth**2.0))
	return f


def MaxwellBoltzmannDistCts(n,v,T,m,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):

	f = MaxwellBoltzmannDist(n,v,T,m)
	return PSDtoCounts(v,f,m,Eff,dOmega,nSpec,Tau,g)

def MaxwellBoltzmannDistCtsE(n,E,T,m,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):

	v = RelVelocity(E,m)
	f = MaxwellBoltzmannDist(n,v,T,m)
	return PSDtoCounts(v,f,m,Eff,dOmega,nSpec,Tau,g)
