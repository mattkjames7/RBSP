import numpy as np
from . import _ECT
from .ReadHOPEOmni import ReadHOPEOmni
from .ReadCDF import ReadCDF
from ..EFW.GetPotential import GetPotential
from ..VExB.ReadData import ReadData
import DateTimeTools as TT
from ..Tools.RelEnergy import RelEnergy
from ..Tools.IntegrateSpectra import IntegrateSpectra
from .. import EMFISIS
from .. import EFW
from scipy.special import erfinv
from scipy.interpolate import interp1d


def CalculateIonMoments(Date,sc,MaxE=0.02):	
	'''
	Save some new moments for the HOPE data.
	
	'''
	#some constants
	e = np.float64(1.6022e-19)
	kB = np.float64(1.380649e-23)
	eVtoK = e/kB
		
	
	#read in the HOPE data
	print('Reading HOPE data')
	spec = ReadHOPEOmni(Date,sc,RemoveBinOverlap=True)
	sH = spec['H+Flux']
	sHe = spec['He+Flux']
	sO = spec['O+Flux']
	moms,_ = ReadCDF(Date,sc,'hope','l3.moments')
	
	#check that both moments and spectra align
	ts = sH.utc[0]
	tm = TT.ContUT(*TT.CDFEpochtoDate(moms['Epoch_Ion']))
	if ts.size == tm.size:
		inds = np.arange(ts.size)
	else:
		inds = np.array([np.where(ts == tm[i])[0][0] for i in range(tm.size)])
	
	#create output arrays
	print('Creating output array')
	ns = spec['H+Flux'].utc[0].size
	out = np.recarray(ns,dtype=_ECT.idtype)
	out.fill(np.nan)

	#copy some fields across
	print('Copying Fields')
	out.Date = spec['H+Flux'].Date[0]
	out.ut = spec['H+Flux'].ut[0]
	out.utc = spec['H+Flux'].utc[0]
	
	out.H_n_h[inds] = moms['Dens_p_30']*1e6
	out.H_T_hpar[inds] = moms['Tpar_p_30']*eVtoK
	out.H_T_hperp[inds] = moms['Tperp_p_30']*eVtoK
	out.H_T_h = (out.H_T_hpar + 2.0*out.H_T_hperp)/3.0
	out.H_p_h = kB*out.H_T_h*out.H_n_h
	
	out.He_n_h[inds] = moms['Dens_he_30']*1e6
	out.He_T_hpar[inds] = moms['Tpar_he_30']*eVtoK
	out.He_T_hperp[inds] = moms['Tperp_he_30']*eVtoK
	out.He_T_h = (out.He_T_hpar + 2.0*out.He_T_hperp)/3.0
	out.He_p_h = kB*out.He_T_h*out.He_n_h
	
	out.O_n_h[inds] = moms['Dens_o_30']*1e6
	out.O_T_hpar[inds] = moms['Tpar_o_30']*eVtoK
	out.O_T_hperp[inds] = moms['Tperp_o_30']*eVtoK
	out.O_T_h = (out.O_T_hpar + 2.0*out.O_T_hperp)/3.0
	out.O_p_h = kB*out.O_T_h*out.O_n_h
	
	#get the ExB drift
	print('Reading ExB Drift')
	exb = ReadData(Date,sc)
				
	#get the spacecraft potential
	print('Reading Potential')
	pot = GetPotential(Date,sc)
	
	#read in the electron densities
	print('Reading UHR/EFW electron densities')
	uhr,_ = EMFISIS.ReadCDF(Date,sc,L='l4')
	efw,_ = EFW.ReadCDF(Date,sc,'l3')
	
	#calcualte time arrays and extract densities
	if not uhr is None:
		if uhr['Epoch'] is None:
			uhr = None
			utcu = []
			nu = []
		else:
			du,tu = TT.CDFEpochtoDate(uhr['Epoch'])
			utcu = TT.ContUT(du,tu)
			nu = uhr['density']
			good = np.where(np.isfinite(nu) & (nu > 0))[0]
			utcu = utcu[good]
			nu = nu[good]
	else:
		utcu = []
		nu = []
	
	if not efw is None:
		de,te = TT.CDFEpochtoDate(efw['epoch'])
		utce = TT.ContUT(de,te)
		ne = efw['density']
		good = np.where(np.isfinite(ne) & (ne > 0))[0]
		utce = utce[good]
		ne = ne[good]
	else:
		utce = []
		ne = []

	#scan for gaps in uhr data > 5 minutes
	no_ne = False
	if not uhr is None:
		fillt = []
		filln = []
		dt = utcu[1:] - utcu[:-1]
		gap = np.where(dt > 5/60.0)[0]
		if gap.size > 0:
			for g in gap:
				t0 = utcu[g]
				t1 = utcu[g+1]
				use = np.where((utce > t0) & (utce < t1))[0]
				if use.size > 0:
					fillt.append(utce[use])
					filln.append(ne[use])
		use = np.where(utce < utcu[0])[0]
		if use.size > 0:
			fillt.append(utce[use])
			filln.append(ne[use])		
		use = np.where(utce > utcu[-1])[0]
		if use.size > 0:
			fillt.append(utce[use])
			filln.append(ne[use])
		if len(fillt) > 0:
			utcne = np.concatenate(fillt)
			ne = np.concatenate(filln)
			utcne = np.append(utcu,utcne)
			ne = np.append(nu,ne)
			srt = np.argsort(utcne)
			utcne = utcne[srt]
			ne = ne[srt]
		else:
			utcne = utcu
			ne = nu
	elif not efw is None:
		utcne = utce
	else:
		#no electron densities
		no_ne = True
	if not no_ne:
		fne = interp1d(utcne,ne,fill_value=(ne[0],ne[-1]),bounds_error=False)
		out.ne = fne(out.utc)*1e6
		
		#find any gaps
		dt = utcne[1:] - utcne[:-1]
		gap = np.where(dt > 5/60.0)[0]

		if gap.size > 0:
			for g in gap:
				t0 = utcne[g]
				t1 = utcne[g+1]
				use = np.where((out.utc > t0) & (out.utc < t1))[0]	
				out.ne[use] = np.nan


	print('Creating Interpolation Objects')
	#create an interp object for pot
	fpot = interp1d(pot.utc,pot.Vsc,fill_value=(pot.Vsc[0],pot.Vsc[-1]),bounds_error=False)

	#ueff
	vx = np.float64(exb.mVxExB - exb.Vx)
	vy = np.float64(exb.mVyExB - exb.Vy)
	vz = np.float64(exb.mVzExB - exb.Vz)
	ueff = np.sqrt(vx**2 + vy**2 + vz**2)
	fueff = interp1d(exb.utc,ueff,fill_value=(ueff[0],ueff[-1]),bounds_error=False)	
	fvx = interp1d(exb.utc,vx,fill_value=(vx[0],vx[-1]),bounds_error=False)	
	fvy = interp1d(exb.utc,vy,fill_value=(vy[0],vy[-1]),bounds_error=False)	
	fvz = interp1d(exb.utc,vz,fill_value=(vz[0],vz[-1]),bounds_error=False)	

	
	#calculate bulk velocity and spacecraft potential
	print('Calculating bulk velocity and spacecraft potential')
	out.vbulk = fueff(out.utc)
	out.vbulkx = fvx(out.utc)
	out.vbulky = fvy(out.utc)
	out.vbulkz = fvz(out.utc)
	out.H_Ebulk = RelEnergy(out.vbulk,_ECT.mass['H'])
	out.He_Ebulk = RelEnergy(out.vbulk,_ECT.mass['He'])
	out.O_Ebulk = RelEnergy(out.vbulk,_ECT.mass['O'])
	out.Vsc = np.abs(fpot(out.utc))
	
	#integrate spectra initially
	print('Integrating spectra for initial n, T and p estimates...')
	print('Hydrogen')
	nH,TH,pH = IntegrateSpectra(sH.Energy[0],sH.E0[0],sH.E1[0],sH.Spec[0],_ECT.mass['H'],4*np.pi,out.Vsc,out.vbulk,Erange=(0.0,MaxE))
	print('Helium')
	nHe,THe,pHe = IntegrateSpectra(sHe.Energy[0],sHe.E0[0],sHe.E1[0],sHe.Spec[0],_ECT.mass['He'],4*np.pi,out.Vsc,out.vbulk,Erange=(0.0,MaxE))
	print('Oxygen')
	nO,TO,pO = IntegrateSpectra(sO.Energy[0],sO.E0[0],sO.E1[0],sO.Spec[0],_ECT.mass['O'],4*np.pi,out.Vsc,out.vbulk,Erange=(0.0,MaxE))
		
	
	print('Rescaling moments using electron density')
	#get total ions
	nI = nH + nHe + nO
	out.ni_c = nI
	
	#work out fractions
	fH = nH/nI
	fHe = nHe/nI
	fO = nO/nI

	
	#work out scaling factor to correct densities
	if no_ne:
		out.Rescaled = False
		out.ne = nI
	else:
		good = np.where(np.isfinite(out.ne) & np.isfinite(nH))[0]
		out.Rescaled[good] = True
	scale = out.ne/nI
	bad = np.where(np.isfinite(scale) == False)[0]
	scale[bad] = 1.0
	out.Rescaled[bad] = False
	
	#scale densities and pressures up
	nH *= scale
	pH *= scale
	nHe *= scale
	pHe *= scale
	nO *= scale
	pO *= scale
		
	print('Calculating temperatures')
	#calculate Ehope min and then the difference between that and the bulk energy
	Ehmin = sH.Energy[0][:,0] + out.Vsc/1000.0
	#this may or may not be a fudge (genuinely not sure)
	#Ehmin = 0.001 + out.Vsc/1000.0
	out.Emin = Ehmin
	dEH = (Ehmin - out.H_Ebulk)*1000.0*e
	dEHe = (Ehmin - out.He_Ebulk)*1000.0*e
	dEO = (Ehmin - out.O_Ebulk)*1000.0*e
	
	
	#calculate Tpend (use "nominal" proportions of 1.0, 0.15 and 0.01, respectively, for H, He and O)
	out.H_T_c_ul[:,0] = np.float64((np.sqrt(2)*dEH)/(erfinv(1.0 - ((nH/scale)/out.ne))))/kB
	out.He_T_c_ul[:,0] = np.float64((np.sqrt(2)*dEHe)/(erfinv(1.0 - ((nHe/scale)/(0.15*out.ne)))))/kB
	out.O_T_c_ul[:,0] = np.float64((np.sqrt(2)*dEO)/(erfinv(1.0 - ((nO/scale)/(0.01*out.ne)))))/kB
	

		
	#now the other method which directly uses the integrals
	out.H_T_c_ul[:,1] = TH
	out.He_T_c_ul[:,1] = THe
	out.O_T_c_ul[:,1] = TO

	
	#now fill the main cold ion temperature array
	#use PEND for Ehmin > 1.25 Ebulk
	#integral method otherwise
	goodTH = np.isfinite(out.H_T_c_ul[:,0]) & (out.H_T_c_ul[:,0] > 0)
	goodTHe = np.isfinite(out.He_T_c_ul[:,0]) & (out.He_T_c_ul[:,0] > 0)
	goodTO = np.isfinite(out.O_T_c_ul[:,0]) & (out.O_T_c_ul[:,0] > 0)
	goodT = goodTH & goodTHe & goodTO
	pendH = np.where((Ehmin > 1.25*out.H_Ebulk) & goodT)[0]
	pendHe = np.where((Ehmin > 1.25*out.He_Ebulk) & goodT)[0]
	pendO = np.where((Ehmin > 1.25*out.O_Ebulk) & goodT)[0]
	out.H_T_c = out.H_T_c_ul[:,1]
	out.He_T_c = out.He_T_c_ul[:,1]
	out.O_T_c[:,1] = out.O_T_c_ul[:,1]
	out.H_T_c[pendH] = out.H_T_c_ul[pendH,0]
	out.He_T_c[pendHe] = out.He_T_c_ul[pendHe,0]
	out.O_T_c[pendO,1] = out.O_T_c_ul[pendO,0]
		
		
	#calculate lower T limit of Oxygen
	out.O_T_c[:,0] = 0.27*out.O_T_c[:,1]
	
	print('Recalculating moments')
	#calculate fOprime - the new scaling factor based on the lower T limit
	fOprime = ((out.O_T_c[:,0]/out.O_T_c[:,1])**1.1)*fO
		
	#calculate the new total fprime
	sumfprime = fH + fHe + fOprime
	
	#get the upper and lower limits to the oxygen density
	out.O_n_c[:,1] = (fOprime/sumfprime)*out.ne #upper
	out.O_n_c[:,0] = nO #lower
		
	#then also hydrogen and helium
	out.H_n_c[:,1] = (fH/sumfprime)*out.ne #lower
	out.H_n_c[:,0] = nH #upper
	out.He_n_c[:,1] = (fHe/sumfprime)*out.ne #lower
	out.He_n_c[:,0] = nHe #upper
		
	#fill in the temperatures
	out.H_T_c = TH
	out.He_T_c = THe
		
	#recalculate pressure
	out.H_p_c[:,0] = kB*out.H_n_c[:,0]*out.H_T_c
	out.H_p_c[:,1] = kB*out.H_n_c[:,1]*out.H_T_c
	out.He_p_c[:,0] = kB*out.He_n_c[:,0]*out.He_T_c
	out.He_p_c[:,1] = kB*out.He_n_c[:,1]*out.He_T_c
	out.O_p_c[:,0] = kB*out.O_n_c[:,0]*out.O_T_c[:,0]
	out.O_p_c[:,1] = kB*out.O_n_c[:,1]*out.O_T_c[:,1]
	
	#calcualte Mav
	print('Calculating Average ion Mass')
	Hamu = _ECT.mass['H']/_ECT.amu
	Heamu = _ECT.mass['He']/_ECT.amu
	Oamu = _ECT.mass['O']/_ECT.amu

	#cold ions
	out.Mav_c[:,0] = (Hamu*out.H_n_c[:,0] + Heamu*out.He_n_c[:,0] + Oamu*out.O_n_c[:,0])/out.ne
	out.Mav_c[:,1] = (Hamu*out.H_n_c[:,1] + Heamu*out.He_n_c[:,1] + Oamu*out.O_n_c[:,1])/out.ne

	#for hot ions
	ne_h = out.H_n_h + out.He_n_h + out.O_n_h
	out.Mav_h = (Hamu*out.H_n_h + Heamu*out.He_n_h + Oamu*out.O_n_h)/ne_h
	
	return out
