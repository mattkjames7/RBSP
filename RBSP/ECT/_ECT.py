import numpy as np
from .. import Globals

#this just stores a few variables for this particular instrument

#data path and index file name:
idxfname = Globals.DataPath + 'ECT/{:s}.{:s}.{:s}.dat'
datapath = Globals.DataPath + 'ECT/{:s}/{:s}/{:s}/'

#file version format
vfmt = 'v\d.\d.\d'


#moments dtype (new ones, not the original)
mdtype = [	('Date','int32'),		#Date in the format yyyymmdd
			('ut','float32'),		#time since start of day in hours
			('utc','float64'),		#continuous time
			('ueff','float32'),		#Effective velocity (v_ExB - u_sc)
			('Ebulk','float32'),	# bulk energy, keV
			('Vsc','float32'),		#spacecraft potential, Volts
			('n0','float32'),		#Original density cm^-3
			('T0','float32'),		#T = (Tpar + 2*Tperp)/3 MK
			('Tpar','float32'),	#Original parallel temperature
			('Tperp','float32'),	#Original perpendicular temperature
			('nfit','float32'),	#density calculated by refitting the spectrum
			('Tfit','float32'),	#temperature as above
			('Success','bool8'),
			('nPEND','float32'),	#Partial Energy Number Density 
			('TPEND','float32'),]	#Temperature of above			




idtype = [	('Date','int32'),		#Date in the format yyyymmdd
			('ut','float32'),		#time since start of day in hours
			('utc','float64'),		#continuous time
			('ueff','float32'),		#Effective velocity (v_ExB - u_sc)
			('H_Ebulk','float32'),	#Proton bulk energy, keV
			('He_Ebulk','float32'),	#Helium bulk energy, keV
			('O_Ebulk','float32'),	#Oxygen bulk energy, keV
			('Vsc','float32'),		#spacecraft potential, Volts
			('H_n0','float32'),		#Original proton density
			('H_T0','float32'),		#T = (Tpar + 2*Tperp)/3 in MK
			('H_Tpar','float32'),	#Original parallel temperature
			('H_Tperp','float32'),	#Original perpendicular temperature
			('H_nfit','float32'),	#density calculated by refitting the spectrum
			('H_Tfit','float32'),	#temperature as above
			('H_Success','bool8'),
			('H_nPEND','float32'),	#Partial Energy Number Density 
			('H_TPEND','float32'),	#Temperature of above			
			('He_n0','float32'),	#Original Helium ion density
			('He_T0','float32'),	#T = (Tpar + 2*Tperp)/3
			('He_Tpar','float32'),	#Original parallel temperature
			('He_Tperp','float32'),	#Original perpendicular temperature
			('He_nfit','float32'),	#density calculated by refitting the spectrum
			('He_Tfit','float32'),	#temperature as above
			('He_Success','bool8'),
			('He_nPEND','float32'),	#Partial Energy Number Density 
			('He_TPEND','float32'),	#Temperature of above			
			('O_n0','float32'),		#Original oxygen density
			('O_T0','float32'),		#T = (Tpar + 2*Tperp)/3
			('O_Tpar','float32'),	#Original parallel temperature
			('O_Tperp','float32'),	#Original perpendicular temperature
			('O_nfit','float32'),	#density calculated by refitting the spectrum
			('O_Tfit','float32'),	#temperature as above
			('O_Success','bool8'),
			('O_nPEND','float32'),	#Partial Energy Number Density 
			('O_TPEND','float32'),]	#Temperature of above

edtype = [	('Date','int32'),		#Date in the format yyyymmdd
			('ut','float32'),		#time since start of day in hours
			('utc','float64'),		#continuous time
			('ueff','float32'),		#Effective velocity (v_ExB - u_sc)
			('e_Ebulk','float32'),	#electron bulk energy, keV
			('Vsc','float32'),		#spacecraft potential, Volts
			('e_n0','float32'),		#Original electron density
			('e_T0','float32'),		#T = (Tpar + 2*Tperp)/3
			('e_Tpar','float32'),	#Original parallel temperature
			('e_Tperp','float32'),	#Original perpendicular temperature
			('e_nfit','float32'),	#density calculated by refitting the spectrum
			('e_Tfit','float32'),	#temperature as above
			('e_Success','bool8'),
			('e_nPEND','float32'),	#Partial Energy Number Density 
			('e_TPEND','float32'),]	#Temperature of above			
