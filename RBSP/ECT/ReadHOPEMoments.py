import numpy as np
from .ReadCDF import ReadCDF
import DateTimeTools as TT

def ReadHOPEMoments(Date,sc='a'):
	'''
	Read the HOPE plasma moments.
	
	'''
	
	#define the dtype to be used
	dtype = [	('Date','int32'),
				('ut','float32'),
				('utc','float64'),
				('L','float32'),
				('MLT','float32'),
				('n','float32'),
				('Tav','float32'),
				('Tpar','float32'),
				('Tperp','float32'),
				('TperpTpar','float32')]
				
	#read the data file
	data,meta = ReadCDF(Date,sc,'hope','l3.moments')
				
	#electrons
	n = data['Epoch_Ele'].size
	e = np.recarray(n,dtype=dtype)
	e.Date,e.ut = TT.CDFEpochtoDate(data['Epoch_Ele'])
	e.utc = TT.ContUT(e.Date,e.ut)
	try: #sometimes L is not the right length for electrons annoyingly
		e.L = data['L']
		e.MLT = data['MLT']
	except:
		pass
		
	e.n = data['Dens_e_200']
	e.Tpar = data['Tpar_e_200']
	e.Tperp = data['Tperp_e_200']
	e.TperpTpar = data['Tperp_Tpar_e_30']
	e.Tav = (e.Tpar + 2.0*e.Tperp)/3.0
		
				
	#protons
	n = data['Epoch_Ion'].size
	p = np.recarray(n,dtype=dtype)
	p.Date,p.ut = TT.CDFEpochtoDate(data['Epoch_Ion'])
	p.utc = TT.ContUT(p.Date,p.ut)
	p.L = data['L']
	p.MLT = data['MLT']
	p.n = data['Dens_p_30']
	p.Tpar = data['Tpar_p_30']
	p.Tperp = data['Tperp_p_30']
	p.TperpTpar = data['Tperp_Tpar_p_30']
	p.Tav = (p.Tpar + 2.0*p.Tperp)/3.0
				
	#helium
	n = data['Epoch_Ion'].size
	he = np.recarray(n,dtype=dtype)
	he.Date,he.ut = TT.CDFEpochtoDate(data['Epoch_Ion'])
	he.utc = TT.ContUT(he.Date,he.ut)
	he.L = data['L']
	he.MLT = data['MLT']
	he.n = data['Dens_he_30']
	he.Tpar = data['Tpar_he_30']
	he.Tperp = data['Tperp_he_30']
	he.TperpTpar = data['Tperp_Tpar_he_30']
	he.Tav = (he.Tpar + 2.0*he.Tperp)/3.0
				
	#oxygen
	n = data['Epoch_Ion'].size
	o = np.recarray(n,dtype=dtype)
	o.Date,o.ut = TT.CDFEpochtoDate(data['Epoch_Ion'])
	o.utc = TT.ContUT(o.Date,o.ut)
	o.L = data['L']
	o.MLT = data['MLT']
	o.n = data['Dens_o_30']
	o.Tpar = data['Tpar_o_30']
	o.Tperp = data['Tperp_o_30']
	o.TperpTpar = data['Tperp_Tpar_o_30']
	o.Tav = (o.Tpar + 2.0*o.Tperp)/3.0
	
	#replace bad values
	fields = ['n','Tperp','Tpar','TperpTpar','Tav']
	obj = [e,p,he,o]
	for f in fields:
		for O in obj:
			bad = np.where(O[f] < -1e-30)[0]
			O[f][bad] = np.nan
				
	return p,he,o,e
