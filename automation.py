import numpy as np

n=int(input("Enter the number of servers   :"))
load=np.zeros(n+100);

max_threshold=int(input("Enter the Max Load Threshold  "))
min_threshold=int(input("Enter the Min Load Threshold  "))
print " \n\n"
nh=int(input("Enter the number of high load VM   "))
nm=int(input("Enter the number of medium load VM   "))
nl=int(input("Enter the number of low load VM    "))


no_of_high_VM=int(nh/n)+1
no_of_medium_VM=int(nm/n)+1
no_of_low_VM=int(nl/n)+1


print "\n\nAverage number of high load Vm on each server is "+str(no_of_high_VM);
print "Average number of medium load Vm on each server is "+str(no_of_medium_VM);
print "Average number of low load Vm on each server is "+str(no_of_low_VM);
m=0;
while True :
    total_load=0;
    for i in range(n):
        load[i]=int(input("\n\nEnter the load on server " +str(i)+"   "))
        total_load+=load[i]
    avg_load=total_load/n   
    print "Average Load on each server is "+str(avg_load)
    if avg_load>max_threshold:
        print "\n\nDeconsolidation process initiated "
        m=n;
        m+=1;
    
        
    elif avg_load<min_threshold:
        print "\n\nConsolidation process initiated "
        m=n;
        m-=1;
    else:
        print "No consolidation or deconsolidation"    
    no_of_high_VM=int(nh/m)+1
    no_of_medium_VM=int(nm/m)+1
    no_of_low_VM=int(nl/m)+1   
    print "\n\nNumber of Active Server is "+str(m)
    print "Average number of high load Vm on each server is "+str(no_of_high_VM);
    print "Average number of medium load Vm on each server is "+str(no_of_medium_VM);
    print "Average number of low load Vm on each server is "+str(no_of_low_VM);
    n=m