import numpy as np
import matplotlib.pyplot as plt
from .ReadFieldTraces import ReadFieldTraces
import DateTimeTools as TT

def PlotMLT(Date,sc,ut=[0.0,24.0],fig=None,maps=[1,1,0,0],nox=False):
	
	#read the positions in
	data = ReadFieldTraces(Date,sc)
	
	#get a time range
	date0 = np.nanmin(Date)
	date1 = np.nanmax(Date)
	utc0 = TT.ContUT(date0,ut[0])[0]
	utc1 = TT.ContUT(date1,ut[1])[0]
			
	#select appropriate data
	use = np.where((data.utc >= utc0) & (data.utc <= utc1))[0]
	data = data[use]
			
			
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
	else:
		ax = fig

	ax.plot(data.utc,data.MltE,color='green')
	
	
	ax.set_ylim(0.0,24.0)
	ax.set_xlim(utc0,utc1)
	TT.DTPlotLabel(ax)
	
	ax.set_ylabel('MLT')
	ax.set_xlabel('UT')
	ax.set_yticks(np.arange(6,24,6))
	
	ax.hlines(np.arange(6,24,6),utc0,utc1,color=[0.0,0.0,0.0,0.25],linestyle=':')
	
	if nox:
		xt = ax.get_xticks()
		ax.set_xticklabels(['']*np.size(xt))
	

	return ax
