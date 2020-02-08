'''
Created on Feb 8, 2020

@author: klein


This is based on the CLI program from speedtest
It basically provides a python wrapper around the speedtest, so tha we can fill
the results in a file, which can then be plotted
The original version of test_speed was pabsed on pyspeedtest and gave different results from
the GUI
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
        parser.add_argument("-t","--time",type = int,help = "the time interval in seconds" )
        parser.add_argument("-s","--server",help = "the speedtest server" )
    
   
        # do our arguments
        args = parser.parse_args()
        #check if there are any arguments
        if(len(sys.argv) == 0):
            return
        else:
            if(args.time != None):
                self.chosentime = args.time
                print('time interval',self.chosentime,'sec')
            if(args.server != None):
                self.st.host = args.server
                #print self.st.host
                print('chosen server',self.st.host)
                
    def Run(self):
        """
        this is the heart of the wrapper, using the CLI command
        """
        
        speed_command = ["/usr/local/bin/speedtest","--progress=no"," >test.txt"]
        
        #sp.call(speed_command,shell=True)
        #lets open temp file
        outfile=open('/Users/klein/test.txt','w')
        process = sp.Popen(speed_command,
                         stdout=outfile,
                         universal_newlines=True)
        #stdout1 = process.communicate()
        #print stdout1
        outfile.close()
        print 'done'
         

if __name__ == '__main__':
    
    server1 = 'speed-king.cybermesa.com:8080'
   # server1 = 'albuquerque.speedtest.centurylink.net:8080'
    ts = test_speed1(server=server1,chosentime=60)
#    ts.GetArguments()
#    ts.OpenFile()
    ts.Run()

    pass