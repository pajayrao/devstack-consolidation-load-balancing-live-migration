'''
Implements load balancing operation across multiple nodes
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

class LoadBalancing:
    def __init__(self):
        self.conn = sql.connect(user = MYSQL_USER_NAME,password = MYSQL_PASSWORD,host = MYSQL_HOST_NAME,database = MYSQL_DB)
        self.cur = self.conn.cursor()
        self.mc = mc.MigrationController()
        
    def get_vm_info(self,vm_id):
        vm_info=[]
        query = 'select * from vm'
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            vm_info.append(list(row))
        return  vm_info  
    
    def get_server_info(self):  
        server_info=[]
        query = 'select * from server where status =1'      
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            server_info.append(list(row))
        return  server_info  
     
    def avg_vm_count(self, vm_info,server_info):
        low_vm_avg = 0
        medium_vm_avg=0
        high_vm_avg=0
        for vm in vm_info:
            if vm[23] ==0:
                low_vm_avg+=1
            elif vm[23] ==1:
                medium_vm_avg+=1
            elif vm[23] ==2:
                high_vm_avg+=1
            else:
                print "Error in deciding the flavour of the vm"     
                 
        total_vm = len(vm_info)
        
        return (low_vm_avg/total_vm, medium_vm_avg/total_vm, high_vm_avg/total_vm)     
                     
    def Execute(self):
        server_info  = self.get_server_info()
        vm_info = self.get_vm_info()
        low_vm_avg,medium_vm_avg,high_vm_avg = self.avg_vm_count(vm_info)
        
        # Load balancing large flavor server
        for server in server_info:
            if server[24] > high_vm_avg:
                mem_req = VM_FLAVOUR_RAM[2]
                for s in server_info:
                    if s[24] < high_vm_avg and s[22]-s[23] > mem_req:
                        for vm in vm_info:
                            if vm[23] == 2 and vm[24] ==server[0]:
                                server[23]-=mem_req
                                server[24]-=1
                                s[24]+=1
                                s[23]+=mem_req
                                print 'Migrating vm '+str(vm[0])+' from server '+str(server[0])+' to server'+str(s[0])
                                self.mc.Execute(vm[0], s[0], server[0])
                                # query = 'insert into migration values(\''+str(vm[0])+'\',\''+str(s[0])+'\',\''+str(server[0])+'\')'     
                                #self.cur.execute(query)
                                break

        # Load balancing medium flavor server
        for server in server_info:
            if server[25] > medium_vm_avg:
                mem_req = VM_FLAVOUR_RAM[1]
                for s in server_info:
                    if s[25] < medium_vm_avg and s[22]-s[23] > mem_req:
                        for vm in vm_info:
                            if vm[23] == 1 and vm[24] ==server[0]:
                                server[23]-=mem_req
                                server[25]-=1
                                s[25]+=1
                                s[23]+=mem_req
                                print 'Migrating vm '+str(vm[0])+' from server '+str(server[0])+' to server'+str(s[0])
                                self.mc.Execute(vm[0], s[0], server[0])
                                # query = 'insert into migration values(\''+str(vm[0])+'\',\''+str(s[0])+'\',\''+str(server[0])+'\')'     
                                #self.cur.execute(query)
                                break 
                                
         # Load balancing small flavor server
        for server in server_info:
            if server[26] > low_vm_avg:
                mem_req = VM_FLAVOUR_RAM[0]
                for s in server_info:
                    if s[26] < low_vm_avg and s[22]-s[23] > mem_req:
                        for vm in vm_info:
                            if vm[23] == 0 and vm[24] ==server[0]:
                                server[23]-=mem_req
                                server[26]-=1
                                s[26]+=1
                                s[23]+=mem_req
                                print 'Migrating vm '+str(vm[0])+' from server '+str(server[0])+' to server'+str(s[0])
                                self.mc.Execute(vm[0], s[0], server[0])
                                #query = 'insert into migration values(\''+str(vm[0])+'\',\''+str(s[0])+'\',\''+str(server[0])+'\')'     
                                #self.cur.execute(query)                                      
                                break
    
    