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
import os.path
import dropbox


for k in range(len(sys.argv)):
    print sys.argv
if len(sys.argv)==2:
    # check if file exists
    try:
        if os.path.isfile((sys.argv[1])):
            filename = sys.argv[1]
    except:
        print('no file')
        sys.exit(0)
elif len(sys.argv)==3:
    drop=True
    

else:
    print( ' to run the program you have to give a filename \n plot_speed.py inputfile ')
    print(' You have to give the token file')
    sys.exit(0)
    
# connect to dropbox
f=open(sys.argv[2],"r")
data =f.readline() #key for encryption
data=data.strip('\n')

#connect to dropbox
dbx=dropbox.Dropbox(data)
myaccount = dbx.users_get_current_account()
print('***************************dropbox*******************\n\n\n')
print myaccount.name.surname , myaccount.name.given_name
print myaccount.email
print('\n\n ***************************dropbox*******************\n')

# get dropbox file
if(drop):
    file = '/LCWA/'+ sys.argv[1]
    dir = os.path.expanduser("~")
    file1 = dir+'/scratch/'+sys.argv[1]
    filename = dbx.files_download_to_file(file1,file)
    print filename         
x1 = []
y1 = []
x2 = []
y2 =[]

# for date plotting
#n=20
#duration =1000


#filename = "/Users/klein/speedfiles/2020-02-09speedfile.csv"        
x1,y1,y2 = np.loadtxt(file1, delimiter=',',
                   unpack=True,usecols=(1,7,8),
#        converters={ 1: md.strpdate2num('%d/%m/%Y-%H:%M:%S')})
        converters={ 1: md.strpdate2num('%H:%M:%S')},skiprows=1)
        #converters={ 0: md.strpdate2num('%d/%m/%Y')})

plt.plot_date(x1,y1, label=file1+'\n blue UP \n red DOWN')
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