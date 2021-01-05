import numpy as np
from .Gamma import Gamma
from .PSDtoCounts import PSDtoCounts
from .RelVelocity import RelVelocity

k_B = 1.38064852e-23

def KappaDist(n,v,T,m,K):
	
	Tk = K*T/(K-1.5)
	wk = np.sqrt(((2.0*K - 3.0)*k_B*Tk)/(K*m))
	f = (n/(2.0*np.pi*(K*wk**2.0)**1.5)) * (Gamma(K+1)/(Gamma(K-0.5)*Gamma(1.5))) * (1.0 + (v**2)/(K*wk**2))**(-(K+1))
	
	return f 
	
def KappaDistE(n,E,T,m,K):
	v = RelVelocity(E,m)
	Tk = K*T/(K-1.5)
	wk = np.sqrt(((2.0*K - 3.0)*k_B*Tk)/(K*m))
	f = (n/(2.0*np.pi*(K*wk**2.0)**1.5)) * (Gamma(K+1)/(Gamma(K-0.5)*Gamma(1.5))) * (1.0 + (v**2)/(K*wk**2))**(-(K+1))
	
	return f 


def KappaDistCts(n,v,T,m,K,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):
	
	f = KappaDist(n,v,T,m,K)
	return PSDtoCounts(v,f,m,Eff,dOmega,nSpec,Tau,g)
	
	
def KappaDistCtsE(n,E,T,m,K,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):
	
	v = RelVelocity(E,m)
	f = KappaDist(n,v,T,m,K)
	return PSDtoCounts(v,f,m,Eff,dOmega,nSpec,Tau,g)
	
