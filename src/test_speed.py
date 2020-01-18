'''
Created on Jan 16, 2020

@author: klein

This program is based on pyspeedtest.py

'''

import sys
import time
import os
import datetime
from datetime import  date 



import pyspeedtest  


class test_speed():
    
    
    
    def __init__(self,server,chosentime):
        
        # before we do anything, let's determine the python version
        if (sys.version_info > (3, 0)):
            print(' we have python 3')
            self.vers = 3
        else:
            print('you are behind the curve with python2')
            self.vers = 2

        self.chosentime = chosentime # how long to wait in seconds before next reading
        self.st = pyspeedtest.SpeedTest()  #instantiate class
        
        if(server == None):
        
            self.st.host = 'albuquerque.speedtest.centurylink.net:8080'
        else:
            self.st.host = server
            
   
            
    def run(self):
        while(1==1):
            pingi = round(self.pingit(),2)
            downloadi = round(self.downloadit(),2)
            uploadi = round(self.uploadit(),2) 
            if(self.vers == 2):
                
                print 'ping = ',pingi, ' download speed Mb/sec = ',downloadi, 'upload_speed Mb/sec = ',uploadi
            else:
                print('ping = ',pingi, ' download speed Mb/sec = ',downloadi, 'upload_speed Mb/sec = ',uploadi)
            now=datetime.datetime.now()
            myline=now.strftime("%d/%m/%Y,%H:%M:%S")+','+str(pingi)+','+str(downloadi)+','+str(uploadi)+'\n'                
            self.output.write(myline)
            time.sleep(self.chosentime)

    
    
    def pingit(self):
        ping_speed =  self.st.ping()
        return ping_speed
    def downloadit(self):
        download_speed = self.st.download()
        return download_speed/1000000.
    def uploadit(self):
        upload_speed = self.st.upload()
        return upload_speed/1000000.
    
         
            
    def OpenFile(self):
        ''' the default filename is going to be the date of the day
        and it will be in append mode
        '''
        self.current_day = date.today()
        a = datetime.datetime.today().strftime('%Y-%m-%d')
        filename = a+'speedfile.csv'
        # if filename exists we open in append mode
        #otherwise we will create it
        homedir = os.environ['HOME']
        filename = homedir + '/speedfiles/'+filename
        print filename
        if os.path.isfile(filename):
            self.output = open(filename,'a',0)
        else :
            self.output = open(filename,'w',0)


if __name__ == '__main__':
    server1 = 'speed-king.cybermesa.com:8080'
   # server1 = 'albuquerque.speedtest.centurylink.net:8080'
    ts = test_speed(server=server1,chosentime=60)
    ts.OpenFile()
    ts.run()
    



