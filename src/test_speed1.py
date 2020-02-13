#!/usr/bin/env python


'''
Created on Feb 8, 2020

@author: klein


This is based on the CLI program from speedtest
It basically provides a python wrapper around the speedtest, so that we can fill
the results in a file, which can then be plotted
The original version of test_speed was pabsed on pyspeedtest and gave different results from
the GUI


some notes about the speedtest CLI; In csv mode the output is Bytes/second. In order to get Mbs, 
we have to multiply the output by 8./1e6


 the output format is
 day,time,server name, server id,latency,jitter,package loss in %, download, upload 
'''

import sys
import time
import os
import datetime
import textwrap
from datetime import  date 
import argparse as argp  # we want to use CLI
import platform # need to determine the OS
import subprocess as sp
import dropbox
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from __builtin__ import True


class test_speed1():
    
    
    
    def __init__(self,server,chosentime):
        #print (' in init')        # before we do anything, let's determine the python version

        self.chosentime = chosentime # how long to wait in seconds before next reading
          
            
        self.vs = '3.02.0'
        self.WriteHeader()
        
        self.DropFlag = False # default no dropbox connection
        

    def ConnectDropBox(self):
        """
        here we establish connection to the dropbox account
        """
        #f=open(self.keyfile,"r")
        #self.key =f.readline() #key for encryption
        #self.key = pad(self.key,16)
        #f.close()

        f=open(self.cryptofile,"r")
        self.data =f.readline() #key for encryption
        #self.data=self.data.strip('\n')
        #print self.data,self.data
        #f.close()
        #enc = base64.b64decode(self.data)
        #iv = enc[:16]
        #cipher = AES.new(self.key, AES.MODE_CBC, iv )
        #print type(unpad(cipher.decrypt( enc[16:] ),16))
        

         
         
         
         #connect to dropbox
        #self.dbx=dropbox.Dropbox(unpad(cipher.decrypt( enc[16:] ),16))
        self.dbx=dropbox.Dropbox(self.data.strip('\n'))

        self.myaccount = self.dbx.users_get_current_account()
        print self.myaccount 
        
        
    def WriteHeader(self):   
        '''
        gives out all the info at startup
        '''
        print(sys.version_info[0])
        if (sys.version_info[0] == 3):
            print(' we have python 3')
            self.vers = 3
            print ('not implemented yet')
            sys.exit(0)
        else:
            print('you are behind the curve with python2')
            self.vers = 2
       
        
        print('\n \n \n')    
        
        print('****************************************************************** \n')   
        print('hello this is the LCWA speedtest version',self.vs)
        print('Written by Andi Klein using the CLI from speedtest')
        print('Run date',datetime.datetime.now()) 
        print('\n ')    
        
        print('****************************************************************** \n')   
        print('\n \n \n')  
        self.Progress()  

    def Progress(self):
        """
        keep track of the updates
        """
        print(' History')
        print('version 2.02', '  trying to catch the random bad data sent by the CLI')
        print('version 2.03', ' fixed conversion problem for N/A')
        print('        version 2.03.1', ' fixed rasp problem wit -L and -V')
        print('version 3.01.0', 'connect to dropbox and store file every 50 entries')
        print('        3.01.1', 'added header line to output')
        print('version 3.02.0', ' - made cybermesa default server unless requested ')
        print('                     - at midnight we open a new file')
        print('\n\n\n')
        
        
    def GetArguments(self):
        """
        this method deals with arguments parsed
        """
        #instantiate the parser
        parser = argp.ArgumentParser(
            prog='test_speed1',
            formatter_class=argp.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''
            Output format:
            day,time,server name, server id,latency[ms],jitter[ms],package loss[%], download Mb/s, updload Mb/s
            If you don't  give a filename for the password and the key, \n
            you will not coinnect to the output
            dropbox 
             
             
             '''))

        
        # now we build up the different args we can have
        parser.add_argument("-s","--serverid",help = "Specify a server from the server list using its id" )
        parser.add_argument("-L","--servers",action='store_true',help = "List nearest servers" )
        parser.add_argument("-V","--version",action='store_true',help = "Print CLI version" )
        parser.add_argument("-o","--host",help = "Specify a server, from the server list, using its host's fully qualified dom" )
        parser.add_argument("-ip","--ip",help = "Attempt to bind to the specified IP address when connecting to servers" )
        parser.add_argument("-t","--time",help = "time between succssive speedtests in minutes (integer)" )
        #parser.add_argument("-p","--pwfile",help = "The passwordfile" )
        parser.add_argument("-d","--dpfile",help = "The file for the dropbox" )

        #parser.add_argument("-ip","--ip=ARG",help = "Attempt to bind to the specified IP address when connecting to servers" )
        
        
        
        #list of argument lists
        
        
    
        # here some of the defaults
        #Of courss Mac has the stuff in different places than Linux
        if platform.system() == 'Darwin':
            temp1=["/usr/local/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default
        elif platform.system() == 'Linux':
            temp1=["/usr/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default         
        # do our arguments
        else:
            print' Sorry we don\'t do Windows yet'
            sys.exit(0)
        args = parser.parse_args()
        #check if there are any arguments
        
        
        self.loop_time = 60 # default 1 minutes before next speedtest
        
        if(len(sys.argv) == 1):
            # we need to give it a server as default use cyber mesa
            se =['-s','18002']
            temp1.extend(se)
            self.command = temp1
            #self.keyfile('LCWA_p.txt')
            return
        else:
            #make cyber mesa the default
            if(args.servers):
                if platform.system() == 'Darwin':

                    self.command = ["/usr/local/bin/speedtest", '-L'] #because argparse does not take single args
                elif platform.system() == 'Linux':
                    self.command=["/usr/bin/speedtest",'-L'] # we want csv output by default         
                   
                
                self.RunShort()
                sys.exit(0)
            if(args.version):
                if platform.system() == 'Darwin':

                    self.command = ["/usr/local/bin/speedtest", '-V'] #because argparse does not take single args
                elif platform.system() == 'Linux':
                    self.command=["/usr/bin/speedtest",'-V'] # we want csv output by default         
                
                self.RunShort()
                sys.exit(0)
                
            if(args.serverid != None):
                t=['-s',args.serverid]
                temp1.extend(t)
            else: # make cybermesa the default
                t=['-s','18002']
                temp1.extend(t)
              
            

            if(args.ip != None):
                t=['--ip=',args.ip]
                temp1.extend(t)
                
            if(args.host != None):
                t=['--host=',args.host]
                temp1.extend(t)
            if(args.time != None):
                self.loop_time = int(args.time)*60 # time between speedtests
                
            #if(args.pwfile != None ) and (args.dpfile != None):
            if(args.dpfile != None):
                #self.keyfile = args.pwfile
                self.cryptofile = args.dpfile
                self.DropFlag = True
                self.ConnectDropBox() # establish the contact to dropbox
                
        self.command = temp1 
        #print self.command      
        return 
    
    def RunLoop(self):
        """
        calls run and forms the loop
        """
        counter = 0
        while(1):
            self.Run()
            if(self.ConnectDropBox):
                counter = counter + 1
            
                if (counter==50):
                    
 
                    
                    
                    
                    f =open(self.lcwa_filename,"rb")
                    self.dbx.files_upload(f.read(),'/LCWA/'+self.docfile,mode=dropbox.files.WriteMode('overwrite', None))
                    print('wrote dropbox file')
                    counter = 0 

            time.sleep(self.loop_time)

            
            
    def RunShort(self):    
        process = sp.Popen(self.command,
                         #stdout=outfile,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE,
                         universal_newlines=True)
        
        out,err = process.communicate()
        
        print out
        sys.exit(0)
            
                    
    def Run(self):
        """
        this is the heart of the wrapper, using the CLI command
        """
        
        #print self.command
        process = sp.Popen(self.command,
                         #stdout=outfile,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE,
                         universal_newlines=True)
        
        out,err = process.communicate()
        
        a=str(out)
        #a is now a tuple , which we fill into a csv list
        self.CreateOutput(a)
        
        #print self.output  #for debugging

        myline=''
        # now create outputline from tuple
        for k in range(len(self.output)-1):
            myline=myline+str(self.output[k])+','
        myline = myline+str(self.output[len(self.output)-1])+'\n'

        
        #check for date, we will open new file at midnight
        if(date.today()>self.current_day):
                #we have a new day
            self.output_file.close()
            self.OpenFile()

        
        #print myline
        self.output_file.write(myline)
        
        
    def CreateOutput(self,inc1):
        """
        this takes the output line tuple and creates the csv line for the outputfile
        """
        #start with trhe current time and date
        now=datetime.datetime.now()
        
        self.output = [now.strftime("%d/%m/%Y"),now.strftime("%H:%M:%S")]
        
        # strip ,NM out of the server description
        
        #First rempve all double quotes
        tt=inc1.replace('"','')
        inc=tt.split(',')

        # cehck data integrity
        if(len(inc) < 2):
            print('bad data block')
            return
        if(len(inc) != 11):
            print('bad block length')
            return
        
        
        print inc # for debugging
        self.output.append(inc[0])
        self.output.append(int(inc[2]))
        for k in  [3,4,5]:
            try:
                float(inc[k])
                self.output.append(float(inc[k]))
            except ValueError:
                print('bad int conversion')
                self.output.append(-10000.)
            
            
        for k in  [6,7] :
            try:
                float(inc[k])
            
                self.output.append(float(inc[k])*8./1000000)
            except ValueError:
                print('bad float conversion')
                self.output.append(-999.)
                
            
        return 


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
        self.docfile = filename #filename for dropbox
        filename = homedir + '/speedfiles/'+filename
        print filename
        self.lcwa_filename = filename
        if os.path.isfile(filename):
            self.output_file = open(filename,'a',0)
        else :
            self.output_file = open(filename,'w',0)
            self.WriteOutputHeader() # first time we write a header
            
            
    def WriteOutputHeader(self):       
        """
        Write the header for the output file
        """
        Header = 'day,time,server name, server id,latency,jitter,package , download, upload \n'
        self.output_file.write(Header)
        
        
        
if __name__ == '__main__':
    
    server1 = 'speed-king.cybermesa.com:8080'
   # server1 = 'albuquerque.speedtest.centurylink.net:8080'
    ts = test_speed1(server=server1,chosentime=60)
    ts.GetArguments()  #commandline args
    ts.OpenFile()  #output file
    
#    ts.GetArguments()
#    ts.OpenFile()
    ts.RunLoop()

    pass
