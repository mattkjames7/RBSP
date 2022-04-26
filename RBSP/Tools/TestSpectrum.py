import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from ..ECT.ReadHOPEOmni import ReadHOPEOmni
import DateTimeTools as TT
from . import TestSpec

from scipy.interpolate import interp1d
import pyomnidata
import kpindex
import vsmodel
from .RelVelocity import RelVelocity
from ..Pos.GetVelocity import GetVelocity
from ..Fields.GetData import GetData
from .RelEnergy import RelEnergy
from .MaxwellBoltzmannDist import MaxwellBoltzmannDist
from .IntegrateFluxes import IntegrateFluxesDensity,IntegrateFluxesPressure,IntegrateFluxesTemperature
from .IntegrateSpectrum import IntegrateSpectrum

'''
This file is intended for testing the processes described in Goldstein et al 2019 and Genestreti et al 2016

'''

# rbwdct = {	'red' :	(	(0.0,0.0,0.0),
						# (0.25,0.0,0.0),
						# (0.5,0.0,0.0),
						# (0.75,1.0,1.0),
						# (1.0,1.0,1.0)),
			# 'green' : (	(0.0,0.0,0.0),
						# (0.25,1.0,1.0),
						# (0.5,1.0,1.0),
						# (0.75,1.0,1.0),
						# (1.0,0.0,0.0)),
			# 'blue' : (	(0.0,1.0,1.0),
						# (0.25,1.0,1.0),
						# (0.5,0.0,0.0),
						# (0.75,0.0,0.0),
						# (1.0,0.0,0.0))}
rbwdct = {	'red' :	(	(0.0,0.0,0.0),
						(0.5,0.0,0.0),
						(0.64,1.0,1.0),
						(1.0,1.0,1.0)),
			'green' : (	(0.0,0.0,0.18),
						(0.12,1.0,1.0),
						(0.74,1.0,1.0),
						(1.0,0.0,0.0)),
			'blue' : (	(0.0,1.0,1.0),
						(0.36,1.0,1.0),
						(0.53,0.0,0.0),
						(1.0,0.0,0.0))}

crbw = colors.LinearSegmentedColormap('rbw',rbwdct)

def PlotAdjustedSpectrum(utc,E,S,Vsc,fig=None,maps=[1,1,0,0],scale=None,zlog=True,utcrnge=None,Error=False,zlabel='',yrnge=None,colspan=1,rowspan=1):
	'''
	
	utc : float64
		Continuous time since 1950 in hours
	E : float
		Energy in keV
	S : float
		Spectrogram m^-6 s^3
	Vsc : float
		spacecraft potential V
	
	'''
	
	#calculate the new energy array
	lE = np.log10(E)
	dlE = (lE[:,1:] - lE[:,:-1])/2
	lEe = np.concatenate((np.array([lE[:,0]-dlE[:,0]]).T,lE[:,:-1]+dlE,np.array([lE[:,-1]+dlE[:,-1]]).T),axis=1)
	Ee = 10**lEe
	
	#change units to eV
	Ee = Ee*1000
	
	#adjust the energies due to spacecraft potential
	Ee = (Ee.T + Vsc).T
	
	#Convert PSD to units used in the paper
	#m -> cm (*100)
	#m^6 -> cm^6 (*1e12)
	#m^-6 -> cm^-6 (*1e-12)
	if not Error:
		s = S*1e-12
	else:
		s = S
	
	#work out the time axis
	dt = utc[1:] - utc[:-1]
	ut0 = utc
	ut1 = np.append(utc[:-1] + dt,utc[-1] + dt[-1])
	
	#get the scale
	if scale is None:
		if zlog:
			scale = [np.nanmin(s[s > 0]),np.nanmax(s)]
		else:
			scale = [np.nanmin(s),np.nanmax(s)]
	
	
	#set norm
	if zlog:
		norm = colors.LogNorm(vmin=scale[0],vmax=scale[1])
	else:
		norm = colors.Normalize(vmin=scale[0],vmax=scale[1])	
	

	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]),colspan=colspan,rowspan=rowspan)
	else:
		ax = fig
	
	for i in range(0,utc.size):
		xg,yg = np.meshgrid(np.array([ut0[i],ut1[i]]),Ee[i])
		grid = np.array([s[i]]).T
		sm = ax.pcolormesh(xg,yg,grid,cmap=crbw,norm=norm)

	ax.plot(utc,Ee[:,0],color=[0.0,0.0,0.0],lw=2)

	if not yrnge is None:
		ax.set_ylim(yrnge)

	ax.set_yscale('log')
	if utcrnge is None:
		utcrnge = [utc[0],utc[-1]]
	ax.set_xlim(utcrnge)
	TT.DTPlotLabel(ax,TickFreq='auto')

	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.05)

	cbar = plt.colorbar(sm,cax=cax) 
	cbar.set_label(zlabel)
	
	return ax
	
def _SCVel(utc,sc):
	vel = GetVelocity(sc,'SM')
	fuscx = interp1d(vel.utc,vel.Vx,bounds_error=False)
	fuscy = interp1d(vel.utc,vel.Vy,bounds_error=False)
	fuscz = interp1d(vel.utc,vel.Vz,bounds_error=False)
	fscx = interp1d(vel.utc,vel.x,bounds_error=False)
	fscy = interp1d(vel.utc,vel.y,bounds_error=False)
	fscz = interp1d(vel.utc,vel.z,bounds_error=False)
	psc = np.array([fscx(utc),fscy(utc),fscz(utc)])
	usc = np.array([fuscx(utc),fuscy(utc),fuscz(utc)])
	
	return psc,usc	
	
def _ExBDrift(utc,psc,sc):
	
	#kp index
	Date,ut = TT.ContUTtoDate(utc)
	kp = kpindex.GetKp(Date)
	utc0 = TT.ContUT(kp.Date,kp.ut0)
	# utc1 = TT.ContUT(kp.Date,kp.ut1)
	# kutc = np.append(utc0,utc1)
	# kpi = np.append(kp.Kp,kp.Kp)
	# srt = np.argsort(kutc)
	# kutc = kutc[srt]
	# kpi = kpi[srt]
	# fkp = interp1d(kutc,kpi,bounds_error=False,fill_value=np.nan)
	# k = fkp(utc)
	use = np.where(utc0 <= utc)[0][-1]
	k = kp.Kp[use]
	print('Kp : ',k)

	#Solar wind electric field
	#get the electric field data
	odata = pyomnidata.GetOMNI(Date//10000)
	good = np.where(np.isfinite(odata.E))[0]
	Vsw = odata.FlowSpeed
	Bz = odata.BzGSM
	E = -Bz*1e-9*Vsw*1e3
	
	fE = interp1d(odata.utc[good],E[good],bounds_error=False,fill_value=np.nan)
	Esw = fE(utc).clip(min=0.25)
	print('Esw (mV/m): ',Esw)
	
	#get magnetic field
	fdata = GetData(Date,sc=sc)
	fbx = interp1d(fdata.utc,fdata.BxSM)
	fby = interp1d(fdata.utc,fdata.BySM)
	fbz = interp1d(fdata.utc,fdata.BzSM)
	
	Bx,By,Bz = np.array([fbx(utc),fby(utc),fbz(utc)])*1e-9
	print('B (T): ',Bx,By,Bz)
	
	#get the vsmodel 
	Ex,Ey,Ez = np.array(vsmodel.ModelECart(psc[0],psc[1],k,Esw))*1e-3
	print('E (V/m): ',Ex,Ey,Ez)
	
	#get the drift velocity
	Vx,Vy,Vz = vsmodel.VExB(Ex,Ey,Ez,Bx,By,Bz)
	print('ExB Velocity (m/s): ',Vx,Vy,Vz)
	
	return Vx,Vy,Vz
	
	
def PlotSpectrum(E,psd,Flux,err,utc,Mass,sc='a',vrnge=None,prnge=None,fig=None,maps=[1,1,0,0],Tpaper=None,npaper=None,colspan=1,rowspan=1):
	'''
	E : float
		Energy in keV (not adjusted for spacecraft velocity etc)
	psd : float
		phase space density in m^-6 s^3
	err : float
		Poisson error
	utc : float64
		time of spectrum
	
	'''
	from ..EFW.GetPotential import GetPotential
	e = 1.602e-19
	kB = 1.381e-23

	Date,ut = TT.ContUTtoDate(utc)
	Date = Date[0]
	ut= ut[0]
	
	#convert PSD to cm^-6 s^3
	p = psd*1e-12
	
	#get Vsc
	pot = GetPotential(Date,'a')
	
	#interpolate so it uses the same time axis
	fVsc = interp1d(pot.utc,pot.Vsc,bounds_error=False)
	Vsc = np.abs(fVsc(utc))
	
	#integrate spectrum to get PEND density
	lE = np.log10(E)
	dlE = (lE[1:] - lE[:-1])/2
	lE0 = np.append(lE[0]-dlE[0],lE[:-1]+dlE)
	lE1 = np.append(lE[:-1]+dlE,lE[-1]+dlE[-1])
	E0 = 10**lE0
	E1 = 10**lE1

	nPEND = IntegrateFluxes(np.array([E]),np.array([E0]),np.array([E1]),np.array([Flux]),Mass,4*np.pi,Vsc,Erange=(0.0,0.02))[0]
	pPEND = IntegrateFluxesPressure(np.array([E]),np.array([E0]),np.array([E1]),np.array([Flux]),Mass,4*np.pi,Vsc,Erange=(0.0,0.02))[0]
	TPEND = IntegrateFluxesTemperature(np.array([E]),np.array([E0]),np.array([E1]),np.array([Flux]),Mass,4*np.pi,Vsc,Erange=(0.0,0.02))[0]
	print('n_PEND (cm^-3) : ',nPEND)
	print('p_PEND (Pa) : ',pPEND)
	print('T_PEND (K) : ',TPEND)
	print('T_PEND (eV) : ',TPEND*kB/e)
	nInt = IntegrateSpectrum(E,psd,Mass,4*np.pi)[0]
	print('n_Int (cm^-3) : ',nInt)

	n30 = IntegrateFluxes(E,E0,E1,Flux,Mass,4*np.pi,Vsc,Erange=(0.03,np.inf))[0]
	p30 = IntegrateFluxesPressure(E,E0,E1,Flux,Mass,4*np.pi,Vsc,Erange=(0.03,np.inf))[0]
	T30 = IntegrateFluxesTemperature(E,E0,E1,Flux,Mass,4*np.pi,Vsc,Erange=(0.03,np.inf))[0]
	print('n_30 (cm^-3) : ',n30)
	print('p_30 (Pa) : ',p30)
	print('T_30 (K) : ',T30)
	print('T_30 (eV) : ',T30*kB/e)
	nInt = IntegrateSpectrum(E,psd,Mass,4*np.pi)[0]
	print('n_Int (cm^-3) : ',nInt)
	
	#get spacecraft velocity and position
	psc,usc = _SCVel(utc,sc)
	print('Spacecraft pos (Re): ',*psc)
	print('Spacecraft vel (m/s): ',*usc)
	
	#get ExB drift
	exb = _ExBDrift(utc,psc,sc)
	Vexb = np.linalg.norm(exb)
	
	#get two versions of the effective velocity
	ueff = np.linalg.norm(usc - exb)
	ueff1 = np.abs(np.linalg.norm(usc) + np.linalg.norm(exb))
	print('u_eff (m/s) : ',ueff)
	print('u_eff (dodgy) (m/s) : ',ueff1)
	
	#calculate Bulk velocity etc
	Ebulk = RelEnergy(ueff,Mass)/1000.0
	Ebulk3 = Ebulk*3
	vmax = RelVelocity(Ebulk3*1000.0,Mass)
	print('Ebulk (eV): ',Ebulk)
	print('Emax (eV): ',Ebulk3)
	print('Vmax (m/s): ',vmax)
	
	#shift energy due to Vsc
	E += (Vsc/1000.0)
	
	#convert energy to velocity
	v = RelVelocity(E,Mass)
	
	#(don't!) subtract the spacecraft velocity
	#v -= ueff0
	
	#convert velocity to km/s
	vk = v/1000.0
	
	#error
	dp = p*err
	
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]),colspan=colspan,rowspan=rowspan)
	else:
		ax = fig	
	
	ax.errorbar(vk,p,yerr=dp,color='k',linestyle='',marker='x')
	ax.set_yscale('log')
	ax.set_xscale('log')
	
	R = ax.axis()

	if not vrnge is None:
		ax.set_xlim(vrnge)
	else:
		ax.set_xlim(R[0],R[1])
	
	if not prnge is None:
		ax.set_ylim(prnge)
	else:
		ax.set_ylim(R[2],R[3])
		
	R = ax.axis()
	#plot Vbulk (ueff)
	ax.plot([ueff/1000.0,ueff/1000.0],[R[2],R[3]],color=[0.0,0.0,1.0],lw=2)
	ax.plot([3*ueff/1000.0,3*ueff/1000.0],[R[2],R[3]],color=[0.0,0.0,1.0],lw=2,linestyle=':')
	ax.plot([vmax/1000.0,vmax/1000.0],[R[2],R[3]],color=[0.0,0.0,1.0],lw=2,linestyle='--')
		
	if not Tpaper is None and not npaper is None:

		#convert T from eV to K
		Ej = Tpaper*e
		Tpaperk = Ej/kB
		#convert density from cm^-3 to m^-3
		npaperm = 1e6*npaper

		ppaper = npaperm*Ej
		print('paper n (cm^-3) : ',npaper)
		print('paper T (eV) (',Tpaper,') -> (K) (',Tpaperk,')')
		print('paper p (Pa) : ',ppaper)
		

		
		#get the psd
		xlim = np.array(ax.get_xlim())
		xl = np.log10(xlim)
		vp = 10**np.linspace(xl[0],xl[1],1000)
		print(vp[0],vp[-1])
		fpaper = MaxwellBoltzmannDist(npaperm,vp*1000-ueff,Tpaperk,Mass)/(4*np.pi) #what is this factor of 10 or 4*pi?
		
		Ep = RelEnergy(vp*1000.0,Mass)
		nIntp = IntegrateSpectrum(Ep,fpaper,Mass,4*np.pi)
		print('n_Int (cm^-3) : ',nIntp)
		
		#convert to the psd units used in the paper
		fpaper = fpaper*1e-12
		print(fpaper[0],fpaper[-1])
		#vp += (ueff/1000.0)
		print(vp[0],vp[-1])
		ax.plot(vp,fpaper,color=[1.0,0.0,0.0])
		
	h,m,s,_ = TT.DectoHHMM(ut)
	title = '{:08d} - {:02d}:{:02d}:{:02d}'.format(Date,h[0],m[0],s[0])
	ax.set_title(title)
	
	ax.set_xlabel('Effective Velocity (km/s)')
	ax.set_aspect('auto')
	return ax
	
def G16F3c(fig=None,maps=[1,1,0,0],colspan=1,rowspan=1):
	
	
	#work out the time
	Date = 20130115
	ut = 11.0 + 1/60.0 + 17/3600.0
	utc = TT.ContUT(Date,ut)[0]
		
	if TestSpec.data is None:
		print('Reading data')
		TestSpec.data = ReadHOPEOmni(Date,'a')
	#get protons
	sh = TestSpec.data['H+Flux']

	
	#now the spectrum
	E,psd,err,_ = sh.GetSpectrum(Date,ut,yparam='PSD',xparam='E')
	_,Flux,_,_ = sh.GetSpectrum(Date,ut,yparam='Flux',xparam='E')
	
	#plot
	ax = PlotSpectrum(E,psd,Flux,err,utc,sh.Mass,fig=fig,maps=maps,npaper=501.0,Tpaper=0.251,vrnge=[1.0,1e4],prnge=[1e-32,1e-15],colspan=colspan,rowspan=rowspan)

def G16F3d(fig=None,maps=[1,1,0,0],colspan=1,rowspan=1):
	
	
	#work out the time
	Date = 20130115
	ut = 11.0 + 30/60.0 + 2/3600.0
	utc = TT.ContUT(Date,ut)[0]
		
	if TestSpec.data is None:
		print('Reading data')
		TestSpec.data = ReadHOPEOmni(Date,'a')
	#get protons
	sh = TestSpec.data['H+Flux']

	
	#now the spectrum
	E,psd,err,_ = sh.GetSpectrum(Date,ut,yparam='PSD',xparam='E')
	_,Flux,_,_ = sh.GetSpectrum(Date,ut,yparam='Flux',xparam='E')
	
	#plot
	ax = PlotSpectrum(E,psd,Flux,err,utc,sh.Mass,fig=fig,maps=maps,npaper=37.0,Tpaper=0.265,vrnge=[1.0,1e4],prnge=[1e-32,1e-15],colspan=colspan,rowspan=rowspan)

def G16F3e(fig=None,maps=[1,1,0,0],colspan=1,rowspan=1):
	
	
	#work out the time
	Date = 20130115
	ut = 12.0 + 0/60.0 + 41/3600.0
	utc = TT.ContUT(Date,ut)[0]
		
	if TestSpec.data is None:
		print('Reading data')
		TestSpec.data = ReadHOPEOmni(Date,'a')
	#get protons
	sh = TestSpec.data['H+Flux']

	
	#now the spectrum
	E,psd,err,_ = sh.GetSpectrum(Date,ut,yparam='PSD',xparam='E')
	_,Flux,_,_ = sh.GetSpectrum(Date,ut,yparam='Flux',xparam='E')
	
	#plot
	ax = PlotSpectrum(E,psd,Flux,err,utc,sh.Mass,fig=fig,maps=maps,npaper=94.0,Tpaper=0.43,vrnge=[1.0,1e4],prnge=[1e-32,1e-15],colspan=colspan,rowspan=rowspan)

def G16F3f(fig=None,maps=[1,1,0,0],colspan=1,rowspan=1):
	
	
	#work out the time
	Date = 20130115
	ut = 12.0 + 29/60.0 + 48/3600.0
	utc = TT.ContUT(Date,ut)[0]
		
	if TestSpec.data is None:
		print('Reading data')
		TestSpec.data = ReadHOPEOmni(Date,'a')
	#get protons
	sh = TestSpec.data['H+Flux']

	
	#now the spectrum
	E,psd,err,_ = sh.GetSpectrum(Date,ut,yparam='PSD',xparam='E')
	_,Flux,_,_ = sh.GetSpectrum(Date,ut,yparam='Flux',xparam='E')
	
	#plot
	ax = PlotSpectrum(E,psd,Flux,err,utc,sh.Mass,fig=fig,maps=maps,npaper=19.0,Tpaper=1.48,vrnge=[1.0,1e4],prnge=[1e-32,1e-15],colspan=colspan,rowspan=rowspan)
	ax.set_ylabel('PSD (cm$^{-6}$ s$^{3}$)')

def G16F3a(fig=None,maps=[1,1,0,0],colspan=1,rowspan=1):
	Date = 20130115
	utr = [11.0,12.5]
	utcr = TT.ContUT([Date,Date],utr)
	
	#get the data in first
	if TestSpec.data is None:
		print('Reading data')
		TestSpec.data = ReadHOPEOmni(Date,'a')
	spec = TestSpec.data
	sh = spec['H+Flux']	

	#get the spacecraft potential
	date0 = TT.MinusDay(Date)
	date1 = TT.PlusDay(Date)
	pot = GetPotential([date0,date1],'a')
	
	#interpolate so it uses the same time axis
	fVsc = interp1d(pot.utc,pot.Vsc,bounds_error=False)
	Vsc = np.abs(fVsc(sh.utc[0]))	
	
	#plot Hydrogen
	PlotAdjustedSpectrum(sh.utc[0],sh.Energy[0],sh.PSD[0],Vsc,scale=[5.6e-32,1.7e-17],utcrnge=utcr,fig=fig,maps=maps,yrnge=[1.0,5e4],zlabel='(s$^{3}$ cm$^{-6}$)',colspan=colspan,rowspan=rowspan)

def G16F3b(fig=None,maps=[1,1,0,0],colspan=1,rowspan=1):
	Date = 20130115
	utr = [11.0,12.5]
	utcr = TT.ContUT([Date,Date],utr)
	
	#get the data in first
	if TestSpec.data is None:
		print('Reading data')
		TestSpec.data = ReadHOPEOmni(Date,'a')
	spec = TestSpec.data
	sh = spec['H+Flux']	

	#get the spacecraft potential
	date0 = TT.MinusDay(Date)
	date1 = TT.PlusDay(Date)
	pot = GetPotential([date0,date1],'a')
	
	#interpolate so it uses the same time axis
	fVsc = interp1d(pot.utc,pot.Vsc,bounds_error=False)
	Vsc = np.abs(fVsc(sh.utc[0]))	
	
	#plot Hydrogen
	PlotAdjustedSpectrum(sh.utc[0],sh.Energy[0],sh.Errors[0],Vsc,scale=[0.0,1.5],utcrnge=utcr,fig=fig,maps=maps,yrnge=[1.0,5e4],Error=True,zlog=False,zlabel='Counts$^{-1/2}$',colspan=colspan,rowspan=rowspan)
	
def G16F3():
	fig = plt
	fig.figure(figsize=(18,6))
	
	G16F3a(fig,[11,4,0,0],rowspan=2,colspan=3)
	G16F3b(fig,[11,4,0,2],rowspan=2,colspan=3)
	G16F3c(fig,[11,4,3,1],colspan=2,rowspan=2)
	G16F3d(fig,[11,4,5,1],colspan=2,rowspan=2)
	G16F3e(fig,[11,4,7,1],colspan=2,rowspan=2)
	G16F3f(fig,[11,4,9,1],colspan=2,rowspan=2)
	plt.subplots_adjust(wspace=1.0,left=0.05,right=0.95)

def G16F2():
	'''
	Reproduce the figure 2 created in Genestreti et al 2016
	
	'''
	Date = 20130115
	utr = [2.5,19.0]
	utcr = TT.ContUT([Date,Date],utr)
	
	#get the data in first
	if TestSpec.data is None:
		print('Reading data')
		TestSpec.data = ReadHOPEOmni(Date,'a')
	spec = TestSpec.data
	sh = spec['H+Flux']
	she = spec['He+Flux']
	so = spec['O+Flux']
		
	#get the spacecraft potential
	date0 = TT.MinusDay(Date)
	date1 = TT.PlusDay(Date)
	pot = GetPotential([date0,date1],'a')
	
	#interpolate so it uses the same time axis
	fVsc = interp1d(pot.utc,pot.Vsc,bounds_error=False)
	Vsc = np.abs(fVsc(sh.utc[0]))
	
	#create figure
	fig = plt
	plt.figure(figsize=(8,11))
	
	#plot Hydrogen
	PlotAdjustedSpectrum(sh.utc[0],sh.Energy[0],sh.PSD[0],Vsc,scale=[8.2e-32,2.8e-17],utcrnge=utcr,fig=fig,maps=[1,10,0,0])
	
	#plot Helium
	PlotAdjustedSpectrum(she.utc[0],she.Energy[0],she.PSD[0],Vsc,scale=[1.2e-30,3.0e-17],utcrnge=utcr,fig=fig,maps=[1,10,0,1])
	
	#plot Oxygen
	PlotAdjustedSpectrum(so.utc[0],so.Energy[0],so.PSD[0],Vsc,scale=[1.5e-29,1.0e-15],utcrnge=utcr,fig=fig,maps=[1,10,0,2])

	#plot density
	
	#plot n ratio
	
	#plot T
	
	#plot T ratio
	
	#plot spacecraft potential
	ax = fig.subplot2grid((20,1),(18,0))
	ax.plot(pot.utc,np.abs(pot.Vsc),color='k')
	ax.set_xlim(utcr)
	ax.set_ylim(0,6)
	ax.set_xticks([])
	
	#plot Esw
	import pyomnidata
	odata = pyomnidata.GetOMNI(Date//10000,Res=1)
	use = np.where((odata.utc >= utcr[0]) & (odata.utc <= utcr[1]))[0]
	odata = odata[use]
	Vsw = -odata.FlowSpeed
	Bz = odata.BzGSM
	Esw = (np.float64(Bz*1e-9)*np.float64(Vsw*1e6)).clip(min=0.1)
	
	
	#Esw = odata.E.clip(min=0.1)
	ax = fig.subplot2grid((20,1),(19,0))
	ax.plot(odata.utc,Esw,color='k')
	ax.set_xlim(utcr)
	ax.set_ylim(0,10)
	TT.DTPlotLabel(ax)	
	
	
