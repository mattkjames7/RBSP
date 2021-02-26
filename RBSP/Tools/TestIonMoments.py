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
