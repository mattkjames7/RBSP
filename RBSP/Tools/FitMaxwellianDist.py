import numpy as np
from .MaxwellBoltzmannDist import MaxwellBoltzmannDist,MaxwellBoltzmannDistCts
from .MaxwellBoltzmannDist import MaxwellBoltzmannDistE,MaxwellBoltzmannDistCtsE
from scipy.optimize import minimize

def _GetMisfitFunc(v,f,mass):
		
	def Func(X):
		n,T = X 
		
		fm = MaxwellBoltzmannDist(n,v,T,mass)
		
		lf = np.log10(f)
		lm = np.log10(fm)
		diff = np.sqrt(np.sum(((lf-lm)**2))/f.size)
		
		return diff

	return Func

def FitMaxwellianDist(v,f,n0,T0,mass,Verbose=False,MaxIter=None):

	#select only good data to fit to
	good = np.where(np.isfinite(f) & (f > 0))[0]
	if (good.size < 3.0):
		return -1, -1, False
	Func = _GetMisfitFunc(v[good],f[good],mass)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0],method='nelder-mead',options=opt)
	#return n,T fitted
	n,t = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad M-B fit')
		print(res.message)
	return n,t,res.success

		
def _GetMisfitFuncCts(v,C,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0):
		
	def Func(X):
		n,T = X 
		
		Cm = MaxwellBoltzmannDistCts(n,v,T,mass,Eff,dOmega,nSpec,Tau,g)
		
		diff = np.sqrt(np.sum(((C-Cm)**2))/C.size)
		
		return diff

	return Func

def FitMaxwellianDistCts(v,Counts,n0,T0,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0,Verbose=False,MaxIter=None):
	
	bad = np.where(np.isfinite(Counts) == False)[0]
	Cs = np.copy(Counts)
	Cs[bad] = 0.0
	

	#select only good data to fit to
	good = np.where((Cs >= 0.0))[0]
	if (good.size < 3.0):
		return -1, -1, False
	Func = _GetMisfitFuncCts(v[good],Counts[good],mass,dOmega,Eff,nSpec,Tau,g)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0],method='nelder-mead',options=opt)
	#return n,T fitted
	n,t = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad M-B fit')
		print(res.message)
	return n,t,res.success

def _GetMisfitFuncE(E,f,mass):
		
	def Func(X):
		n,T = X 
		
		fm = MaxwellBoltzmannDistE(n,E,T,mass)
		
		lf = np.log10(f)
		lm = np.log10(fm)
		diff = np.sqrt(np.sum(((lf-lm)**2))/f.size)
		
		return diff

	return Func

def FitMaxwellianDistE(E,f,n0,T0,mass,Verbose=False,MaxIter=None):

	#select only good data to fit to
	good = np.where(np.isfinite(f) & (f > 0))[0]
	if (good.size < 3.0):
		return -1, -1, False
	Func = _GetMisfitFuncE(E[good],f[good],mass)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0],method='nelder-mead',options=opt)
	#return n,T fitted
	n,t = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad M-B fit')
		print(res.message)
	return n,t,res.success

		
def _GetMisfitFuncCtsE(E,C,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0):
		
	def Func(X):
		n,T = X 
		
		Cm = MaxwellBoltzmannDistCtsE(n,E,T,mass,Eff,dOmega,nSpec,Tau,g)
		
		diff = np.sqrt(np.sum(((C-Cm)**2))/C.size)
		
		return diff

	return Func

def FitMaxwellianDistCtsE(E,Counts,n0,T0,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0,Verbose=False,MaxIter=None):
	
	bad = np.where(np.isfinite(Counts) == False)[0]
	Cs = np.copy(Counts)
	Cs[bad] = 0.0
	

	#select only good data to fit to
	good = np.where((Cs >= 0.0))[0]
	if (good.size < 3.0):
		return -1, -1, False
	Func = _GetMisfitFuncCtsE(E[good],Counts[good],mass,dOmega,Eff,nSpec,Tau,g)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0],method='nelder-mead',options=opt)
	#return n,T fitted
	n,t = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad M-B fit')
		print(res.message)
	return n,t,res.success

