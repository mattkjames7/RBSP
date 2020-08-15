import numpy as np
import DateTimeTools as TT

def ListDates(Date0,Date1):
	'''
	Creates an array of dates from Date0 to Date1
	
	'''
	dates = []
	date = np.copy(Date0)
	dates.append(date)
	while date < Date1:
		date = TT.PlusDay(date)
		dates.append(date)
	dates = np.array(dates)
	return dates
