import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.PSpecCls import PSpecCls
import DateTimeTools as TT
from ..Tools.ProcessEnergyBins import ProcessEnergyBins

def ReadHOPESA(Date,sc='a',RemoveBinOverlap=True):
	'''
	Reads the level 2 spinaverage data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
		If Date is a single integer - one date is loaded.
		If Date is a 2-element tuple or list, all dates from Date[0] to
		Date[1] are loaded.
		If Date contains > 2 elements, all dates within the list will
		be loaded.
	sc : 
		Spacecraft to load data for: 'a' or 'b'
			
	Returns
	=======
	data : dict
		Contains the following fields:
		'H+Flux' : PSpecCls object, contains proton fluxes
		'He+Flux' : PSpecCls object, contains helium ion fluxes
		'O+Flux' : PSpecCls object, contains oxygen ion fluxes
		'eFlux' : PSpecCls object, contains electron fluxes
		
	For more information about the PSpecCls object, see Arase.Tools.PSpecCls 
		

	'''		


	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = TT.ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'H+Flux' : None,
			'He+Flux' : None,
			'O+Flux' : None,
			'eFlux' : None}


	#loop through dates
	for date in dates:	
				
					
		#read the CDF file
		data,meta = ReadCDF(date,sc,'hope','l2.spinaverage')		

		if data is None:
			continue
		
		
		#get the time 
		sEpochI = data['Epoch_Ion']
		sDateI,sutI = TT.CDFEpochtoDate(sEpochI)
		sEpochE = data['Epoch_Ele']
		sDateE,sutE = TT.CDFEpochtoDate(sEpochE)



		#replace bad data
		fields = {	'FPSA' : 	('H+','Energy (keV)',r'H$^+$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','H'),
					'FHESA' : 	('He+','Energy (keV)',r'He$^+$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','He'),
					'FOSA' : 	('O+','Energy (keV)',r'O$^+$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','O'),
					'FESA' : 	('e','Energy (keV)',r'e Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','e'),}
		
		for k in list(fields.keys()):
			s = data[k]
			bad = np.where(s < 0)
			s[bad] = np.nan
			
			#get the base field name
			kout,ylabel,zlabel,spectype = fields[k]
			
			#output spectra fields name
			kspec = kout + 'Flux'
			
		
			#select the appropriate time/date and energy
			if k == 'FESA':
				sEpoch,sDate,sut = sEpochE,sDateE,sutE
				ke = data['HOPE_ENERGY_Ele']/1000.0
				kde = data['ENERGY_Ele_DELTA']/1000.0
			else:
				sEpoch,sDate,sut = sEpochI,sDateI,sutI
				ke = data['HOPE_ENERGY_Ion']/1000.0
				kde = data['ENERGY_Ion_DELTA']/1000.0
			if RemoveBinOverlap:
				kde = None
			E0,E1,Em = ProcessEnergyBins(ke,kde)
			
			
			#now to store the spectra
			if out[kspec] is None:
				out[kspec] = PSpecCls(SpecType=spectype,ylabel=ylabel,zlabel=zlabel,ScaleType='positive',ylog=True,zlog=True)
			out[kspec].AddData(sDate,sut,sEpoch,E0,E1,Em,s,Meta=meta[k],Label='HOPE')
			

	return out	
