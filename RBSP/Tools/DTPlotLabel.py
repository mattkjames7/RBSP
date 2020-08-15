import numpy as np
import DateTimeTools as TT

def DTPlotLabel(fig,ut,date,Seconds=False,IncludeYear=True,TickFreq='default'):
	'''
	Simple subroutine to convert the time axis of a plot to show human 
	readable times and dates, hopefully!
	
	Inputs:
		fig: Either an instance of pyplot or pyplot.Axes passed to the 
			function, useful for plotting multiple figures on one page,
			or overplotting
		ut: Array of time values plotted against.
		date: Array of date integers in the format yyyymmdd 
			corresponding to the times in ut.
		Seconds: Show seconds in the time format.
		IncludeYear: Show the year in the date.  
	'''
	
	if hasattr(fig,'gca'):
		ax = fig.gca()
	else:
		ax = fig
		
	if TickFreq == 'default':
		#use existing ticks
		mt = ax.xaxis.get_majorticklocs()
	else:
		trnge = ax.get_xlim()
		tlen = (trnge[1] - trnge[0])
		#set the tick frequency in hours
		if TickFreq == 'auto':
			tfs = np.array([1440.0,720.0,360.0,240.0,180.0,120.0,60.0,30.0,15.0,10.0,5.0,2.0,1.0])
			dtf = np.abs(60.0*tlen/tfs - 5.0)
			use = np.where(dtf == np.min(dtf))[0][0]
			tf = tfs[use]/60.0
		else: 
			#use custom tick frequency
			tf = TickFreq
		#work out the tick values
		mt0 = tf * np.int32(trnge[0]/tf)
		mt1 = tf * (np.int32(trnge[1]/tf) + 1)
		mt = np.arange(mt0,mt1+tf,tf)
		use = np.where((mt >= trnge[0]) & ( mt <= trnge[1]))[0]
		mt = mt[use]
		
	#get tick ut and dates
	tickut = mt % 24.0		
	ut0 = np.floor(ut[0]/24.0)*24.0
	tickdate = np.zeros(mt.size,dtype='int32')
	datediff = np.int32(np.floor((mt - ut0)/24.0))
	udd = np.unique(datediff)
	for u in udd:
		d = np.copy(date[0])
		use = np.where(datediff == u)[0]
		if u == 0:
			tickdate[use] = d
		else:
			if u < 0:
				func = TT.MinusDay
			else:
				func = TT.PlusDay
				
			for i in range(0,np.abs(u)):
				d = func(d)
			
			tickdate[use] = d
	
			
	labels = np.zeros(mt.size,dtype='U20')
	Months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	for i in range(0,mt.size):
		
		yr,mn,dy = TT.DateSplit(tickdate[i])
		datestr = '{:02d} '.format(np.int(dy))+Months[mn-1]
		if IncludeYear:
			datestr += '\n{:04d}'.format(yr)
		
		hh,mm,ss,ms = TT.DectoHHMM(tickut[i],True,True,True)
		if Seconds:
			utstr='{:02n}:{:02n}:{:02n}'.format(hh,mm,ss)
		else:
			if ss >= 30:
				mm+=1
				ss = 0
			if mm > 59:
				hh+=1
				mm=0
			if hh > 23:
				hh = 0
			utstr = '{:02n}:{:02n}'.format(hh,mm)
		labels[i] = utstr+'\n'+datestr

	R = fig.axis()
	use = np.where((mt >= R[0]) & (mt <= R[1]))[0]
	ax.set_xticks(mt[use])
	ax.set_xticklabels(labels[use])
