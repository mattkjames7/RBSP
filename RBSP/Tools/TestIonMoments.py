import numpy as np
import matplotlib.pyplot as plt
from .. import ECT
import DateTimeTools as TT

def TestIonMoments(Date=20130115,sc='a',MaxE=0.02):
	
	#get the data in
	if MaxE == 0.02:
		data = ECT.ReadIonMoments(Date,sc)
	else:
		data = ECT.CalculateIonMoments(Date,sc,MaxE)
	
	#replace zeros with nan
	fields = ['H_n_c','He_n_c','O_n_c','H_T_c','He_T_c','O_T_c',]
	for f in fields:
		use = np.where(data[f] == 0)[0]
		data[f][use] = np.nan
		
	#create the figure
	fig = plt
	fig.figure(figsize=(9,11))
	
	#Protons
	ax0 = fig.subplot2grid((4,2),(0,0))
	ax0.plot(data.utc,data.H_n_c[:,0]/1e6,color=[0.4,0.0,0.0,0.7],label='H$^+_0$')
	ax0.plot(data.utc,data.H_n_c[:,1]/1e6,color=[1.0,0.0,0.0,0.7],label='H$^+_1$')
	ax0.set_ylim(0.1,10000.0)
	ax0.set_yscale('log')
	ax0.set_ylabel('$n_H$ (cm$^{-3}$)')
	ax0.set_xlabel('')
	ax0.set_xticks([])
	
	ax1 = fig.subplot2grid((4,2),(0,1))
	ax1.plot(data.utc,data.H_T_c[:],color=[1.0,0.0,0.0,0.7],label='H$^+$')
	ax1.set_ylim(1000.0,1000000.0)
	ax1.set_yscale('log')
	ax1.set_ylabel('$T_H$ (K)')
	ax1.set_xlabel('')
	ax1.set_xticks([])
	
	#Helium
	ax2 = fig.subplot2grid((4,2),(1,0))
	ax2.plot(data.utc,data.He_n_c[:,0]/1e6,color=[0.0,0.4,0.0,0.7],label='He$^+_0$')
	ax2.plot(data.utc,data.He_n_c[:,1]/1e6,color=[0.0,1.0,0.0,0.7],label='He$^+_1$')
	ax2.set_ylim(0.01,4000.0)
	ax2.set_yscale('log')
	ax2.set_ylabel('$n_{He}$ (cm$^{-3}$)')
	ax2.set_xlabel('')
	ax2.set_xticks([])
	
	ax3 = fig.subplot2grid((4,2),(1,1))
	ax3.plot(data.utc,data.He_T_c[:],color=[0.0,1.0,0.0,0.7],label='He$^+$')
	ax3.set_ylim(1000.0,1000000.0)
	ax3.set_yscale('log')
	ax3.set_ylabel('$T_{He}$ (K)')
	ax3.set_xlabel('')
	ax3.set_xticks([])
	
	#Oxygen
	ax4 = fig.subplot2grid((4,2),(2,0))
	ax4.plot(data.utc,data.O_n_c[:,0]/1e6,color=[0.0,0.0,0.4,0.7],label='O$^+_0$')
	ax4.plot(data.utc,data.O_n_c[:,1]/1e6,color=[0.0,0.0,1.0,0.7],label='O$^+_1$')
	ax4.set_ylim(0.01,4000.0)
	ax4.set_yscale('log')
	ax4.set_ylabel('$n_{O}$ (cm$^{-3}$)')
	ax4.set_xlabel('')
	ax4.set_xticks([])
	
	ax5 = fig.subplot2grid((4,2),(2,1))
	ax5.plot(data.utc,data.O_T_c[:,0],color=[0.0,0.0,0.4,0.7],label='O$^+_0$')
	ax5.plot(data.utc,data.O_T_c[:,1],color=[0.0,0.0,1.0,0.7],label='O$^+_1$')
	ax5.set_ylim(200.0,5000000.0)
	ax5.set_yscale('log')
	ax5.set_ylabel('$T_{O}$ (K)')
	ax5.set_xlabel('')
	ax5.set_xticks([])
	
	#Mav
	ax6 = fig.subplot2grid((4,2),(3,1))
	ax6.plot(data.utc,data.Mav_c[:,0],color=[0.5,0.0,1.0],label='$m_{av0}$')
	ax6.plot(data.utc,data.Mav_c[:,1],color=[0.2,0.0,0.7],label='$m_{av1}$')
	ax6.set_ylim(1.0,16.0)
	ax6.set_ylabel('$m_{av}$ (amu)')
	TT.DTPlotLabel(ax6)
	
	#Ebulk
	ax7 = fig.subplot2grid((4,2),(3,0))
	ax7.plot(data.utc,data.H_Ebulk*1000.0,color=[1.0,0.0,0.0,0.7],label='H$^+$')
	ax7.plot(data.utc,data.He_Ebulk*1000.0,color=[0.0,1.0,0.0,0.7],label='He$^+$')
	ax7.plot(data.utc,data.O_Ebulk*1000.0,color=[0.0,0.0,1.0,0.7],label='O$^+$')
	ax7.set_ylim(0.001,10.0)
	ax7.set_yscale('log')
	ax7.set_ylabel('$E_{bulk}$ (eV)')
	TT.DTPlotLabel(ax7)	
	
	ax0.legend()
	ax1.legend()
	ax2.legend()
	ax3.legend()
	ax4.legend()
	ax5.legend()
	ax6.legend()
	ax7.legend()

	plt.subplots_adjust(hspace=0.0)



def IonMomentHist(Date,sc):
	
	#read the moments in
	data = ECT.ReadIonMoments(Date,sc)
	
	#create a plot
	plt.figure()
	plt.hist(data.Mav_c[:,0],histtype='step',bins=np.linspace(1.0,16.0,60),label='$m_{avc0}$')
	plt.hist(data.Mav_c[:,1],histtype='step',bins=np.linspace(1.0,16.0,60),label='$m_{avc1}$')
	plt.hist(np.mean(data.Mav_c,axis=1),histtype='step',bins=np.linspace(1.0,16.0,60),label='$m_{avc}$')
	plt.legend()
	
	
	
def _PlotRange(ax,x,y0,y1,color,label):
	'''
	This will plot a shaded area between a range of values.
	
	'''
	ax.scatter(x,y1,s=2,color=color,label=label)
	ax.scatter(x,y0,s=0.1,color=color)


	good = np.where(np.isfinite(y0))[0]
	xf = x[good]
	yf0 = y0[good]
	yf1 = y1[good]

	
	#find gaps
	maxgap = 5/60.0
	dt = xf[1:] - xf[:-1]
	gaps = np.where(dt > maxgap)[0]
	if gaps.size == 0:
		i0 = np.array([0])
		i1 = np.array([xf.size])
	else:
		i0 = np.append(0,gaps+1)
		i1 = np.append(gaps+1,xf.size)
	ni = i0.size

	
	for i in range(0,ni):
		inds = np.arange(i0[i],i1[i])

		xp = np.append(xf[inds],xf[inds][::-1])
		yp = np.append(yf0[inds],yf1[inds][::-1])		
		fillcolor = np.append(color,[0.2])
		ax.fill(xp,yp,color=fillcolor)


def G2019f3(MaxE=0.02):
	
	#get the data in
	if MaxE == 0.02:
		data = ECT.ReadIonMoments(20130115,'a')
	else:
		data = ECT.CalculateIonMoments(20130115,'a',MaxE)
	
	#replace zeros with nan
	fields = ['H_n_c','He_n_c','O_n_c','H_T_c','He_T_c','O_T_c',]
	for f in fields:
		use = np.where(data[f] == 0)[0]
		data[f][use] = np.nan
	
	#get the quantities we need
	
	#electrons and ions
	utlim = TT.ContUT(np.array([20130115,20130115]),np.array([0.0,4.867]))
	ut = data.utc
	ne = data.ne/1e6
	ni = data.ni_c/1e6
	
	#scale factor
	scale = ni/ne
	
	#original ion densities
	Hn0 = data.H_n_c[:,0]*scale/1e6
	Hen0 = data.He_n_c[:,0]*scale/1e6
	On0 = data.O_n_c[:,0]*scale/1e6
	
	#new ion densities
	Hn_a = data.H_n_c[:,0]/1e6
	Hn_b = data.H_n_c[:,1]/1e6
	Hen_a = data.He_n_c[:,0]/1e6
	Hen_b = data.He_n_c[:,1]/1e6
	On_a = data.O_n_c[:,0]/1e6
	On_b = data.O_n_c[:,1]/1e6
	
	#oxygen temp
	kB = np.float64(1.38064852e-23)
	e = np.float64(1.6022e-19)
	OTl = data.O_T_c[:,0]*kB/e
	OTh = data.O_T_c[:,1]*kB/e
	
	
	#mav
	mav0 = np.nanmin(data.Mav_c,axis=1)
	mav1 = np.nanmax(data.Mav_c,axis=1)
	
	#Energy
	Emin = data.Emin*1e3
	H_Eb = data.H_Ebulk*1e3
	He_Eb = data.He_Ebulk*1e3
	O_Eb = data.O_Ebulk*1e3
		
	#create the figure
	fig = plt
	fig.figure(figsize=(8,11))
	plt.subplots_adjust(hspace=0.0)
	
	#Top plot
	ax0 = fig.subplot2grid((9,1),(0,0),rowspan=3)
	ax0.set_xlim(utlim)
	ax0.set_ylim(0.002,5000)
	ax0.scatter(ut,ne,s=2.0,color=[0.0,0.0,0.0],label='$n_e$')
	ax0.scatter(ut,Hn0,s=2.0,color=[1.0,0.0,0.0],label='$n_{H+}$')
	ax0.scatter(ut,Hen0,s=2.0,color=[0.0,1.0,0.0],label='$n_{He+}$')
	ax0.scatter(ut,On0,s=2.0,color=[0.0,1.0,1.0],label='$n_{O+}$')
	_PlotRange(ax0,ut,OTl,OTh,[1.0,0.0,1.0],'$T_{O+}$')
	ax0.set_yscale('log')
	ax0.set_xticklabels(['']*len(ax0.get_xticklabels()))
	ax0.set_ylabel('cm$^{-3}$ or eV')
	ax0.legend(loc='upper right')

	#bottom plot
	ax1 = fig.subplot2grid((9,1),(3,0),rowspan=2)
	ax1.set_xlim(utlim)
	ax1.set_ylim(0.1,5000)
	ax1.scatter(ut,ne,s=2.0,color=[0.0,0.0,0.0],label='$n_e$')
	ax1.scatter(ut,Hn_a,s=2.0,color=[1.0,0.0,0.0],label='$n_{H+}$')
	ax1.scatter(ut,Hen_a,s=2.0,color=[0.0,1.0,0.0],label='$n_{He+}$')
	_PlotRange(ax1,ut,On_b,On_a,[0.0,1.0,1.0],'$n_{O+}$')
	ax1.set_yscale('log')
	ax1.set_xticklabels(['']*len(ax1.get_xticklabels()))
	ax1.set_ylabel('cm$^{-3}$')
	ax1.legend(loc='upper right')
	
	#extra plot: Emin,Emax,E_Bulk
	ax2 = fig.subplot2grid((9,1),(5,0),rowspan=2)
	ax2.set_xlim(utlim)
	ax2.scatter(ut,Emin,s=2.0,color=[0.0,0.0,0.0],label='$E_{min}$')
	ax2.scatter(ut,H_Eb,s=2.0,color=[1.0,0.0,0.0],label='$E_{bulk}$ (H$^+$)')
	ax2.scatter(ut,He_Eb,s=2.0,color=[0.0,1.0,0.0],label='$E_{bulk}$ (He$^+$)')
	ax2.scatter(ut,O_Eb,s=2.0,color=[0.0,1.0,1.0],label='$E_{bulk}$ (O$^+$)')	
	ax2.set_xticklabels(['']*len(ax1.get_xticklabels()))
	ax2.legend(loc='upper right')
	ax2.set_ylabel('eV')
	
	#extra plot: Mav
	ax3 = fig.subplot2grid((9,1),(7,0),rowspan=2)
	_PlotRange(ax3,ut,mav0,mav1,[1.0,0.5,0.0],'$m_{av}$')
	ax3.set_ylim(1.0,16.0)
	ax3.set_xlim(utlim)
	ax3.legend(loc='upper right')
	ax3.set_ylabel('amu')
	TT.DTPlotLabel(ax3)

	plt.savefig('G2019f3-{:05.3f}.png'.format(MaxE))
