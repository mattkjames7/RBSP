import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import DateTimeTools as TT
from .PosDTPlotLabel import PosDTPlotLabel
from scipy.interpolate import interp1d
from .PSDtoCounts import PSDtoCounts,PSDtoCountsE
from .PSDtoFlux import PSDtoFlux,PSDtoFluxE
from .CountstoFlux import CountstoFlux,CountstoFluxE
from .CountstoPSD import CountstoPSD,CountstoPSDE
from .FitMaxwellianDist import FitMaxwellianDistCtsE,FitMaxwellianDistE
from .FitKappaDist import FitKappaDistCtsE,FitKappaDistE
from .KappaDist import KappaDistE
from .MaxwellBoltzmannDist import MaxwellBoltzmannDistE
from ..Pos.ReadFieldTraces import ReadFieldTraces
from .RelVelocity import RelVelocity
from .IntegrateSpectrum import IntegrateSpectrum
from .. import ECT
from .RelEnergy import RelEnergy

defargs = {	'Meta' : None,
			'dt' : None,
			'ew' : None,
			'xlabel' : 'UT',
			'ylabele' : 'Energy, (keV)',
			'ylabelv' : 'V (m s$^{-1}$)',
			'zlabelf' : 'Flux (s cm$^{2}$ sr keV)$^{-1}$',
			'zlabelp' : 'PSD (s$^3$ m$^{-6}$)',
			'ylog' : False,
			'zlog' : False, 
			'ScaleType' : 'range',
			'nStd' : 2}

amu = 1.6605e-27

ParticleMass = { 	'e' : 9.10938356e-31,
					'H' : 1.6726219e-27,
					'He' : 4.002602*amu,
					'O' : 15.999*amu,
					'O2' : 15.999*amu*2}

class PSpecCls(object):
	def __init__(self,SpecType='e',**kwargs):
		'''
		An object for storing and plotting particle spectral data.
		
		See SpecCls.Plot, SpecCls.PlotSpectrum and SpecCls.GetSpectrum
		for more information.
		
		Inputs
		=====
		SpecType : str
			'e'|'H'|'He'|'O'|'O2'
		xlabel : str
			Label for x-axis
		ylabel : str
			Label for y-axis
		zlabel : str
			Label for color scale
		ylog : bool
			True for logarithmic y-axis
		zlog : bool
			True for logarithmic color scale
		
		'''
		
		#create lists to store the input variables
		self.Date = []
		self.ut = []
		self.Epoch = []
		self.E0 = []
		self.E1 = []
		self.Energy = []
		self.Spec = []
		self.utc = []
		self.dt = []
		self.Meta = []
		self.Label = []
		self.V = []
		self.V0 = []
		self.V1 = []
		self.PSD = []
		self.Mass = ParticleMass.get(SpecType,9.10938356e-31)
		self.Omega = []
		self.density = []
		self.Moments = []
		self.n = 0
		self.SpecType = SpecType
		
		#and the keywords
		self.xlabel = kwargs.get('xlabel',defargs['xlabel'])
		self.ylabele = kwargs.get('ylabele',defargs['ylabele'])
		self.ylabelv = kwargs.get('ylabelv',defargs['ylabelv'])
		self.zlabelf = kwargs.get('zlabelf',defargs['zlabelf'])
		self.zlabelp = kwargs.get('zlabelp',defargs['zlabelp'])
		self._ylog = kwargs.get('ylog',defargs['ylog'])
		self._zlog = kwargs.get('zlog',defargs['zlog'])
		self._ScaleType = kwargs.get('ScaleType',defargs['ScaleType'])
		self._nStd = kwargs.get('nStd',defargs['nStd'])
		
			

		
	def _ProcessDT(self,dt,ut):
		#set the interval between each measurement (assuming ut is start 
		#of interval and that ut + dt is the end
		if dt is None:
			dt = (ut[1:] - ut[:-1])
			u,c = np.unique(dt,return_counts=True)
			dt = u[np.where(c == c.max())[0][0]]
		
		#convert it to an array the same length as ut
		dt = np.zeros(ut.size,dtype='float32') + dt
		return dt
		
	def _CalculatePSD(self,Spec,Energy):
		e = 1.6022e-19
		psd =  np.float64(Spec)*(np.float64(self.Mass)/(2000*e*np.float64(Energy/self.Mass))) * np.float64(10.0/e)
		#psd = np.float64(self.Mass/(2*Energy)) * np.float64(Spec)
		self.PSD.append(psd)
		
	def _CalculateV(self,E0,E1,Emid):
		V = RelVelocity(Emid,self.Mass)
		V0 = RelVelocity(E0,self.Mass)
		V1 = RelVelocity(E1,self.Mass)
		self.V.append(V)
		self.V0.append(V0)
		self.V1.append(V1)		
		
	def _IntegrateSpectra(self,E,PSD,Omega):
		if self.SpecType == 'e':
			Erange = (0.2,np.inf)
		else:
			Erange = (0.03,np.inf)
		self.density.append(IntegrateSpectrum(E,PSD,self.Mass,Omega,Erange))			
	
	def AddData(self,Date,ut,Epoch,E0,E1,Emid,Spec,dt=None,Meta=None,Omega=4*np.pi,Label='',Moments=None):
		'''
		Adds data to the object
		
		Inputs
		======
		Date : int
			Array of dates in format yyyymmdd
		ut : float
			Array of times since beginning of the day
		Epoch : float
			CDF epoch 
		Energy : float
			An array of energy bins
		Spec : float
			2D array containing the spectral data, shape (nt,nf) where
			nt is ut.size and nf is Energy.size
		dt : None or float
			duration of each spectrum
		Meta : dict
			Meta data from CDF - not used
		Label : str
			String containing a plot label if desired
		'''

		#store the input variables by appending to the existing lists
		self.Date.append(Date)
		self.ut.append(ut)
		self.Epoch.append(Epoch)
		self.Spec.append(Spec)		
		self.Meta.append(Meta)
		self.Label.append(Label)
		self.Omega.append(Omega)
		self.Moments.append(Moments)
	
		#separate energy bins into lower, uppwer and middle
		self.E0.append(E0)
		self.E1.append(E1)
		self.Energy.append(Emid)

		#calculate the Phase Space Density
		self._CalculatePSD(Spec,Emid)
		
		#calculate velocities
		self._CalculateV(E0,E1,Emid)
		
		#calculate integrated densities
		self._IntegrateSpectra(Emid,self.PSD[-1],Omega)
		
		#calculate continuous time axis
		self.utc.append(TT.ContUT(Date,ut))
		
		#calculate dt
		self.dt.append(self._ProcessDT(dt,ut))

		#calculate the new time, energy and z scale limits
		self._CalculateTimeLimits() 
		self._CalculateEnergyLimits()
		self._CalculateScale()
		self._CalculateVLimits()
		self._CalculatePSDScale()
		
		#add to the total count of spectrograms stored
		self.n += 1
	
	def _GetSpectrum(self,I,sutc,dutc,Method,xparam,yparam):
	
		#get the appropriate data
		l = self.Label[I]
		utc = self.utc[I]
		if xparam == 'V':
			f = self.V[I]
		else:
			f = self.Energy[I]
			
		if yparam == 'PSD':
			Spec = self.PSD[I]		
		else:
			Spec = self.Spec[I]		
		
		#find the nearest
		dt = np.abs(utc - sutc)
		near = np.where(dt == dt.min())[0][0]
		
		#check if the nearest is within dutc
		if dt[near] > dutc:
			return [],[],[]
			
		
		#check if we are past the end of the time series, or Method is nearest
		if (Method == 'nearest') or (sutc < utc[0]) or (sutc > utc[-1]):
			s = Spec[near,:]
			if len(f.shape) == 2:
				e = f[near,:]
			else:
				e = f
			
		else:
			#in this case we need to find the two surrounding neighbours
			#and interpolate between them
			bef = np.where(utc <= sutc)[0][-1]
			aft = np.where(utc > sutc)[0][0]
			
			s0 = Spec[bef,:]
			s1 = Spec[aft,:]
			
			if len(f.shape) == 2:
				e0 = f[near,:]
				e1 = f[near,:]
			else:
				e0 = f
				e1 = f
			
			dx = utc[aft] - utc[bef]
			ds = s1 - s0
			de = e1 - e0
			
			dsdx = ds/dx
			dedx = de/dx
			
			dt = sutc - utc[bef]
			
			s = s0 + dt*dsdx
			e = e0 + dt*dedx
		
		
		#remove rubbish
		good = np.where(e > 0)[0]
		e = e[good]
		s = s[good]
			
		#sort by e
		srt = np.argsort(e)
		e = e[srt]
		s = s[srt]
		return e,s,l
		
	def _GetMoment(self,I,sutc,dutc):
	
		#get the appropriate data
		mom = self.Moments[I]
		
		#find the nearest
		dt = np.abs(mom.utc - sutc)
		near = np.where(dt == dt.min())[0][0]
		
		#check if the nearest is within dutc
		if dt[near] > dutc:
			return None
		else:
			return near
		

	
	def GetSpectrum(self,Date,ut,Method='nearest',Maxdt=60.0,Split=False,xparam='E',yparam='Flux'):
		'''
		This method will return a spectrum from a given time.
		
		Inputs
		======
		Date : int
			Date in format yyyymmdd
		ut : float
			Time in hours since beginning of the day
		Method : str
			'nearest'|'interpolate' - will find the nearest spectrum to
			the time specified time, or will interpolate between two 
			surrounding spectra.
		Maxdt : float
			Maximum difference in time between the specified time and the
			time of the spectra in seconds.
		Split : bool
			If True, the spectra will be returned as a list, if False,
			they will be combined to form a single spectrum.
		xparam : str
			Sets the x-axis of the returned spectrum to be either energy
			(keV) or velocity (m/s): 'E'|'V'
		yparam : str
			Sets the type of spectrum output to either differential
			energy flux or phase space density: 'Flux'|'PSD'
		
		Returns
		=======
		energy : float/list
			Array(s) of energies or velocities
		spec : float/list
			Array(s) containing specral data
		labs : list
			List of plot labels
		
		'''
	
		#convert to continuous time
		utc = TT.ContUT(np.array([Date]),np.array([ut]))[0]
		dutc = Maxdt/3600.0
		
		#create the objects to store spectra and energy bins
		spec = []
		energy = []
		labs = []
		
		#get the spectra for each element in  self.Spec
		for i in range(0,self.n):
			e,s,l = self._GetSpectrum(i,utc,dutc,Method,xparam,yparam)
			if len(s) > 0:
				spec.append(s)
				energy.append(e)
				labs.append(l)
			
		#combine if necessary
		if not Split:
			spec = np.concatenate(spec)
			energy = np.concatenate(energy)
			srt = np.argsort(energy)
			spec = spec[srt]
			energy = energy[srt]
			
		return energy,spec,labs
		
	def GetMoments(self,Date,ut,Maxdt=60.0):
		'''
		This method will return a spectrum from a given time.
		
		Inputs
		======
		Date : int
			Date in format yyyymmdd
		ut : float
			Time in hours since beginning of the day
		Maxdt : float
			Maximum difference in time between the specified time and the
			time of the spectra in seconds.

		Returns
		=======
		moment : numpy.recarray
			Element(s) of a numpy recarray with the dtype provided in 
			RBSP.ECT._ECT.mdtype which contains number densities in cm^-3
			and temperatures in MK.
		
		'''
	
		#convert to continuous time
		utc = TT.ContUT(np.array([Date]),np.array([ut]))[0]
		dutc = Maxdt/3600.0
		
		#create the objects to store spectra and energy bins
		ind0 = []
		ind1 = []
		
		#get the spectra for each element in  self.Spec
		for i in range(0,self.n):
			tmp = self._GetMoment(i,utc,dutc)
			if not tmp is None:
				ind0.append(i)
				ind1.append(tmp)
			
		#create recarray
		ind0 = np.array(ind0)
		ind1 = np.array(ind1)
		if ind0.size > 0:
			moment = np.recarray(ind0.size,dtype=ECT._ECT.mdtype)
			for i in range(0,ind0.size):
				moment[i] = self.Moments[ind0[i]][ind1[i]]
		else:
			moment = np.recarray(0,dtype=ECT._ECT.mdtype)
		
		return moment
		
	def PlotSpectrum(self,Date,ut,Method='nearest',Maxdt=60.0,Split=False,
		fig=None,maps=[1,1,0,0],color=None,xlog=True,ylog=None,xparam='E',yparam='Flux',
		FitKappa=False,FitMaxwellian=False,nox=False,noy=False,Erange=(0.0,np.inf),
		MaxIter=None,n0=10.0,T0=100.0,Integrate=False,ShowMoments=False):
		'''
		This method will plot a spectrum from a given time.
		
		Inputs
		======
		Date : int
			Date in format yyyymmdd
		ut : float
			Time in hours since beginning of the day
		Method : str
			'nearest'|'interpolate' - will find the nearest spectrum to
			the time specified time, or will interpolate between two 
			surrounding spectra.
		Maxdt : float
			Maximum difference in time between the specified time and the
			time of the spectra in seconds.
		Split : bool
			If True, the spectra will be returned as a list, if False,
			they will be combined to form a single spectrum.
		xparam : str
			Sets the x-axis of the returned spectrum to be either energy
			(keV) or velocity (m/s): 'E'|'V'
		yparam : str
			Sets the type of spectrum output to either differential
			energy flux or phase space density: 'Flux'|'PSD'
		fig : None, matplotlib.pyplot or matplotlib.pyplot.Axes instance
			If None - a new plot is created
			If an instance of pyplot then a new Axes is created on an existing plot
			If Axes instance, then plotting is done on existing Axes
		maps : list
			[xmaps,ymaps,xmap,ymap] controls position of subplot
		xlog : bool
			if True, x-axis is logarithmic
		ylog : bool
			If True, y-axis is logarithmic
		FitMaxwellian : bool or str
			If True - the PSD will be used to fit a Maxwellian 
			distribution, if 'counts' then the counts will be used 
			instead.
		FitKappa : bool or str
			If True - the PSD will be used to fit a Kappa
			distribution, if 'counts' then the counts will be used 
			instead.		
		Erange : tuple
			Minimum and maximum energy to fit distribution function 
			against (keV)
		MaxIter : None,int
			Maximum number of iterations for the spectrum fitting.
		n0 : float
			Initial density required for the spectral fitting (cm^-3).
		T0 : float
			Initial temperature for fitting spectrum (MK).
				
		'''	
		
		#get the spectra
		energy,spec,labs = self.GetSpectrum(Date,ut,Method,Maxdt,Split,xparam,yparam)
		
		
		#create the figure
		if fig is None:
			fig = plt
			fig.figure()
		if hasattr(fig,'Axes'):	
			ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		else:
			ax = fig	
			
		#plot
		if Split:
			if not color is None:
				nc = len(color)
			for i in range(0,len(spec)):
				bad = np.where((np.isfinite(spec[i]) == False) | (spec[i] == 0.0))[0]
				spec[i][bad] = np.nan
				if color is None:
					ax.plot(energy[i],spec[i],label=labs[i],marker='.')
				else:
					ax.plot(energy[i],spec[i],color=color[i % nc],label=labs[i],marker='.')
			
		else:
			bad = np.where((np.isfinite(spec) == False) | (spec == 0.0))[0]
			spec[bad] = np.nan
			ax.plot(energy,spec,color=color,marker='.')

		#set the x-axis scale
		if xlog is None:
			xlog = self._ylog
		if xlog:
			ax.set_xscale('log')
		
		#set the y-axis scale
		if ylog is None:
			ylog = self._zlog
		if ylog:
			ax.set_yscale('log')
			
		#set the axis labels
		if xparam == 'V':
			ax.set_xlabel(self.ylabelv)
		else:
			ax.set_xlabel(self.ylabele)
			
		if yparam == 'PSD':
			ax.set_ylabel(self.zlabelp)
		else:
			ax.set_ylabel(self.zlabelf)
			
		#turn axes off when needed
		if nox:
			ax.set_xlabel('')
			ax.xaxis.set_ticks([])
		if noy:
			ax.set_ylabel('')
			ax.yaxis.set_ticks([])


		if (not FitKappa is False) or (not FitMaxwellian is False) or Integrate:
			ylim = ax.get_ylim()
			ax.set_ylim(ylim)
			
			
			#get the combined spectra
			E,spec,labs = self.GetSpectrum(Date,ut,Method,Maxdt,False,'E','PSD')
			e = 1.6022e-19
			v = RelVelocity(E,self.Mass)
		
			#convert to counts
			C = PSDtoCountsE(E,spec,self.Mass)

			#apply the threshold in keV
			use = np.where((E <= Erange[1]) & (E >= Erange[0]))[0]

			v = v[use]
			E = E[use]
			C = C[use]
			spec = spec[use]
			
			if xparam == 'V':
				x = v
			else:
				x = E
					
			#fit spectrum
			if (not FitKappa is False):
				if FitKappa is 'counts':
					nk,Tk,K,statk = FitKappaDistCtsE(E,C,n0*1e6,T0*1e6,self.Mass,Verbose=True,MaxIter=MaxIter)
				else:
					nk,Tk,K,statk = FitKappaDistE(E,spec,n0*1e6,T0*1e6,self.Mass,Verbose=True,MaxIter=MaxIter)
				fk = KappaDistE(nk,E,Tk,self.Mass,K)
				if yparam == 'Flux':
					y = PSDtoFluxE(E,fk,self.Mass)
				else:
					y = fk
				
				ax.plot(x,y,color='pink',linestyle='--',label=r'Kappa Fit: $n_{\kappa}$=' + '{:5.2f}'.format(nk/1e6)+r' cm$^{-3}$,'+'\n'+'$T_{\kappa}$='+'{:5.2f}'.format(Tk/1e6)+r' MK, $\kappa$='+'{:5.1f}'.format(K))

			if (not FitMaxwellian is False):
				if FitMaxwellian is 'counts':
					nm,Tm,statm = FitMaxwellianDistCtsE(E,C,n0*1e6,T0*1e6,self.Mass,MaxIter=MaxIter)
				else:
					nm,Tm,statm = FitMaxwellianDistE(E,spec,n0*1e6,T0*1e6,self.Mass,Verbose=True,MaxIter=MaxIter)
				fm = MaxwellBoltzmannDistE(nm,E,Tm,self.Mass)
				if yparam == 'Flux':
					y = PSDtoFluxE(E,fm,self.Mass)
				else:
					y = fm
				
				ax.plot(x,y,color='blue',linestyle='--',label=r'M-B Fit: $n$=' + '{:5.2f}'.format(nm/1e6)+r' cm$^{-3}$,'+'\n'+'$T$='+'{:5.2f}'.format(Tm/1e6)+r' MK')
	
			if Integrate:
				ni = IntegrateSpectrum(E,spec,self.Mass,4*np.pi)
				ax.text(0.05,0.95,'$n_I$ = {:6.3f}'.format(ni[0]) + ' cm$^{-3}$',transform=ax.transAxes)
				print('Estimated density: {:6.3f} cm^-3'.format(ni[0]))
	
		if ShowMoments:
			
			moments = self.GetMoments(Date,ut,Maxdt)
			R = ax.axis()
			ax.axis(R)
			
			if xlog:
				x = 10**np.linspace(np.log10(R[0]),np.log10(R[1]),100)
			else:
				x = np.linspace(R[0],R[1],100)
			
			if xparam == 'E':
				E = x
				xueff = RelEnergy(moments[0].ueff,self.Mass)
			else:
				E = RelEnergy(x,self.Mass)
				xueff = moments[0].ueff
			print(xueff*3)
			
			for mom in moments:
				print(mom.ut)
				f1 = MaxwellBoltzmannDistE(mom.n0*1e6,E,mom.T0*1e6,self.Mass)
				f2 = MaxwellBoltzmannDistE(mom.nfit*1e6,E,mom.Tfit*1e6,self.Mass)
				
				ax.plot(x,f1,color='grey',linestyle='--',label=r'$n_0$=' + '{:5.2f}'.format(mom.n0)+r' cm$^{-3}$,'+'\n'+'$T_0$='+'{:5.2f}'.format(mom.T0*1e6)+r' K')
				ax.plot(x,f2,color='red',linestyle='--',label=r'$n_{fit}$=' + '{:5.2f}'.format(mom.nfit)+r' cm$^{-3}$,'+'\n'+'$T_{fit}$='+'{:5.2f}'.format(mom.Tfit*1e6)+r' K')
				
			ax.plot([xueff,xueff],[R[2],R[3]],color='cyan')
			ax.plot([xueff*3,xueff*3],[R[2],R[3]],color='cyan',linestyle='--')
	
		ax.legend(fontsize=8)
			
		return ax
				
		
	def Plot(self,Date=None,ut=[0.0,24.0],fig=None,maps=[1,1,0,0],ylog=None,scale=None,zlog=None,
			cmap='gnuplot',yparam='E',zparam='Flux',nox=False,noy=False,TickFreq='auto',PosAxis=True):
		'''
		Plots the spectrogram
		
		Inputs
		======
		Date : int32
			This, along with 'ut' controls the time limits of the plot,
			either set as a single date in the format yyyymmdd, or if 
			plotting over multiple days then set a 2 element tuple/list/
			numpy.ndarray with the start and end dates. If set to None 
			(default) then the time axis limits will be calculated 
			automatically.
		ut : list/tuple
			2-element start and end times for the plot, where each 
			element is the time in hours sinsce the start fo the day,
			e.g. 17:30 == 17.5.
		yparam : str
			Sets the y-axis of the plot to be either energy
			(keV) or velocity (m/s): 'E'|'V'
		zparam : str
			Sets the type of spectrum to either differential
			energy flux or phase space density: 'Flux'|'PSD'
		fig : None, matplotlib.pyplot or matplotlib.pyplot.Axes instance
			If None - a new plot is created
			If an instance of pyplot then a new Axes is created on an existing plot
			If Axes instance, then plotting is done on existing Axes
		maps : list
			[xmaps,ymaps,xmap,ymap] controls position of subplot
		xlog : bool
			if True, color scale is logarithmic
		ylog : bool
			If True, y-axis is logarithmic
		cmap : str
			String containing the name of the colomap to use
		scale : list
			2-element list or tuple containing the minimum and maximum
			extents of the color scale
		nox : bool
			If True, no labels or tick marks are drawn for the x-axis
		noy : bool
			If True, no labels or tick marks are drawn for the y-axis
		'''
		
		
		
		#create the plot
		if fig is None:
			fig = plt
			fig.figure()
			#adjust the top and bottom
			fig.subplots_adjust(top=0.95,bottom=0.23)
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		
		#set axis limits
		if Date is None:
			ax.set_xlim(self._utlim)
		else:
			if np.size(Date) == 1:
				Date0 = Date
				Date1 = Date
			else:
				Date0 = Date[0]
				Date1 = Date[1]
			utclim = TT.ContUT(np.array([Date0,Date1]),np.array(ut))
			ax.set_xlim(utclim)
		if ylog is None:
			ylog = self._ylog

		#get the yparameter stuff
		if yparam == 'E':
			if ylog:
				ax.set_yscale('log')
				ax.set_ylim(self._logelim)
			else:
				ax.set_ylim(self._elim)
		elif yparam == 'V':
			if ylog:
				ax.set_yscale('log')
				ax.set_ylim(self._logvlim)
			else:
				ax.set_ylim(self._vlim)
		else:
			return		

		
		#and labels
		ax.set_xlabel(self.xlabel)
		if yparam == 'V':
			ax.set_ylabel(self.ylabelv)
		else:
			ax.set_ylabel(self.ylabele)
	


			
		#get color scale
		if zlog is None:
			zlog = self._zlog
		if zparam == 'PSD':
			if scale is None:
				if zlog:
					scale = self._psdlogscale
				else:
					scale = self._psdscale
		elif zparam == 'Flux':
			if scale is None:
				if zlog:
					scale = self._logscale
				else:
					scale = self._scale
		if zlog:
			norm = colors.LogNorm(vmin=scale[0],vmax=scale[1])
		else:
			norm = colors.Normalize(vmin=scale[0],vmax=scale[1])
			
		#create plots
		for i in range(0,self.n):
			tmp = self._PlotSpectrogram(ax,i,norm,cmap,yparam,zparam)
			if i == 0:
				sm = tmp

		#sort the UT axis out
		tdate = np.concatenate(self.Date)
		tutc = np.concatenate(self.utc)
		srt = np.argsort(tutc)
		tdate = tdate[srt]
		tutc = tutc[srt]



		#turn axes off when needed
		if nox:
			ax.set_xlabel('')
			ax.xaxis.set_ticks([])
		else:
			if PosAxis:
				udate = np.unique(tdate)
				
				Pos = ReadFieldTraces([udate[0],udate[-1]])
				
				#get the Lshell, Mlat and Mlon
				good = np.where(np.isfinite(Pos.Lshell) & np.isfinite(Pos.MlatN) & np.isfinite(Pos.MlonN))[0]
				Pos = Pos[good]
				fL = interp1d(Pos.utc,Pos.Lshell,bounds_error=False,fill_value='extrapolate')
				fLon = interp1d(Pos.utc,Pos.MlonN,bounds_error=False,fill_value='extrapolate')
				fLat = interp1d(Pos.utc,Pos.MlatN,bounds_error=False,fill_value='extrapolate')
			
				PosDTPlotLabel(ax,tutc,tdate,fL,fLon,fLat,TickFreq=TickFreq)
				ax.set_xlabel('')
			else:
				TT.DTPlotLabel(ax,tutc,tdate,TickFreq=TickFreq)			
				
			
		if noy:
			ax.set_ylabel('')
			ax.yaxis.set_ticks([])

		#colorbar
		divider = make_axes_locatable(ax)
		cax = divider.append_axes("right", size="2.5%", pad=0.05)

		cbar = fig.colorbar(sm,cax=cax) 
		if zparam == 'PSD':
			cbar.set_label(self.zlabelp)		
		else:
			cbar.set_label(self.zlabelf)		
		self.currax = ax
		
		
		return ax
		
	def UpdateTimeAxis(self,ax=None,Date=None,ut=[0.0,24.0],TickFreq='auto'):
		'''
		Update the time ax is limits and labels.
		
		Inputs
		======
		ax : None or Axes object
			If None, then the current Axes instance will be used
		Date : int32
			This, along with 'ut' controls the time limits of the plot,
			either set as a single date in the format yyyymmdd, or if 
			plotting over multiple days then set a 2 element tuple/list/
			numpy.ndarray with the start and end dates. If set to None 
			(default) then the time axis limits will be calculated 
			automatically.
		ut : list/tuple
			2-element start and end times for the plot, where each 
			element is the time in hours sinsce the start fo the day,
			e.g. 17:30 == 17.5.
		TickFreq : str or float
			If 'auto' the tick spacing will be calculated automatically,
			otherwise set to a number of hours between each tick.
		
		'''
		
		#check if an Axes instance has been supplied (if not, try getting the current one)
		if ax is None:
			ax = self.currax
			
		#check if we need to resize
		if not Date is None:
			if np.size(Date) == 1:
				Date0 = Date
				Date1 = Date
			else:
				Date0 = Date[0]
				Date1 = Date[1]
			utclim = TT.ContUT(np.array([Date0,Date1]),np.array(ut))
			ax.set_xlim(utclim)		
			
		#now update the axis
		tdate = np.concatenate(self.Date)
		tutc = np.concatenate(self.utc)
		srt = np.argsort(tutc)
		tdate = tdate[srt]
		tutc = tutc[srt]
		if PosAxis:
			udate = np.unique(tdate)
			
			Pos = ReadFieldTraces([udate[0],udate[-1]])
			
			#get the Lshell, Mlat and Mlon
			good = np.where(np.isfinite(Pos.Lshell) & np.isfinite(Pos.MlatN) & np.isfinite(Pos.MlonN))[0]
			Pos = Pos[good]
			fL = interp1d(Pos.utc,Pos.Lshell,bounds_error=False,fill_value='extrapolate')
			fLon = interp1d(Pos.utc,Pos.MlonN,bounds_error=False,fill_value='extrapolate')
			fLat = interp1d(Pos.utc,Pos.MlatN,bounds_error=False,fill_value='extrapolate')
		
			PosDTPlotLabel(ax,tutc,tdate,fL,fLon,fLat,TickFreq=TickFreq)
		else:
			TT.DTPlotLabel(ax,tutc,tdate,TickFreq=TickFreq)		
		

	def _PlotSpectrogram(self,ax,I,norm,cmap,yparam,zparam):
		'''
		This will plot a single spectrogram (multiple may be stored in
		this object at any one time
		
		
		
		'''
		#get the appropriate data
		Date = self.Date[I]
		utc = self.utc[I]
		ut = self.ut[I]
		dt = self.dt[I]
		
		if yparam == 'V':
			e = self.V[I]
			e0 = self.V0[I]
			e1 = self.V1[I]
		elif yparam == 'E':	
			e = self.Energy[I]
			e0 = self.E0[I]
			e1 = self.E1[I]
		
		if zparam == 'PSD':
			Spec = self.PSD[I]		
		elif zparam == 'Flux':
			Spec = self.Spec[I]	
		
		#get the energy band limits
		bad = np.where(np.isnan(e))
		e[bad] = 0.0
		e0[bad] = 0.0
		e1[bad] = 0.0

		#get the ut array limits
		t0 = utc
		t1 = utc + dt
		
		
		#look for gaps in ut
		if len(e.shape) > 1:

			isgap = ((utc[1:] - utc[:-1]) > 60.0/3600.0) | ((e[1:,:] - e[:-1,:]) != 0).any(axis=1)
			ne = e.shape[1]
		else:
			#isgap = (utc[1:] - utc[:-1]) > 1.1*dt[:-1]
			isgap = (utc[1:] - utc[:-1]) > 60.0/3600.0
			ne = e.size
		gaps = np.where(isgap)[0] + 1
		if gaps.size == 0:
			#no gaps
			i0 = [0]
			i1 = [utc.size]
		else:
			#lots of gaps
			i0 = np.append(0,gaps)
			i1 = np.append(gaps,utc.size)
		ng = np.size(i0)

		#loop through each continuous block of utc
		for i in range(0,ng):
			ttmp = np.append(t0[i0[i]:i1[i]],t1[i1[i]-1])
			st = Spec[i0[i]:i1[i]]
			for j in range(0,ne):				
				if len(e.shape) > 1:
					etmp = np.array([e0[i0[i],j],e1[i0[i],j]])
				else:
					etmp = np.array([e0[j],e1[j]])
				if np.isfinite(etmp).all():
					#plot each row of energy
					tg,eg = np.meshgrid(ttmp,etmp)
					
					s = np.array([st[:,j]])
					
					sm = ax.pcolormesh(tg,eg,s,cmap=cmap,norm=norm)
			
		return sm
		
	def _CalculateTimeLimits(self):
		'''
		Loop through all of the stored spectra and find the time limits.
		
		'''
		#initialize time limits
		utlim = [np.inf,-np.inf]
		
		#loop through each array
		n = len(self.utc)
		for i in range(0,n):
			mn = np.nanmin(self.utc[i])
			mx = np.nanmax(self.utc[i] + self.dt[i])
			if mn < utlim[0]:
				utlim[0] = mn
			if mx > utlim[1]:
				utlim[1] = mx
		self._utlim = utlim
		
	def _CalculateEnergyLimits(self):
		'''
		Loop through all of the stored spectra and work out the energy
		range to plot.
		
		'''
		#initialize energy limits
		elim = [0.0,-np.inf]
		logelim = [np.inf,-np.inf]
		

		#loop through each array
		n = len(self.Energy)
		for i in range(0,n):

			e0 = self.E0
			e1 = self.E1
			mn = np.nanmin(e0)
			mx = np.nanmax(e1)
			if mn < elim[0]:
				elim[0] = mn
			if mx > elim[1]:
				elim[1] = mx
			le0 = np.log10(e0)
			le1 = np.log10(e1)
			bad = np.where(self.Energy[i] <= 0.0)
			le0[bad] = np.nan
			le1[bad] = np.nan

			lmn = np.nanmin(le0)
			lmx = np.nanmax(le1)
			if lmn < logelim[0]:
				logelim[0] = lmn
			if lmx > logelim[1]:
				logelim[1] = lmx

		self._elim = elim
		self._logelim = 10**np.array(logelim)


	def _CalculateVLimits(self):
		'''
		Loop through all of the stored spectra and work out the velocity
		range to plot.
		
		'''
		#initialize velocity limits
		vlim = [0.0,-np.inf]
		logvlim = [np.inf,-np.inf]
		

		#loop through each array
		n = len(self.V)
		for i in range(0,n):
			f0 = self.V0[i]
			f1 = self.V1[i]
			mn = np.nanmin(f0)
			mx = np.nanmax(f1)
			if mn < vlim[0]:
				vlim[0] = mn
			if mx > vlim[1]:
				vlim[1] = mx
			lf0 = np.log10(f0)
			lf1 = np.log10(f1)
			bad = np.where(self.V[i] <= 0.0)
			lf0[bad] = np.nan
			lf1[bad] = np.nan

			lmn = np.nanmin(lf0)
			lmx = np.nanmax(lf1)
			if lmn < logvlim[0]:
				logvlim[0] = lmn
			if lmx > logvlim[1]:
				logvlim[1] = lmx

		self._vlim = vlim
		self._logvlim = 10**np.array(logvlim)


		
	def _CalculateScale(self):
		'''
		Calculate the default scale limits for the plot.
		
		'''
		scale = [np.inf,-np.inf]
		logscale = [np.inf,-np.inf]
		
		n = len(self.Spec)
		for i in range(0,n):
			ls = np.log10(self.Spec[i])
			bad = np.where(self.Spec[i] <= 0)
			ls[bad] = np.nan
				
			if self._ScaleType == 'std':
				mu = np.nanmean(self.Spec[i])
				std = np.std(self.Spec[i])
				
				lmu = np.nanmean(ls)
				lstd = np.std(ls)
					
				tmpscale = [mu - self._nStd*std, mu + self._nStd*std]
				tmplogscale = 10**np.array([lmu - self._nStd*lstd, lmu + self._nStd*lstd])					
				
			elif self._ScaleType == 'positive':
				#calculate the scale based on all values being positive 
				std = np.sqrt((1.0/np.sum(self.Spec[i].size))*np.nansum((self.Spec[i])**2))
				lstd = np.sqrt(((1.0/np.sum(np.isfinite(ls))))*np.nansum((ls)**2))
					
				tmpscale = [0.0,std*self._nStd]
				tmplogscale = 10**np.array([np.nanmin(ls),lstd*self._nStd])			
			else:
				#absolute range
				tmpscale = [np.nanmin(self.Spec[i]),np.nanmax(self.Spec[i])]
				tmplogscale = 10**np.array([np.nanmin(ls),np.nanmax(ls)])


			if tmpscale[0] < scale[0]:
				scale[0] = tmpscale[0]
			if tmpscale[1] > scale[1]:
				scale[1] = tmpscale[1]
			
			if tmplogscale[0] < logscale[0]:
				logscale[0] = tmplogscale[0]
			if tmplogscale[1] > logscale[1]:
				logscale[1] = tmplogscale[1]
	
		
		self._scale = scale
		self._logscale = logscale
	
	def _CalculatePSDScale(self):
		'''
		Calculate the default scale limits for the plot.
		
		'''
		scale = [np.inf,-np.inf]
		logscale = [np.inf,-np.inf]
		
		n = len(self.PSD)
		for i in range(0,n):
			ls = np.log10(self.PSD[i])
			bad = np.where(self.PSD[i] <= 0)
			ls[bad] = np.nan
				
			if self._ScaleType == 'std':
				mu = np.nanmean(self.PSD[i])
				std = np.std(self.PSD[i])
				
				lmu = np.nanmean(ls)
				lstd = np.std(ls)
					
				tmpscale = [mu - self._nStd*std, mu + self._nStd*std]
				tmplogscale = 10**np.array([lmu - self._nStd*lstd, lmu + self._nStd*lstd])					
				
			elif self._ScaleType == 'positive':
				#calculate the scale based on all values being positive 
				std = np.sqrt((1.0/np.sum(self.Spec[i].size))*np.nansum((self.PSD[i])**2))
				lstd = np.sqrt(((1.0/np.sum(np.isfinite(ls))))*np.nansum((ls)**2))
					
				tmpscale = [0.0,std*self._nStd]
				tmplogscale = 10**np.array([np.nanmin(ls),lstd*self._nStd])			
			else:
				#absolute range
				tmpscale = [np.nanmin(self.PSD[i]),np.nanmax(self.PSD[i])]
				tmplogscale = 10**np.array([np.nanmin(ls),np.nanmax(ls)])


			if tmpscale[0] < scale[0]:
				scale[0] = tmpscale[0]
			if tmpscale[1] > scale[1]:
				scale[1] = tmpscale[1]
			
			if tmplogscale[0] < logscale[0]:
				logscale[0] = tmplogscale[0]
			if tmplogscale[1] > logscale[1]:
				logscale[1] = tmplogscale[1]
	
		
		self._psdscale = scale
		self._psdlogscale = logscale
