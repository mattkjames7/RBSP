import numpy as np
from .KappaDist import KappaDist,KappaDistCts
from .KappaDist import KappaDistE,KappaDistCtsE
from scipy.optimize import minimize

def _GetMisfitFunc(v,f,mass):
	
	def Func(X):
		n,T,K = X 
		
		fk = KappaDist(n,v,T,mass,K)
		#if np.isnan(fk[0]):
	#		print(n,T,K,fk)
		lf = np.log10(f)
		lk = np.log10(fk)
		diff = np.sqrt(np.sum(((lf-lk)**2))/f.size)
		
		return diff

	return Func

def FitKappaDist(v,f,n0,T0,mass,Verbose=False,MaxIter=None):
	

	#select only good data to fit to
	good = np.where(np.isfinite(f) & (f > 0))[0]
	if (good.size < 3.0):
		return -1, -1, -1, False
	Func = _GetMisfitFunc(v[good],f[good],mass)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0,5.0],method='nelder-mead',options=opt)
	n,t,k = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad Kappa fit')
		print(res.message)
	#return n,T and Kappa fitted
	return n,t,k,res.success

def _GetMisfitFuncCts(v,C,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0):
		
	def Func(X):
		n,T,K = X 
		Cm = KappaDistCts(n,v,T,mass,K,Eff,dOmega,nSpec,Tau,g)
		
		diff = np.sqrt(np.sum(((C-Cm)**2))/C.size)

		return diff

	return Func

def FitKappaDistCts(v,Counts,n0,T0,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0,Verbose=False,MaxIter=None):
	
	bad = np.where(np.isfinite(Counts) == False)[0]
	Cs = np.copy(Counts)
	Cs[bad] = 0.0
	

	#select only good data to fit to
	good = np.where((Cs >= 0.0))[0]
	if (good.size < 3.0):
		return -1, -1, -1, False
	Func = _GetMisfitFuncCts(v[good],Cs[good],mass,dOmega,Eff,nSpec,Tau,g)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0,5.0],method='nelder-mead',options=opt)
	n,t,k = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad Kappa fit')
		print(res.message)
	#return n,T fitted
	return n,t,k,res.success
		

def _GetMisfitFuncE(E,f,mass):
	
	def Func(X):
		n,T,K = X 
		
		fk = KappaDistE(n,E,T,mass,K)
		#if np.isnan(fk[0]):
	#		print(n,T,K,fk)
		lf = np.log10(f)
		lk = np.log10(fk)
		diff = np.sqrt(np.sum(((lf-lk)**2))/f.size)
		
		return diff

	return Func

def FitKappaDistE(E,f,n0,T0,mass,Verbose=False,MaxIter=None):
	

	#select only good data to fit to
	good = np.where(np.isfinite(f) & (f > 0))[0]
	if (good.size < 3.0):
		return -1, -1, -1, False
	Func = _GetMisfitFuncE(E[good],f[good],mass)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0,5.0],method='nelder-mead',options=opt)
	n,t,k = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad Kappa fit')
		print(res.message)
	#return n,T and Kappa fitted
	return n,t,k,res.success

def _GetMisfitFuncCtsE(E,C,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0):
		
	def Func(X):
		n,T,K = X 
		Cm = KappaDistCtsE(n,E,T,mass,K,Eff,dOmega,nSpec,Tau,g)
		
		diff = np.sqrt(np.sum(((C-Cm)**2))/C.size)

		return diff

	return Func

def FitKappaDistCtsE(E,Counts,n0,T0,mass,dOmega=1.0,Eff=1.0,nSpec=1.0,Tau=1.0,g=1.0,Verbose=False,MaxIter=None):
	
	bad = np.where(np.isfinite(Counts) == False)[0]
	Cs = np.copy(Counts)
	Cs[bad] = 0.0
	

	#select only good data to fit to
	good = np.where((Cs >= 0.0))[0]
	if (good.size < 3.0):
		return -1, -1, -1, False
	Func = _GetMisfitFuncCtsE(E[good],Cs[good],mass,dOmega,Eff,nSpec,Tau,g)
	if MaxIter is None:
		opt = {}
	else:
		opt = { 'maxiter' : MaxIter }
	res = minimize(Func,[n0,T0,5.0],method='nelder-mead',options=opt)
	n,t,k = res.x
	if not res.success and Verbose:
		print('Warning - potentially bad Kappa fit')
		print(res.message)
	#return n,T fitted
	return n,t,k,res.success
		
