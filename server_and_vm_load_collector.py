'''
This module collects information from servers and its vm's mentioned in the 
initial list collects vm compute and ram usage and stores in mysql database.
'''

import mysql.connector as sql
import os
import time
from novaclient.v2 import client
import urllib2
import ast

MYSQL_USER_NAME = 'root'
MYSQL_PASSWORD = '1234'
MYSQL_HOST_NAME = 'localhost'
MYSQL_DB = 'stack'



def get_nova_creds():
    d = {}
    d['username'] = 'admin'
    d['api_key'] = 'nomoresecret'
    d['auth_url'] = 'http://192.168.0.5:5000/v2.0'
    d['project_id'] = 'admin'
    return d


class ServerAndVmLoadCollector:
    def __init__(self):
        self.conn = sql.connect(user = MYSQL_USER_NAME,password = MYSQL_PASSWORD,host = MYSQL_HOST_NAME,database = MYSQL_DB)
        self.cur = self.conn.cursor()
        self.creds = get_nova_creds()
        nova =client.Client(**self.creds)
        
    
    def get_server_info(self):  
        server_info=[]
        query = 'select * from server'      
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            server_info.append(list(row))
        return  server_info   
        
    
    def get_vm_info(self):
        vm_info=[]
        query = 'select * from vm'
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            vm_info.append(list(row))
        return  vm_info  
    
    def get_server_load(self,server_info):
        for server in server_info:
            cpu,ram_total,ram_used = self.get_node_load(server[1])
            server[2] = cpu
            server[23] = ram_used
         
    def get_vm_load(self,vm_info):
        for vm in vm_info:
            cpu,ram_total,ram_used = self.get_node_load(vm[2])
            vm[2] = cpu  
            
    def get_node_load(self,node_ip):
        request_url = 'http://'+node_ip+':8080/cgi-bin/getload.html'
        response = urllib2.urlopen(request_url)
        load_dict = ast.literal_eval(response.read())
        return (load_dict['cpu_usage'],load_dict['ram_total'],load_dict['ram_total']-load_dict['ram_free'])
    
    def get_migration_status(self):
        query = 'select * from status'      
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result[0]
    
    def set_migration_status(self):
        query = 'update status set status = 1'     
        self.cur.execute(query)
        self.conn.commit()
        
        
    def unset_migration_status(self):
        query = 'update status set status = 0'     
        self.cur.execute(query)
        self.conn.commit()
        
    def update_server_info(self,server_info):
        for server in server_info:
            query = 'update server set server_load1=\''+str(server[2])+'\',server_load2=\''+str(server[3])+'\',server_load3=\''+str(server[4])+'\',server_load4=\''+str(server[5])+'\',server_load5=\''+str(server[6])+'\',server_load6=\''+str(server[7])+'\',server_load7=\''+str(server[8])+'\',server_load8=\''+str(server[9])+'\',server_load9=\''+str(server[10])+'\',server_load10=\''+str(server[11])+'\',server_load11=\''+str(server[12])+'\',server_load12=\''+str(server[13])+'\',server_load13=\''+str(server[14])+'\',server_load14=\''+str(server[15])+'\',server_load15=\''+str(server[16])+'\',server_load16=\''+str(server[17])+'\',server_load17=\''+str(server[18])+'\',server_load18=\''+str(server[19])+'\',server_load19=\''+str(server[20])+'\',server_load20=\''+str(server[21])+'\',server_ram_total=\''+str(server[22])+'\',server_ram_used=\''+str(server[23])+'\',no_of_large_vm=\''+str(server[24])+'\',no_of_medium_vm=\''+str(server[25])+'\',no_of_small_vm=\''+str(server[26])+'\',no_of_high_load_vm=\''+str(server[27])+'\',no_of_medium_load=\''+str(server[28])+'\',no_of_low_load=\''+str(server[29])+'\'where name = \''+str(server[0])+'\';'
            self.cur.execute(query)
            self.conn.commit()
            
    def update_vm_info(self,vm_info):
        for vm in vm_info:
            query = 'update vm set  vm_load1=\''+str(vm[2])+'\',vm_load2=\''+str(vm[3])+'\',vm_load3=\''+str(vm[4])+'\',vm_load4=\''+str(vm[5])+'\',vm_load5=\''+str(vm[6])+'\',vm_load6=\''+str(vm[7])+'\',vm_load7=\''+str(vm[8])+'\',vm_load8=\''+str(vm[9])+'\',vm_load9=\''+str(vm[10])+'\',vm_load10=\''+str(vm[11])+'\',vm_load11=\''+str(vm[12])+'\',vm_load12=\''+str(vm[13])+'\',vm_load13=\''+str(vm[14])+'\',vm_load14=\''+str(vm[15])+'\',vm_load15=\''+str(vm[16])+'\',vm_load16=\''+str(vm[17])+'\',vm_load18=\''+str(vm[19])+'\',vm_load19=\''+str(vm[20])+'\',vm_load20=\''+str(vm[21])+'\',vm_class=\''+str(vm[22])+'\',server_id=\''+str(vm[24])+'\'where name = \''+str(vm[0])+'\';'
            self.cur.execute(query)
            self.conn.commit()
            
    def alter_server_load(self,server_info):
        for i in reversed(range(3,22)):
            server_info[i]=server_info[i-1]
   
    def alter_vm_load(self,vm_info):
            for i in reversed(range(3,22)):
                vm_info[i]=vm_info[i-1]
    
    def load_avg(self,node):
        sum=0
        for i in range(2,22):
            sum+=node[i]
        return sum/20    
    
    def modify_vm_and_server_info(self,server_info,vm_info):
        for vm in vm_info:
            load = self.load_avg(vm)
            if load < 33:
                vm[22] = 0
            elif load < 66:
                vm[22]= 1
            else:
                vm[22] = 3
         
        server_vm_table = {}           
        for server in server_info:
            server_vm_table[server[0]][0] = 0
            server_vm_table[server[0]][1] = 0
            server_vm_table[server[0]][2] = 0
            
        for vm in vm_info:
            server_vm_table[vm[24]][vm[22]] +=1
        
        for server in server_info:
            server[29] = server_vm_table[server[0]][0] 
            server[28] = server_vm_table[server[0]][1]
            server[27] = server_vm_table[server[0]][2]
            
            
    def Execute(self):
        while True:
            while self.get_migration_status()==1:
                time.sleep(10)
            self.unset_migration_status()
            server_info = self.get_server_info()
            self.alter_server_load(server_info)
            vm_info  = self.get_vm_info()
            self.alter_vm_load(vm_info)
            self.get_server_load(server_info)
            self.get_vm_load(vm_info)
            self.modify_vm_and_server_info(server_info,vm_info)
            self.update_server_info(server_info)
            self.update_vm_info(vm_info)
            self.set_migration_status()
            time.sleep(60)
            
    