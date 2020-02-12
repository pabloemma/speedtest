'''
Created on Feb 11, 2020

@author: klein

Class to handle transfer of files to dropbox
'''

import dropbox

class MyDrop():
    
    def __init__(self):
          
          # connect to my newmexicopand drop box
        self.dbx=dropbox.Dropbox("1N74OZNee0AAAAAAAAAAC8Pvo3BX2phcS-95b62r_F7W_xfjV_Xx606gC_Nxfeq5")
        self.myaccount = self.dbx.users_get_current_account()
    
    
    def PushFile(self):
        f =open('/Users/klein/speedfiles/2020-02-11speedfile.csv',"rb") 
        self.dbx.files_upload(f.read(),'/LCWA/2020-02-11speedfile.csv',
                              mode=dropbox.files.WriteMode('overwrite', None)) 

if __name__ == '__main__':
    MyD = MyDrop()
    MyD.PushFile()
    pass