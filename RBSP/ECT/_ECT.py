import numpy as np
from .. import Globals

#this just stores a few variables for this particular instrument

#data path and index file name:
idxfname = Globals.DataPath + 'ECT/{:s}.{:s}.{:s}.dat'
datapath = Globals.DataPath + 'ECT/{:s}/{:s}/{:s}/'

#file version format
vfmt = 'v\d.\d.\d'

amu = 1.6605e-27
mass = { 	'e' : 9.10938356e-31,
			'H' : 1.6726219e-27,
			'He' : 4.002602*amu,
			'O' : 15.999*amu }
				
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

idtype = [	('Date','int32'),			#Date in the format yyyymmdd
			('ut','float32'),			#time since start of day in hours
			('utc','float64'),			#continuous time
			('vbulk','float32'),		#Effective velocity (v_ExB - u_sc) magnitude
            ('vbulkx','float32'),		#Effective velocity (v_ExB - u_sc)
            ('vbulky','float32'),		#Effective velocity (v_ExB - u_sc)
            ('vbulkz','float32'),		#Effective velocity (v_ExB - u_sc)
			('H_Ebulk','float32'),		# bulk energy, keV
			('He_Ebulk','float32'),		# bulk energy, keV
			('O_Ebulk','float32'),		# bulk energy, keV
			('Vsc','float32'),			#spacecraft potential, Volts
			('Emin','float32'),			#Minimum HOPE energy (keV)
			('ne','float32'),			#Electron density according to EFW or EMFISIS (m^-3)
			('ni_c','float32'),			#Number of ions (before rescaling to match electrons) (m^-3)
			('H_n_h','float32'),		#Original density m^-3 (hot ions > 3e eV/electrons > 200eV)
			('H_T_h','float32'),		#T = (Tpar + 2*Tperp)/3 K  (hot ions > 3e eV/electrons > 200eV)
			('H_p_h','float32'),		#pressure (Pa)  (hot ions > 3e eV/electrons > 200eV)
			('H_T_hpar','float32'),		#Original parallel temperature
			('H_T_hperp','float32'),	#Original perpendicular temperature
			('H_n_c','float32',(2,)),		#Cold density (m^-3)
			('H_T_c','float32'),		#Cold temperature (K)	
			('H_p_c','float32',(2,)),		#Cold pressure (Pa)	
			('H_T_c_ul','float32',(2,)),#two upper limits of proton temperatures: 0 - PEND method, 1 - integration method
			('He_n_h','float32'),		#Original density m^-3 (hot ions > 3e eV/electrons > 200eV)
			('He_T_h','float32'),		#T = (Tpar + 2*Tperp)/3 K  (hot ions > 3e eV/electrons > 200eV)
			('He_p_h','float32'),		#pressure (Pa)  (hot ions > 3e eV/electrons > 200eV)
			('He_T_hpar','float32'),	#Original parallel temperature
			('He_T_hperp','float32'),	#Original perpendicular temperature
			('He_n_c','float32',(2,)),		#Cold density (m^-3)
			('He_T_c','float32'),		#Cold temperature (K)	
			('He_p_c','float32',(2,)),		#Cold pressure (Pa)	
			('He_T_c_ul','float32',(2,)),#two upper limits of helium temperatures: 0 - PEND method, 1 - integration method
			('O_n_h','float32'),		#Original density m^-3 (hot ions > 3e eV/electrons > 200eV)
			('O_T_h','float32'),		#T = (Tpar + 2*Tperp)/3 K  (hot ions > 3e eV/electrons > 200eV)
			('O_p_h','float32'),		#pressure (Pa)  (hot ions > 3e eV/electrons > 200eV)
			('O_T_hpar','float32'),		#Original parallel temperature
			('O_T_hperp','float32'),	#Original perpendicular temperature
			('O_n_c','float32',(2,)),	#Cold density (m^-3)
			('O_T_c','float32',(2,)),	#Cold temperature (K)	
			('O_p_c','float32',(2,)),	#Cold pressure (Pa)	
			('O_T_c_ul','float32',(2,)),#two upper limits of oxygen temperatures: 0 - PEND method, 1 - integration method
			('Mav_h','float32'),		#Hot ion average ion mass
			('Mav_c','float32',(2,)),	#cold ion average ion mass
			('Rescaled','bool')]		#True if ne exists, otherwise, possibly shouldn't trust


# idtype = [	('Date','int32'),		#Date in the format yyyymmdd
			# ('ut','float32'),		#time since start of day in hours
			# ('utc','float64'),		#continuous time
			# ('ueff','float32'),		#Effective velocity (v_ExB - u_sc)
			# ('H_Ebulk','float32'),	#Proton bulk energy, keV
			# ('He_Ebulk','float32'),	#Helium bulk energy, keV
			# ('O_Ebulk','float32'),	#Oxygen bulk energy, keV
			# ('Vsc','float32'),		#spacecraft potential, Volts
			# ('H_n0','float32'),		#Original proton density
			# ('H_T0','float32'),		#T = (Tpar + 2*Tperp)/3 in MK
			# ('H_Tpar','float32'),	#Original parallel temperature
			# ('H_Tperp','float32'),	#Original perpendicular temperature
			# ('H_nfit','float32'),	#density calculated by refitting the spectrum
			# ('H_Tfit','float32'),	#temperature as above
			# ('H_Success','bool8'),
			# ('H_nPEND','float32'),	#Partial Energy Number Density 
			# ('H_TPEND','float32'),	#Temperature of above			
			# ('He_n0','float32'),	#Original Helium ion density
			# ('He_T0','float32'),	#T = (Tpar + 2*Tperp)/3
			# ('He_Tpar','float32'),	#Original parallel temperature
			# ('He_Tperp','float32'),	#Original perpendicular temperature
			# ('He_nfit','float32'),	#density calculated by refitting the spectrum
			# ('He_Tfit','float32'),	#temperature as above
			# ('He_Success','bool8'),
			# ('He_nPEND','float32'),	#Partial Energy Number Density 
			# ('He_TPEND','float32'),	#Temperature of above			
			# ('O_n0','float32'),		#Original oxygen density
			# ('O_T0','float32'),		#T = (Tpar + 2*Tperp)/3
			# ('O_Tpar','float32'),	#Original parallel temperature
			# ('O_Tperp','float32'),	#Original perpendicular temperature
			# ('O_nfit','float32'),	#density calculated by refitting the spectrum
			# ('O_Tfit','float32'),	#temperature as above
			# ('O_Success','bool8'),
			# ('O_nPEND','float32'),	#Partial Energy Number Density 
			# ('O_TPEND','float32'),]	#Temperature of above

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
