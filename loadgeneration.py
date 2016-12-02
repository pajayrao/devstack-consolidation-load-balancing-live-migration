import time


'''
sum=0

for _ in range(10):
    stat = time.time()
    c=(11**11**5 + 12**11**5)*11
    sum+= time.time()-stat
    time.sleep(1)
print sum/10	

'''

load =45
x=0.0467851877213
t=x*100/load
while True:
	c=(11**11**5 + 12**11**5)*11
	time.sleep(t-x)
	

