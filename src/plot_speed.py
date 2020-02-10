#!/usr/bin/env python

'''
Created on Jan 23, 2020

@author: klein
'''



import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import csv
import time
import sys


for k in range(len(sys.argv)):
    print sys.argv
if len(sys.argv)==2:
    filename = sys.argv[1]
else:
    print( ' to run the program you have to give a filename \n plot_speed.py inputfile ')
    sys.exit(0)      
x1 = []
y1 = []
x2 = []
y2 =[]

# for date plotting
#n=20
#duration =1000


#filename = "/Users/klein/speedfiles/2020-02-09speedfile.csv"        
x1,y1,y2 = np.loadtxt(filename, delimiter=',',
                   unpack=True,usecols=(1,7,8),
#        converters={ 1: md.strpdate2num('%d/%m/%Y-%H:%M:%S')})
        converters={ 1: md.strpdate2num('%H:%M:%S')})
        #converters={ 0: md.strpdate2num('%d/%m/%Y')})

plt.plot_date(x1,y1, label=filename+'\n blue UP \n red DOWN')
plt.plot_date(x1,y2)

#plt.plot(x2,y2,"r-")

plt.xlabel('Time')
plt.ylabel('Speed in Mbs')
plt.title('Speedtest LCWA')
plt.legend()
plt.ylim(0.,22.) # set yaxis limit
plt.show()




if __name__ == '__main__':
    pass