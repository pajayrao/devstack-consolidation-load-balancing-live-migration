import mysql.connector as sql
import os,time

MYSQL_USER_NAME = 'root'
MYSQL_PASSWORD = '1234'
MYSQL_HOST_NAME = 'localhost'
MYSQL_DB = 'stack'

'''
sum=0

for _ in range(10):
    stat = time.time()
    c=11**11**6
    sum+= time.time()-stat
    time.sleep(1)
print sum/10	
'''

def gen_load(load_per=50):
	comp_time = 0.564104247093
	total_time = comp_time*100/load_per
	while 100:
		c=11**11**6
		time.sleep(total_time-comp_time)



conn = sql.connect(user = MYSQL_USER_NAME,password = MYSQL_PASSWORD,host = MYSQL_HOST_NAME,database = MYSQL_DB)
cur = conn.cursor()
while True:
	query = 'select * from lo'
	cur.execute(query)
	rows = cur.fetchall()
	load = rows[0][0]
	print "Load is "+str(load)
	gen_load(load-2)	
