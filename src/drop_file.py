'''
Created on Feb 11, 2020

@author: klein

Class to handle transfer of files to dropbox
'''

import dropbox

class MyDrop():
    
    def __init__(self,cryptofile):
        
        
        f=open(cryptofile,"r")
        self.data =f.readline() #key for encryption

        # connect to my newmexicopand drop box
        self.dbx=dropbox.Dropbox(self.data.strip('\n'))
        self.myaccount = self.dbx.users_get_current_account()
        print self.myaccount.name.surname , self.myaccount.name.given_name
        print self.myaccount.email
        #print self.myaccount
    
    
    def PushFile(self):
        f =open('/Users/klein/speedfiles/2020-02-11speedfile.csv',"rb") 
        self.dbx.files_upload(f.read(),'/LCWA/2020-02-11speedfile.csv',
                              mode=dropbox.files.WriteMode('overwrite', None)) 

if __name__ == '__main__':
    MyD = MyDrop('/Users/klein/workspace/network speed/src/LCWA_d.txt')
    #MyD.PushFile()
    pass