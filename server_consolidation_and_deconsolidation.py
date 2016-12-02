'''
Implements server consolidation and deconsolidation across multiple compute node 
'''
import mysql.connector as sql
import migration_controller as mc

MYSQL_USER_NAME = 'root'
MYSQL_PASSWORD = '1234'
MYSQL_HOST_NAME = 'localhost'
MYSQL_DB = 'stack'

MAX_THRESHOLD = 80
MIN_THRESHOLD = 40

VM_FLAVOUR_RAM = [512,1024,2048]



class ServerConsolidationAndDeconsolidation:
    def __init__(self):
        self.conn = sql.connect(user = MYSQL_USER_NAME,password = MYSQL_PASSWORD,host = MYSQL_HOST_NAME,database = MYSQL_DB)
        self.cur = self.conn.cursor()
        self.mc = mc.MigrationController()
        
        
    
    def avg_server_load(self,server_info):
        total = 0
        for server in server_info:
            if server[31] ==1:
                total += self.load_avg(server)
    
        return total/len(server_info)
   
    def consolidation(self,server_info):
        query = 'select * from server where priority = (select max(priority) from server where status = 1) '      
        self.cur.execute(query)
        result = self.cur.fetchrow()
        server_shut_down = result[0]
        query = 'select * from vm where server_id = \'' +str(server_shut_down) +'\''    
        self.cur.execute(query)
        result = self.cur.fetchall()
        vm_migrate_list = []
        for vm in result:
            vm_migrate_list.append(list(vm))
        count = 0   
        for vm in vm_migrate_list:
            mem_req = VM_FLAVOUR_RAM[vm[23]]
            for server in server_info:
                if server[22]-server[23] > mem_req and server[31] == 1 and server[0]!=server_shut_down:
                    self.mc.Execute(vm[0], server[0], server_shut_down)
                    server[23]+=mem_req
                    count+=1
                    break
        if(count == len(vm_migrate_list)):
            print 'Server consolidation successful with '+ str(count)+ ' migration'
            query = 'update server set status = 0 where name = \''+server_shut_down+'\' '      
            self.cur.execute(query)       
            self.conn.commit()
        else:
            print 'Unable to consolidate due insufficient RAM for '+str(len(vm_migrate_list)-count)+' .The load will be balanced by load balancer'  
             
                
    def deconsolidation(self,server_info):
        query = 'select * from server where priority = (select min(priority) from server where status = 0) '      
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result) ==0:
            print 'No server to deconsolidate'
        else:    
            server_start_up = result[0]
            query = 'update server set status = 1 where name = \''+server_start_up+'\' '    
            self.cur.execute(query)
            self.conn.commit()
            
            

    
    def load_avg(self,node):
        sum=0
        for i in range(2,22):
            sum+=node[i]
        return sum/20 
    
    def get_server_info(self):  
        server_info=[]
        query = 'select * from server order by priority asc'      
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            server_info.append(list(row))
        return  server_info
  
    def Execute(self):
        server_info = self.get_server_info()
        server_load = self.avg_server_load(server_info)
        if server_load>MAX_THRESHOLD:
            self.deconsolidation(server_info)
        elif server_load<MIN_THRESHOLD:
            self.consolidation(server_info)
                
            