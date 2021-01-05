import numpy as np
from . import _ECT
from ..EFW.GetPotential import GetPotential
from ..VExB.ReadData import ReadData
from .ReadCDF import ReadCDF
from scipy.interpolate import interp1d
from ..Tools.RelVelocity import RelVelocity
from ..Tools.FitMaxwellianDist import FitMaxwellianDist
from ..Tools.IntegrateFluxes import IntegrateFluxes
import DateTimeTools as TT
from .. import Globals
import os
import RecarrayTools as RT


def _CalculatePSD(Spec,Energy,Mass):
	e = 1.6022e-19
	psd =  np.float64(Spec)*(np.float64(Mass)/(2000*e*np.float64(Energy/Mass))) * np.float64(10.0/e)
	return psd

def _CreateMoments(Species,hopepa,hopem,fpot,fueff):
	
	#some constants
	e = np.float64(1.6022e-19)
	kB = np.float64(1.380649e-23)
	eVtoK = e/kB
	
	#some CDF tags
	tags = {	'H' : ('Epoch_Ion','HOPE_ENERGY_Ion','ENERGY_Ion_DELTA',
						'Dens_p_30','Tpar_p_30','Tperp_p_30','FPDO'),
				'He' : ('Epoch_Ion','HOPE_ENERGY_Ion','ENERGY_Ion_DELTA',
						'Dens_he_30','Tpar_he_30','Tperp_he_30','FHEDO'),
				'O' : ('Epoch_Ion','HOPE_ENERGY_Ion','ENERGY_Ion_DELTA',
						'Dens_o_30','Tpar_o_30','Tperp_o_30','FODO'),
				'e' : ('Epoch_Ele','HOPE_ENERGY_Ele','ENERGY_Ele_DELTA',
						'Dens_e_200','Tpar_e_200','Tperp_e_200','FEDO'),}
	tepoch,tenergy,tdenergy,tdens,ttpar,ttperp,tflux = tags[Species]

	#mass
	amu = 1.6605e-27
	masses = { 	'e' : 9.10938356e-31,
				'H' : 1.6726219e-27,
				'He' : 4.002602*amu,
				'O' : 15.999*amu }
	m = masses[Species]
	
	#create output array
	print('Creating Output Array')
	ns = hopepa[tepoch].size
	out = np.recarray(ns,dtype=_ECT.mdtype)	
		
	#dates and times
	out.Date,out.ut = TT.CDFEpochtoDate(hopepa[tepoch])
	out.utc = TT.ContUT(out.Date,out.ut)
	
	#copy fields across -  convert Temperatures from eV to MK
	out.n0 = hopem[tdens]
	out.Tpar = hopem[ttpar]*1e-6
	out.Tperp = hopem[ttperp]*1e-6
	out.T0 = (out.Tpar + 2.0*out.Tperp)/3.0

	bad = np.where(out.n0 <= 0.0)[0]
	out.n0[bad] = np.nan
	bad = np.where(out.T0 <= 0.0)[0]
	out.T0[bad] = np.nan	
		
	print('Calculating Energy Bins')
	#calculate dE and E in keV
	E = hopepa[tenergy]/1000.0
	out.Vsc = fpot(out.utc)
	dE = np.abs(out.Vsc)/1000.0
	E = (E.T + dE).T
		
	#get E0 and E1
	E0 = E - hopepa[tdenergy]/1000.0
	E1 = E + hopepa[tdenergy]/1000.0

	print('Calculating Effective Velocity')
	#calculate ueff
	ueff = fueff(out.utc)
	out.ueff = ueff

	#get the bulk energies (keV)
	Ebulk = (0.001*0.5*m*ueff**2 )/e
	out.Ebulk = Ebulk


	#calculate the velocities
	V = (RelVelocity(E,m).T - ueff).T

	
	print('Calculating PSD')
	#get the PSD
	f = _CalculatePSD(hopepa[tflux],E,m)


	#The energy range over which to do PEND (EHOPEmin < E < 20 eV)
	#for the fitting process, use E < 3*Ebulk
	print('Calculating PEND')
	#### the easy bit: calculating the PEND densities ###
	out.nPEND = IntegrateFluxes(E,E0,E1,hopepa[tflux],m,4*np.pi,0.0,Erange=(0.0,20.0))
	
	#try fitting a M-B distribution
	print('Fitting Spectra')
	for i in range(0,ns):
		print('\rFitting {:s} Spectrum {:04d} of {:04d}'.format(Species,i+1,ns),end='')
		use = np.where(E[i] <= 3*Ebulk[i])[0]
		use = np.where(E[i] <= 0.01)[0]
		if use.size < 3:
			n = -1
			T = -1
			s = False
		else:
			n,T,s = FitMaxwellianDist(V[i][use],f[i][use],out.nPEND[i]*1e6,out.T0[i]*1e6,m)
		if n < 0:
			n = np.nan
			T = np.nan
		else:
			n *= 1e-6
			T *= 1e-6
		out.nfit[i] = n
		out.Tfit[i] = T
		out.Success[i] = s
	print()	
	
	return out
			
def SaveMoments(Date,sc,Verbose=True,Overwrite=True):
	'''
	Save some new moments for the HOPE data.
	
	'''
	Species = ['H','He','O','e']
	
	Loaded = False
	
	for S in Species:
		#get the file and folder names
		outdir = Globals.DataPath + 'Moments/{:s}/{:s}/'.format(sc,S)
		if not os.path.isdir(outdir):
			os.system('mkdir -pv '+outdir)
		fname = outdir + '{:08d}.bin'.format(Date)
		if os.path.isfile(fname) and not Overwrite:
			print('File Exists')
		else:
			if not Loaded:
				#read the HOPE data in
				print('Reading HOPE data')
				hopepa,_ = ReadCDF(Date,sc,'hope','l3.pitchangle')
				hopem,_ = ReadCDF(Date,sc,'hope','l3.moments')
				
				#get the ExB drift
				print('Reading ExB Drift')
				exb = ReadData(Date,sc)
				
				#get the spacecraft potential
				print('Reading Potential')
				pot = GetPotential(Date,sc)
				
				print('Creating Interpolation Objects')
				#create an interp object for pot
				fpot = interp1d(pot.utc,pot.Vsc,fill_value='extrapolate',bounds_error=False)

				#ueff
				vx = np.float64(exb.mVxExB - exb.Vx)
				vy = np.float64(exb.mVyExB - exb.Vy)
				vz = np.float64(exb.mVzExB - exb.Vz)
				ueff = np.sqrt(vx**2 + vy**2 + vz**2)
				fueff = interp1d(exb.utc,ueff,fill_value='extrapolate',bounds_error=False)	
				Loaded = True			
			
			data = _CreateMoments(S,hopepa,hopem,fpot,fueff)
		
			#save the file
			print('Saving: '+fname)
			RT.SaveRecarray(data,fname)
	
	


