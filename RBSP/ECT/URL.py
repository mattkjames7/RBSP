from .. import Globals 
import time
import os
import numpy as np

def URL(sc,Inst,L):
	'''
	Returns a function which works out the URLs for a given date
	
	Inputs
	======
	sc : str
		'a' or 'b'
	Inst: str
		'hope', 'mageis' or 'rept' 
	L : str
		Level of data to download



	Available data products
	=======================
	hope: 'l2.sectors'|'l2.spinaverage'|'l3.moments'|'l3.pitchangle'
	mageis: 'l2'|'l3'
	rept: 'l2'|'l3'
	
	Returns
	=======
	urls,fnames
	'''
	
	def URLFunction(Date):
	
		#get the year
		Year = Date//10000
		
		
		#first let's get the url which will contain the link to the cdf file
		if Inst == 'hope':
			l = L.split('.')
		elif Inst == 'mageis':
			if L == 'l3':
				l = [L,'pitchangle']
			else:
				l = [L,'sectors']
		else:
			if L == 'l3':
				l = [L,'pitchangle']
			else:
				l = [L,'sectors']
		l[0] = l[0].replace('l','level')
		url0 = 'https://www.rbsp-ect.lanl.gov/data_pub/rbsp{:s}/{:s}/{:s}/{:s}/{:4d}/'.format(sc,Inst,l[0],l[1],Year)
		return url0
	
	return URLFunction

