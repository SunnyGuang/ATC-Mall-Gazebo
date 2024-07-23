import sqlite3
from sqlite3 import Error

#################################  
#                               #
##### Creat a data class ########
#                               #
#################################


class Data_class():
    def __init__(self, db_name):
        self.name = db_name #radius of influence around pedestrian
        
        try:
            self.conn = sqlite3.connect(self.name)#connect to the data base
            self.c = self.conn.cursor()
        except Error as e:
            print(e)
            
        
    def update_db(self,command):
        
        self.c.execute(command)
        
    def extract_ped_at_pedid(self,index):#extract pedestrian at a particular index from ped_id file
        command = "SELECT * FROM ped_id WHERE rowid = "+str(index)+";"
        ped=[]
            
        for row in self.c.execute(command):
            ped.append(list(row))
        return ped
        

    def extract_all_tw(self):#extract all time windows in a db
        command = "SELECT * FROM timewindow;"
        tw=[]
            
        for row in self.c.execute(command):
            tw.append(list(row))
        return tw 

    def extract_all_tw_win_only(self):#extract all time windows in a db
        command = "SELECT seq_no FROM timewindow WHERE seq_no >2 ;"
        tw=[]
            
        for row in self.c.execute(command):
            tw.append(row)
        return tw 
    
    def extract_all_ped(self):#extract all pedestrians in a db
        command = "SELECT * FROM ped_id;"
        ped=[]
            
        for row in self.c.execute(command):
            ped.append(list(row))
        return ped 

    def extract_ped(self,ped_id):#extract all instances of a particular pedestrian
        command = "SELECT * FROM pedestrian WHERE ped_id = "+str(ped_id)+";"
        ped=[]
            
        for row in self.c.execute(command):
            ped.append(list(row))
        return ped   
    
    def extract_ped_vel(self,ped_id): #extract all velocity of a particular pedestrian
        command = "SELECT vel FROM pedestrian WHERE ped_id = "+str(ped_id)+";"
        ped=[]
            
        for row in self.c.execute(command):
            ped.append(list(row))
        return ped 
    
    def extract_ped_sorted(self,ped_id):#extract all instances of a particular pedestrian
        command = "SELECT * FROM pedestrian WHERE ped_id = "+str(ped_id)+" ORDER BY timewindow_id ASC;"
        ped=[]
            
        for row in self.c.execute(command):
            ped.append(list(row))
        return ped 
    
    def extract_timewin_at(self,index):#extract pedestrian at a particular index
        command = "SELECT * FROM pedestrian WHERE timewindow_id = "+str(index)+";"
        ped=[]
            
        for row in self.c.execute(command):
            ped.append(list(row))
        return ped   
    
    def extract_timewin(self):#extract all data before timewindow = 10000
        command = "SELECT * FROM pedestrian WHERE id < 80857 "
        ped=[]
            
        for row in self.c.execute(command):
            ped.append(list(row))
        return ped   
      
    def close_db(self):
        self.conn.close()
