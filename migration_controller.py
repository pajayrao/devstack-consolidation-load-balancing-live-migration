'''
Collects migration details across multiple nodes and performs live migration.
'''
import mysql.connector as sql
import os,time

MYSQL_USER_NAME = 'root'
MYSQL_PASSWORD = '1234'
MYSQL_HOST_NAME = 'localhost'
MYSQL_DB = 'stack'

class MigrationController:
    def __init__(self):
        self.conn = sql.connect(user = MYSQL_USER_NAME,password = MYSQL_PASSWORD,host = MYSQL_HOST_NAME,database = MYSQL_DB)
        self.cur = self.conn.cursor()
        
    def migrate(self,vm_id,server_id):
        os.system('nova live-migration --block-migrate '+str(vm_id)+' '+str(server_id))
    
    def get_server_info(self,server):  
        server_info=[]
        query = 'select * from server where name = \''+str(server)+'\''    
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            server_info.append(list(row))
        return  server_info   
        
    
    def get_vm_info(self,vm_id):
        vm_info=[]
        query = 'select * from vm where name = \''+str(vm_id)+'\''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            vm_info.append(list(row))
        return  vm_info  
        
    def Execute(self, vm, dest_node, source_node):
        dest_server_info  = self.get_server_info(dest_node)
        source_server_info  = self.get_server_info(source_node)
        vm_info = self.get_vm_info(vm)
        self.migrate(vm,dest_node)
        if(vm_info[23]==0):
            query = 'update server set no_of_large_vm =no_of_large_vm-1 where server = \''+str(source_node)+'\'  '      
            self.cur.execute(query)
            self.conn.commit()
            query = 'update server set no_of_large_vm =no_of_large_vm+1 where server = \''+str(dest_node)+'\'  '      
            self.cur.execute(query)
            self.conn.commit()
        elif (vm_info[23]==0):
            query = 'update server set no_of_medium_vm =no_of_large_vm-1 where server = \''+str(source_node)+'\'  '      
            self.cur.execute(query)
            self.conn.commit()
            query = 'update server set no_of_medium_vm =no_of_large_vm+1 where server = \''+str(dest_node)+'\'  '      
            self.cur.execute(query)
            self.conn.commit()
        else:
            query = 'update server set no_of_low_vm =no_of_large_vm-1 where server = \''+str(source_node)+'\'  '      
            self.cur.execute(query)
            self.conn.commit()
            query = 'update server set no_of_low_vm =no_of_large_vm+1 where server = \''+str(dest_node)+'\'  '      
            self.cur.execute(query)
            self.conn.commit()
        query = 'update vm set server_id = \''+str(dest_node)+'\' where name = \''+str(vm)+'\' '      
        self.cur.execute(query)
        self.conn.commit()
        
        
        
    
    