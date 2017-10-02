#!/usr/bin/python
#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

import ephem as ep
import time
from time import gmtime, strftime
import datetime
import numpy as np
from numpy import linalg as la
from math import pi,acos,asin,sin,cos,sqrt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.dates as md
np.set_printoptions(threshold=np.nan)
import sys
import subprocess as sp
import re

def GreatCircleDistance(l1, b1, l2, b2):
	x = cos(l2)*cos(b2) - cos(l1)*cos(b1)
	y = sin(l2)*cos(b2) - sin(l1)*cos(b1)
	z = sin(b2) - sin(b1)
	chordLength = sqrt( x**2 + y**2 + z**2 )
	distance = 2*asin(chordLength/2)
	return distance


with open('WebGSE_GPStrack_flightOP.dat') as f:
        data = f.read()

data2 = data.strip().split(' \n')
columnNum = len(data2)
DATA = [[0]*20 for i in range(columnNum)]
for j in range(0,columnNum):
        DATA[j] = re.split(r'[  | ]\s*',data2[j])

num_comp = 20
trackfile = {k: [] for k in range(0,num_comp+1)}
cosiposition = [[0,0,0] for i in range(0,columnNum)]
trackcheck = [[0,0,0] for i in range(0,columnNum)]
for l in range(0,columnNum):
	if DATA[l][0] != '':
		for m in range(0,num_comp):
			try:		                        
				trackfile[m].append(float(DATA[l][m]))
			except(ValueError,IndexError):
				continue

for l in range(0,columnNum):
	cosiposition[l][0] = trackfile[0][l]	#time
	cosiposition[l][1] = trackfile[3][l]	#lon
	cosiposition[l][2] = trackfile[4][l]	#lat
#init_time = "23:45:00"
#init_time = "00:09:00"
#init_date = "2014/12/20 "
#init_date = "2016/04/06 "

var = 0
lines = len(cosiposition)  
columnNum = 1 + var

sun_list = []
source_list = []
tstring_list = []

###########  edit here  #############
starttime = 1463441700	# unix time you want to start with, time when COSI launched 1463441700
endtime   = 1467478260	# unix time you want to end with, time when COSI landed 1467478260
source_l  = 263.552021	# galactic lontitude of your source
source_b  = -2.787006	# galactic latitude of your source
#####################################
source_l = source_l * pi/180 # convert to raidan
source_b = source_b * pi/180 # convert to radian

unixtime1 = 0
unixtime_sum = 0	

while columnNum < lines:
	
	init_lat, init_lon = cosiposition[columnNum][2]*(pi/180.0), cosiposition[columnNum][1]*(pi/180.0) #NOT a location
    
	# Convert Unix Time  
	unixtime = int(cosiposition[columnNum][0])
	init_time = str(strftime('%H:%M:%S',gmtime(unixtime)))
	init_date = str(strftime('%Y/%m/%d ',gmtime(unixtime)))
	init_dt = str(strftime('%Y/%m/%d-%H:%M:%S',gmtime(unixtime)))

	#initialize parameters for the ephemeris calculations
	interval = float(cosiposition[columnNum][0]-cosiposition[columnNum-1][0]) #number of seconds 
	if unixtime< starttime:
		columnNum +=1		
		continue
	elif interval == 0:
		columnNum +=1		
		continue
	elif (cosiposition[columnNum][2] == 0 and cosiposition[columnNum][1] == 0):
#	elif (init_lat ==0 and init_lon==0):
		columnNum +=1		
		continue
	else: 
		num_intervals_per_day = 1.
		
		timest = time.strptime(init_date + init_time,"%Y/%m/%d %H:%M:%S")
		nct = ep.Observer()
		nct.lat, nct.lon = init_lat, init_lon
		
	
		#represents the Sun position
		sun_nct = ep.FixedBody()
		sun_nct._epoch = '2000'

		#represents the point in the sky aligned with the NCT axis
		onaxis = ep.FixedBody()
		onaxis._epoch = '2000'
		
		#direction to the north from NCT
		north1 = ep.FixedBody()
		north1._epoch = '2000'
		
		#represents the zenith direction of NCT (for tilt = 0, this is the same as zenith = onaxis)
		zenith = ep.FixedBody()
		zenith._epoch = '2000'
		
		for i in range(int(num_intervals_per_day)): #loop over 5 minute intervals
			
			tstring = time.strftime("%Y/%m/%d %H:%M:%S",timest)	
			nct.date = tstring
					
			v = ep.Sun(nct)	

			ra_sun_nct,dec_sun_nct = nct.radec_of(v.az,v.alt)	
			sun_nct._ra = ra_sun_nct
			sun_nct._dec = dec_sun_nct 
			sun_nct.compute()							
			sun_nct_gal = ep.Galactic(sun_nct)
			lon_sun_nct = sun_nct_gal.lon.__float__()
			lat_sun_nct = sun_nct_gal.lat.__float__() 

			sun_l = lon_sun_nct # radian
			sun_b = lat_sun_nct # radian

			ra_zenith,dec_zenith = nct.radec_of(0.0,90.0*pi/180.0)	
			zenith._ra = ra_zenith
			zenith._dec = dec_zenith	
			zenith.compute()		
			zenith_gal = ep.Galactic(zenith)	
			zenith_lon = zenith_gal.lon.__float__()
			zenith_lat = zenith_gal.lat.__float__()

			cosi_l = zenith_lon # radian
			cosi_b = zenith_lat # radian

			sun_elevation = 90 - GreatCircleDistance(sun_l, sun_b, cosi_l, cosi_b)*180/pi 			# degree
			source_elevation = 90 - GreatCircleDistance(source_l, source_b, cosi_l, cosi_b)*180/pi 	# degree

			sun_list.append(sun_elevation)
			source_list.append(source_elevation)
			tstring_list.append(unixtime)       	
		
		columnNum +=1

	if unixtime > endtime:		
		break

f0=open('elevation.txt','w')
for i in range(len(tstring_list)):
	f0.write('%f	%f\n'% (tstring_list[i],source_list[i]))


dates=[datetime.datetime.fromtimestamp(t) for t in tstring_list] 
datenums=md.date2num(dates)
if endtime-starttime < 300000:
	xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
else:
	xfmt = md.DateFormatter('%Y-%m-%d')
startdate=datetime.datetime.fromtimestamp(starttime)
enddate=datetime.datetime.fromtimestamp(endtime)

fivedays=md.DayLocator(interval=5)
threedays=md.DayLocator(interval=3)
days=md.DayLocator()

#Draw Sun and source elevation
plt.title('Vela Pulsar Elevation angle')
#plt.plot(datenums,sun_list,c='r',ls='--',label='Sun')
plt.plot(datenums,source_list,c='b',ls='-', label='Vela Pulsar')
plt.legend(loc=0)
plt.xlabel('UTC date')
plt.ylabel('Elevation angle(degee)')
if endtime-starttime > 2400000:
	plt.gca().get_xaxis().set_major_locator(fivedays)
elif endtime-starttime <= 2400000 and endtime-starttime > 1250000 :
	plt.gca().get_xaxis().set_major_locator(threedays)

plt.gca().get_xaxis().set_major_formatter(xfmt)
plt.gca().get_xaxis().set_minor_locator(days)
plt.xticks(rotation=25)
#plt.xlim(startdate,enddate)
plt.ylim(0,90)
plt.gca().grid()
#plt.show()
plt.savefig('Vela_Pulsar_Elevation.png', format='png')

#fig1 = plt.figure(figsize=(11,11))
#plt.axis([1463441128, 1467489587, 0, 90])
#plt.plot(tstring_list,sun_list,'rs', label='Sun')
#plt.plot(tstring_list,source_list,'bs', label='Crab')
#plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
#plt.ylim(0,90)
#plt.plot(tstring_list,sun_list,'r--',tstring_list,source_list,'bs')
#plt.savefig('Sun Elevation.png', format='png')

