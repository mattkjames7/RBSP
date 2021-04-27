import matplotlib.pyplot as plt
import numpy as np
from .ReadIonMoments import ReadIonMoments
from ..Pos import GetPos
import DateTimeTools as TT
from scipy.interpolate import interp1d
from ..Pos.PlotL import PlotL
from ..Pos.PlotMLT import PlotMLT

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

	srt = np.argsort(xf)
	xf = xf[srt]
	yf0 = yf0[srt]
	yf1 = yf1[srt]
	
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
		inds = np.arange(i0[i],i1[i]-1)

		xp = np.append(xf[inds],xf[inds][::-1])
		yp = np.append(yf0[inds],yf1[inds][::-1])		
		fillcolor = np.append(color,[0.2])
		ax.fill(xp,yp,color=fillcolor)


	
def _GetPPtimes(x,R,ne):
	
	
	nb = 10.0*(6.6/R)**4			
	ps = (ne > nb) | (R < 2)
	pt = (ne <= nb) & (R >= 2)
	
	ispp = (ps[:-1] & pt[1:]) | (pt[:-1] & ps[1:])
	

	
	ipp0 = np.where(ispp)[0]
	ipp1 = ipp0 + 1
	
	
	
	x0 = x[ipp0]
	x1 = x[ipp1]

	
	maxgap = 5/60.0

	good = np.where((x1 - x0) <= maxgap)[0]

	if good.size == 0:
		return np.array([])
	
	return 0.5*(x0[good] + x1[good])


def PlotDensity(Date,sc,ut=[0.0,24.0],ylog=True,fig=None,maps=[1,1,0,0],
	colspan=1,rowspan=1,
	ShowPP=True,ListPP=True,ReturnPP=True,yrnge=[0.1,5000.0],loc=None,
	ShowSheeley2001=True,nox=False):
	
	#read the data in
	data = ReadIonMoments(Date,sc)
	
	#get date and time limits
	date0 = np.nanmin(Date)
	date1 = np.nanmax(Date)
	utc0 = TT.ContUT(date0,ut[0])
	utc1 = TT.ContUT(date1,ut[1])
	
	#create the figure
	if fig is None:
		fig = plt
		fig.figure()
	ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]),colspan=colspan,rowspan=rowspan)	
	
	#plot each particle
	
	#electrons
	ax.scatter(data.utc,data.ne/1e6,s=1.0,color=[0.0,0.0,0.0],label='$n_e$')
	
	#protons
	ax.scatter(data.utc,data.H_n_c[:,0]/1e6,s=1.0,color=[1.0,0.0,0.0],label='$n_{H+}$')
	
	#helium
	ax.scatter(data.utc,data.He_n_c[:,0]/1e6,s=1.0,color=[0.0,1.0,0.0],label='$n_{He+}$')
	
	#oxygen
	Omax = np.nanmax(data.O_n_c/1e6,axis=1)
	Omin = np.nanmin(data.O_n_c/1e6,axis=1)
	_PlotRange(ax,data.utc,Omin,Omax,[0.0,1.0,1.0],'$n_{O+}$')
	
	#set axis limits
	ax.set_xlim([utc0,utc1])
	ax.set_ylim(yrnge)
	if ylog:
		ax.set_yscale('log')
	
	#set axis labels
	TT.DTPlotLabel(ax)
	ax.set_xlabel('UT')
	ax.set_ylabel('cm$^{-3}$')
	if nox:
		xt = ax.get_xticks()
		ax.set_xticklabels(['']*np.size(xt))
		ax.set_xlabel('')
	
	if ShowPP:
		pos = GetPos(sc)
		use = np.where((pos.utc >= utc0) & (pos.utc <= utc1))[0]
		pos = pos[use]
		R = np.sqrt(pos.Xsm**2 + pos.Ysm**2 + pos.Zsm**2)
		fR = interp1d(pos.utc,R,bounds_error=False)
		fx = interp1d(pos.utc,pos.Xsm,bounds_error=False)
		fy = interp1d(pos.utc,pos.Ysm,bounds_error=False)
		R = fR(data.utc)
		
		pputc = _GetPPtimes(data.utc,R,data.ne/1e6)
		
		ax.vlines(pputc,yrnge[0],yrnge[1],color=[1.0,0.6,0.0,0.3],label='PP Crossing')
		
		if ListPP:
			dpp,tpp = TT.ContUTtoDate(pputc)
			hh,mm,ss,_ = TT.DectoHHMM(tpp)
			L = fR(pputc)
			x = fx(pputc)
			y = fy(pputc)
			M = np.arctan2(-y,-x)*12.0/np.pi
			print('Possible PP Crossings')
			print('   Date  -    UT    |   L   |  MLT')
			print('--------------------------------------')
			for i in range(0,pputc.size):
				print('{:08d} - {:02d}:{:02d}:{:02d} | {:5.3f} | {:6.3f}'.format(dpp[i],hh[i],mm[i],ss[i],L[i],M[i]))
				
	if ShowSheeley2001:
		sutc = np.linspace(utc0,utc1,1000)
		pos = GetPos(sc)
		use = np.where((pos.utc >= utc0) & (pos.utc <= utc1))[0]
		pos = pos[use]
		R = np.sqrt(pos.Xsm**2 + pos.Ysm**2 + pos.Zsm**2)
		fR = interp1d(pos.utc,R,bounds_error=False)
		L = fR(sutc)
		nb = 10.0*(6.6/L)**4
		
		ax.plot(sutc,nb,color='pink',linestyle='--',label='$n_b$ (Sheeley et al 2001)')
						
	ax.legend(loc=loc)
	
	if ShowPP and ReturnPP:
		return ax,pputc
	else:
		return ax
	
def PlotTemp(Date,sc,ut=[0.0,24.0],ylog=True,fig=None,maps=[1,1,0,0],
	colspan=1,rowspan=1,
	ShowPP=True,ListPP=True,ReturnPP=True,yrnge=[1000,1e6],loc=None,nox=False):
	
	#read the data in
	data = ReadIonMoments(Date,sc)
	
	#get date and time limits
	date0 = np.nanmin(Date)
	date1 = np.nanmax(Date)
	utc0 = TT.ContUT(date0,ut[0])
	utc1 = TT.ContUT(date1,ut[1])
	
	#create the figure
	if fig is None:
		fig = plt
		fig.figure()
	ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]),colspan=colspan,rowspan=rowspan)	
	
	#plot each particle
	
	#protons
	ax.scatter(data.utc,data.H_T_c,s=1.0,color=[0.7,0.25,0.0],label='$T_{H+}$')
	
	#helium
	ax.scatter(data.utc,data.He_T_c,s=1.0,color=[0.0,0.0,1.0],label='$T_{He+}$')
	
	#oxygen
	Omax = np.nanmax(data.O_T_c,axis=1)
	Omin = np.nanmin(data.O_T_c,axis=1)
	_PlotRange(ax,data.utc,Omin,Omax,[1.0,0.0,1.0],'$T_{O+}$')
	
	#set axis limits
	ax.set_xlim([utc0,utc1])
	ax.set_ylim(yrnge)
	if ylog:
		ax.set_yscale('log')
	
	#set axis labels
	TT.DTPlotLabel(ax)
	ax.set_xlabel('UT')
	ax.set_ylabel('K')
	if nox:
		xt = ax.get_xticks()
		ax.set_xticklabels(['']*np.size(xt))
		ax.set_xlabel('')
		
	if ShowPP:
		pos = GetPos(sc)
		use = np.where((pos.utc >= utc0) & (pos.utc <= utc1))[0]
		pos = pos[use]
		R = np.sqrt(pos.Xsm**2 + pos.Ysm**2 + pos.Zsm**2)
		fR = interp1d(pos.utc,R,bounds_error=False)
		fx = interp1d(pos.utc,pos.Xsm,bounds_error=False)
		fy = interp1d(pos.utc,pos.Ysm,bounds_error=False)
		R = fR(data.utc)
		
		pputc = _GetPPtimes(data.utc,R,data.ne/1e6)
		
		ax.vlines(pputc,yrnge[0],yrnge[1],color=[1.0,0.6,0.0,0.3],label='PP Crossing')
		
		if ListPP:
			dpp,tpp = TT.ContUTtoDate(pputc)
			hh,mm,ss,_ = TT.DectoHHMM(tpp)
			L = fR(pputc)
			x = fx(pputc)
			y = fy(pputc)
			M = np.arctan2(-y,-x)*12.0/np.pi
			print('Possible PP Crossings')
			print('   Date  -    UT    |   L   |  MLT')
			print('--------------------------------------')
			for i in range(0,pputc.size):
				print('{:08d} - {:02d}:{:02d}:{:02d} | {:5.3f} | {:6.3f}'.format(dpp[i],hh[i],mm[i],ss[i],L[i],M[i]))
				
						
	ax.legend(loc=loc)
	
	if ShowPP and ReturnPP:
		return ax,pputc
	else:
		return ax	
	
	return ax
	
def PlotMav(Date,sc,ut=[0.0,24.0],ylog=False,fig=None,maps=[1,1,0,0],
	colspan=1,rowspan=1,
	ShowPP=True,ListPP=True,ReturnPP=False,yrnge=[1.0,16.0],loc=None,
	nox=False):

	#read the data in
	data = ReadIonMoments(Date,sc)
	
	#get date and time limits
	date0 = np.nanmin(Date)
	date1 = np.nanmax(Date)
	utc0 = TT.ContUT(date0,ut[0])
	utc1 = TT.ContUT(date1,ut[1])
	
	#create the figure
	if fig is None:
		fig = plt
		fig.figure()
	ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]),colspan=colspan,rowspan=rowspan)	
	
	#get Mav
	Mav0 = np.nanmin(data.Mav_c,axis=1)
	Mav1 = np.nanmax(data.Mav_c,axis=1)
	
	#plot Mav
	_PlotRange(ax,data.utc,Mav0,Mav1,[1.0,0.7,0.0],'$m_{av}$')
	
	#set axis limits
	ax.set_xlim([utc0,utc1])
	ax.set_ylim(yrnge)
	if ylog:
		ax.set_yscale('log')
	
	#set axis labels
	TT.DTPlotLabel(ax)
	ax.set_xlabel('UT')
	ax.set_ylabel('amu')
	if nox:
		xt = ax.get_xticks()
		ax.set_xticklabels(['']*np.size(xt))
		ax.set_xlabel('')
	
	if ShowPP:
		pos = GetPos(sc)
		use = np.where((pos.utc >= utc0) & (pos.utc <= utc1))[0]
		pos = pos[use]
		R = np.sqrt(pos.Xsm**2 + pos.Ysm**2 + pos.Zsm**2)
		fR = interp1d(pos.utc,R,bounds_error=False)
		fx = interp1d(pos.utc,pos.Xsm,bounds_error=False)
		fy = interp1d(pos.utc,pos.Ysm,bounds_error=False)
		R = fR(data.utc)
		
		pputc = _GetPPtimes(data.utc,R,data.ne/1e6)
		
		ax.vlines(pputc,yrnge[0],yrnge[1],color='yellowgreen',alpha=0.3,label='PP Crossing')
		
		if ListPP:
			dpp,tpp = TT.ContUTtoDate(pputc)
			hh,mm,ss,_ = TT.DectoHHMM(tpp)
			L = fR(pputc)
			x = fx(pputc)
			y = fy(pputc)
			M = np.arctan2(-y,-x)*12.0/np.pi
			print('Possible PP Crossings')
			print('   Date  -    UT    |   L   |  MLT')
			print('--------------------------------------')
			for i in range(0,pputc.size):
				print('{:08d} - {:02d}:{:02d}:{:02d} | {:5.3f} | {:6.3f}'.format(dpp[i],hh[i],mm[i],ss[i],L[i],M[i]))
				
						
	ax.legend(loc=loc)
	
	if ShowPP and ReturnPP:
		return ax,pputc
	else:
		return ax
	
def PlotMoments(Date,sc,ut=[0.0,24.0],ylog=True,fig=None,
	ShowPP=True,ListPP=True,ReturnPP=True,yrnge=[0.1,5000.0],
	loc='upper right',ShowSheeley2001=True,nox=False,ShowPos=True,ShowMav=True):
	'''
	Plot HOPE level 3 moments.
	
	'''

	if fig is None:
		fig = plt
		fig.figure(figsize=(11,8))
	
	if ShowPos:
		ny = 6
		nox1 = True
	else:
		ny = 4
		nox1 = False
	
	if ShowMav:
		ny += 2
		dypos = 2
		nox1 = True
	else:
		dypos = 0
		
	ax0 = PlotDensity(Date,sc,ut=ut,fig=fig,maps=[1,ny,0,0],ShowPP=ShowPP,ListPP=ListPP,ReturnPP=ReturnPP,loc=loc,ShowSheeley2001=ShowSheeley2001,nox=True,rowspan=2)
	ax1 = PlotTemp(Date,sc,ut=ut,fig=fig,maps=[1,ny,0,2],ShowPP=ShowPP,ListPP=False,ReturnPP=ReturnPP,loc=loc,rowspan=2,nox=nox1)
	
	if ReturnPP:
		ax0,pputc = ax0
		ax1,pputc = ax1
	else:
		pputc = None
	axes = [ax0,ax1]
	if ShowMav:
		axm = PlotMav(Date,sc,ut=ut,fig=fig,maps=[1,ny,0,4],ShowPP=ShowPP,ListPP=False,ReturnPP=False,loc=loc,rowspan=2,nox=ShowPos)
		axes.append(axm)
	
	if ShowPos:
		ax2 = PlotL(Date,sc,ut=ut,fig=fig,maps=[1,ny,0,4+dypos],nox=True)
		ax3 = PlotMLT(Date,sc,ut=ut,fig=fig,maps=[1,ny,0,5+dypos])
		axes.append(ax2)
		axes.append(ax3)
		if ShowPP and ReturnPP:
			y2 = ax2.get_ylim()
			ax2.vlines(pputc,y2[0],y2[1],color=[1.0,0.6,0.0,0.3])
			y3 = ax3.get_ylim()
			ax3.vlines(pputc,y3[0],y3[1],color=[1.0,0.6,0.0,0.3])
		
		
	plt.subplots_adjust(hspace=0.0)
	
	return axes
