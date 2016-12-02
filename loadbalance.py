import numpy as np

n=int(input("Enter the number of servers "))

highLoadVM=np.zeros(n);
lowLoadVM=np.zeros(n);
mediumLoadVM=np.zeros(n);
noOfHighLoad=0;
noOfLowLoad=0;
noOfMediumLoad=0;


for i in range(n):
    highLoadVM[i]=int(input("Enter number of high load VM on server  "+str(i)+"  "))
    mediumLoadVM[i]=int(input("Enter number of medium load VM on server  "+str(i)+"  "))
    lowLoadVM[i]=int(input("Enter number of low load VM on server  "+str(i)+"  "))
   
    noOfHighLoad+=highLoadVM[i]
    noOfMediumLoad+=mediumLoadVM[i]
    noOfLowLoad+=lowLoadVM[i]
    
    
avgNoOfHighLoadVM=int(noOfHighLoad/n)
avgNoOfMediumLoadVM=int(noOfMediumLoad/n)
avgNoOfLowLoadVM=int(noOfLowLoad/n)

print "Average number of high load Vm per server "+str(avgNoOfHighLoadVM)
print "Average number of medium load Vm per server "+str(avgNoOfMediumLoadVM)
print "Average number of low load Vm per server "+str(avgNoOfLowLoadVM)

total=0

for i in range(n):
    while highLoadVM[i]>avgNoOfHighLoadVM :
        for j in range(n):
            if highLoadVM[j] < avgNoOfHighLoadVM :
                print "Moving High VM from server "+str(i) + "    to   "+str(j);
                highLoadVM[i]-=1;
                highLoadVM[j]+=1;
                break;
        print str(highLoadVM[i]) + "  " + str(avgNoOfHighLoadVM)    
        if highLoadVM[i]+2>=avgNoOfHighLoadVM and highLoadVM[i]<=2+avgNoOfHighLoadVM :  
            break
        


for i in range(n):
    while mediumLoadVM[i]>avgNoOfMediumLoadVM :
        for j in range(n):
            if mediumLoadVM[j] < avgNoOfMediumLoadVM :
                print "Moving Medium VM from server "+str(i) + "   to   "+str(j);
                mediumLoadVM[i]-=1;
                mediumLoadVM[j]+=1;

                break;    
         
        if mediumLoadVM[i]+2>=avgNoOfMediumLoadVM and mediumLoadVM[i]<= 2+avgNoOfMediumLoadVM :  
            break   
        


for i in range(n):
    while lowLoadVM[i]>avgNoOfLowLoadVM :
        for j in range(n):
            if lowLoadVM[j] < avgNoOfLowLoadVM :
                print "Moving Low VM from server "+str(i) + "  to    "+str(j);
                lowLoadVM[i]-=1;
                lowLoadVM[j]+=1;
                break;            
        if lowLoadVM[i]+2>=avgNoOfLowLoadVM and lowLoadVM[i]<=1+avgNoOfLowLoadVM:  
            break   
    
         
                
                



        
       
       
    
