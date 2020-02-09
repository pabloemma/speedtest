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
'''

import sys
import time
import os
import datetime
from datetime import  date 
import argparse as argp  # we want to sue CLI
import subprocess as sp


class test_speed1():
    
    
    
    def __init__(self,server,chosentime):
        print (' in init')        # before we do anything, let's determine the python version

        self.chosentime = chosentime # how long to wait in seconds before next reading
          
        if(server == None):
        
            self.host = 'albuquerque.speedtest.centurylink.net:8080'
        else:
            self.host = server
            
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
        else:
            print('you are behind the curve with python2')
            self.vers = 2
       
        
        print('\n \n \n')    
        
        print('****************************************************************** \n')   
        print('hello this is the LCWA speedtest version',self.vs)
        print('Written by Andi Klein')
        print('Run date',datetime.datetime.now()) 
        print('Speedtest host', self.host) 
        print('****************************************************************** \n')   
        print('\n \n \n')    


    def GetArguments(self):
        """
        this method deals with arguments parsed
        """
        #instantiate the parser
        parser = argp.ArgumentParser()
        
        # now we build up the different args we can have
        parser.add_argument("-s","--server-id",help = "Specify a server from the server list using its id" )
        parser.add_argument("-L","--servers",help = "List nearest servers" )
        parser.add_argument("-V","--version",help = "Print CLI version" )
        parser.add_argument("-o","--host",help = "Specify a server, from the server list, using its host's fully qualified dom" )
        parser.add_argument("-ip","--ip",help = "Attempt to bind to the specified IP address when connecting to servers" )
        #parser.add_argument("-ip","--ip=ARG",help = "Attempt to bind to the specified IP address when connecting to servers" )
        
        
        
        #list of argument lists
        ser_list=['-L']
        vers=['V']
        
    
        # here some of the defaults
        temp1=["/usr/local/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default
                  
        # do our arguments
        args = parser.parse_args()
        #check if there are any arguments
        if(len(sys.argv) == 0):
            self.commands = temp1
            return
        else:
            if(args.servers != None):
                temp1.append(ser_list)

            if(args.version != None):
                temp1.append(vers)
                
            #if(args.server-id != None):
             #   t=['-s',args.server-id]
              #  temp1.expand(t)

            if(args.ip != None):
                t=['--ip=',args.ip]
                temp1.expand(t)
                
            if(args.host != None):
                t=['--host=',args.host]
                temp1.expand(t)
                
        self.command = temp1       
        return 
    
    
                    
    def Run(self):
        """
        this is the heart of the wrapper, using the CLI command
        """
        
#        speed_command = ["/usr/local/bin/speedtest","--progress=no"," >test.txt"]
        
        #sp.call(speed_command,shell=True)
        #lets open temp file
        #outfile=open('/Users/klein/test.txt','w')
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
        
        print self.output
        
        
    def CreateOutput(self,inc1):
        """
        this takes the output line tuple and creates the csv line for the outputfile
        """
        self.output = []
        
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
    
    
if __name__ == '__main__':
    
    server1 = 'speed-king.cybermesa.com:8080'
   # server1 = 'albuquerque.speedtest.centurylink.net:8080'
    ts = test_speed1(server=server1,chosentime=60)
    ts.GetArguments()
#    ts.GetArguments()
#    ts.OpenFile()
    ts.Run()

    pass