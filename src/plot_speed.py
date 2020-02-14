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

drop = False
for k in range(len(sys.argv)):
    print sys.argv
if len(sys.argv)==2:
    # check if file exists
    try:
        if os.path.isfile((sys.argv[1])):
            filename = sys.argv[1]
            file1=filename
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
if(drop):
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

    file = '/LCWA/'+ sys.argv[1]
    dir = os.path.expanduser("~")
    file1 = dir+'/scratch/'+sys.argv[1]
    filename = dbx.files_download_to_file(file1,file)
    print filename         
x1 = []
y1 = []
x2 = []
y2 =[]

# check for data integrtity by writing file to temporary buffer

temp_file = open('temp.txt',"w")
for line in open(file1, 'r'):

    a = line.split(',')
    if(len(a)< 9):
        print ('problem',a)
    else:
        temp_file.write(line)
f.close()
temp_file.close()
   


#filename = "/Users/klein/speedfiles/2020-02-09speedfile.csv"        
x1,y1,y2 = np.loadtxt('temp.txt', delimiter=',',
                   unpack=True,usecols=(1,7,8),
#        converters={ 1: md.strpdate2num('%d/%m/%Y-%H:%M:%S')})
        converters={ 1: md.strpdate2num('%H:%M:%S')},skiprows=1)
        #converters={ 0: md.strpdate2num('%d/%m/%Y')})



fig=plt.figure()
ax=fig.add_subplot(1,1,1)


plt.plot_date(x1,y1,'g^',label='\n green UP')
plt.plot_date(x1,y2,'bs',label=' blue DOWN')
#plt.text(1.,1.,r' $\sigma = .1$')
plt.grid(True)

ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
plt.xlabel('Time')
plt.ylabel('Speed in Mbs')
plt.title('Speedtest LCWA using '+file)
plt.legend(loc="lower right",shadow=True, fancybox=True)
plt.ylim(0.,24.) # set yaxis limit
plt.xticks(rotation='vertical')
plt.tight_layout()
plt.show()




if __name__ == '__main__':
    pass