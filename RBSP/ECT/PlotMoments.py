from .ReadCDF import ReadCDF
import matplotlib.pyplot as plt
import numpy as np


def _FillBadDens(t,n):
	badT = '0000-01-01T00:00:00.000'
	tstr = t.astype('U')
	
	bad = np.where((n < -0.9e-31))[0]
	n[bad] = np.nan
	
	gd = np.where(tstr != badT)[0]
	return t[gd],10**n[gd]

def PlotMoments(Date,sc='a',ylog=False,fig=None,maps=[1,1,0,0]):
	'''
	Plot HOPE level 3 moments.
	
	'''
	data,meta = ReadCDF(Date,sc,'hope','l3.moments')
	
	ut_e = data['Epoch_Ele']
	ut_i = data['Epoch_Ion']
	
	
	n_e = data['Dens_e_200']
	n_he = data['Dens_he_30']
	n_o = data['Dens_o_30']
	n_p = data['Dens_p_30']
	n_i = data['Ion_density']
	
	te,n_e = _FillBadDens(ut_e,n_e)
	ti,n_he = _FillBadDens(ut_i,n_he)
	ti,n_o = _FillBadDens(ut_i,n_o)
	ti,n_p = _FillBadDens(ut_i,n_p)
	ti,n_i = _FillBadDens(ut_i,n_i)

	if fig is None:
		fig = plt
		fig.figure()
	ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
	
	ax.plot(te,n_e,label='$n_e$')
	#ax.plot(ti,n_p,label='$n_H$')
	#ax.plot(ti,n_he,label='$n_{He}$')
	#ax.plot(ti,n_o,label='$n_O$')
	ax.plot(ti,n_i,label='$n_i$')
	#ax.plot(ti,n_o + n_p + n_he,label='Sum')

	ax.legend()
