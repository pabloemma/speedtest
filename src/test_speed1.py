#!/usr/bin/env python


'''
Created on Feb 8, 2020

@author: klein


This is based on the CLI program from speedtest
It basically provides a python wrapper around the speedtest, so tha we can fill
the results in a file, which can then be plotted
The original version of test_speed was pabsed on pyspeedtest and gave different results from
the GUI


some notes about the speedtest CLI; In csv mode the output is Bytes/second. In order to get Mbs, 
we have to multiply the output by 8./1e6


 the output format is
 day,time,server name, server id,latency,jitter,package loss in %, download, updload 
'''

import sys
import time
import os
import datetime
import textwrap
from datetime import  date 
import argparse as argp  # we want to sue CLI
import subprocess as sp


class test_speed1():
    
    
    
    def __init__(self,server,chosentime):
        print (' in init')        # before we do anything, let's determine the python version

        self.chosentime = chosentime # how long to wait in seconds before next reading
          
            
        self.vs = 2.0
        self.WriteHeader()
        
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
        print('Written by Andi Klein')
        print('Run date',datetime.datetime.now()) 
        print('****************************************************************** \n')   
        print('\n \n \n')    


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
             '''))

        
        # now we build up the different args we can have
        parser.add_argument("-s","--serverid",help = "Specify a server from the server list using its id" )
        parser.add_argument("-L","--servers",action='store_true',help = "List nearest servers" )
        parser.add_argument("-V","--version",action='store_true',help = "Print CLI version" )
        parser.add_argument("-o","--host",help = "Specify a server, from the server list, using its host's fully qualified dom" )
        parser.add_argument("-ip","--ip",help = "Attempt to bind to the specified IP address when connecting to servers" )
        #parser.add_argument("-ip","--ip=ARG",help = "Attempt to bind to the specified IP address when connecting to servers" )
        
        
        
        #list of argument lists
        
        
    
        # here some of the defaults
        temp1=["/usr/local/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default
                  
        # do our arguments
        args = parser.parse_args()
        #check if there are any arguments
        print args
        
        
        
        if(len(sys.argv) == 1):
            # we need to give it a server as default use cyber mesa
            se =['-s','18002']
            temp1.extend(se)
            self.command = temp1
            return
        else:
            if(args.servers):
                self.command = ["/usr/local/bin/speedtest", '-L'] #because argparse does not take single args
                self.RunShort()
                sys.exit(0)
            if(args.version):
                
                self.command = ["/usr/local/bin/speedtest", '-V'] #because argparse does not take single args
                self.RunShort()
                sys.exit(0)
                
            if(args.serverid != None):
                t=['-s',args.serverid]
                temp1.extend(t)

            if(args.ip != None):
                t=['--ip=',args.ip]
                temp1.extend(t)
                
            if(args.host != None):
                t=['--host=',args.host]
                temp1.extend(t)
                
        self.command = temp1 
        print self.command      
        return 
    
    def RunLoop(self):
        """
        calls run and forms the loop
        """
        while(1):
            self.Run()
            time.sleep(60)
            
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
        
        print self.command
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

        print myline
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
        self.output.append(inc[0])
        self.output.append(int(inc[2]))
        for k in  [3,4,5]:
            self.output.append(float(inc[k]))
            
        for k in  [6,7] :
            self.output.append(float(inc[k])*8./1000000)
            
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
        filename = homedir + '/speedfiles/'+filename
        print filename
        if os.path.isfile(filename):
            self.output_file = open(filename,'a',0)
        else :
            self.output_file = open(filename,'w',0)
            
    
    
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