#Automation and Consolidation of Virtual Machine
##Abstract
Virtualization of Operating Systems is a method of running multiple instances of different OS on the same system. Along with the benefits of reduced costs and easy implementation, virtualization provides features to move VMs across different servers. Migration of VMs is the concept of moving VMs across servers either by stopping the VM on the current server or in real time. The existing technology involves manual migrations of live VM across server, which includes a lot of redundancy which is not a practical solution for large cluster of servers.The purpose of this paper is to introduce a system supported by automated consolidation and load balancing techniques which results in efficient and optimized migration.


##Introduction 




Virtualization of Operating Systems is the method by which multiple instances of different OS are implemented on the same system. The concept of VM enables the administrator to run a VM on the preferred platform without having to install the OS on a dedicated server.This concept is largely used in data centers to run multiple VMs on powerful servers. To improve the utility of virtualization, VMs are moved across different servers.


Migration of VMs is the process of moving the instances of the virtual OS across multiple servers. These migrations can be done either by switching off the VM on the current server or while the VM is still active . Live Migration is the method of moving running VMs across active servers .The major advantages of moving the active VM without actually stopping it is that it ensures that the QoS is met along with minimal downtime .Post-Copy Migration and Pre-Copy Migration are the two types of Live Migration techniques. In pre-copy migration, the memory pages are first copied and then the VM is migrated from source to destination. In contrast, post-copy migration does the memory pages migration after the VM is moved to the destination.


To improve the efficiency of live migration, we use consolidation and load balancing techniques.Consolidation of Virtual Machines on servers is a procedure of finding the optimal number of active servers on which all the VM load can be effectively managed.Load balancing is a process of efficiently balancing the load amongst servers without overloading any of them. Manual migration, which involves human intervention has a few disadvantages including useless migrations,redundant migrations, ineffective load balancing and server handling. For large data centers with more than 1000 nodes, it is impractical for humans to get involved in the consolidation or load balancing process.


##Existing Works


The current approach to live migration of multiple virtual machines involves manual migration by solving the virtual machine scheduling problem for the considered set of inputs, desired outputs and the constraints.ADD MORE PAPERS
Existing works in the domain includes a multiple VM migration scheduling algorithm [1]. This algorithm introduces inter-VM dependencies, underlying network topology and its bandwidth, and maximises the migration performance.
An optimized approach to live migration is to reduce migration time by using log records [2]. Here , the migration time is reduced by transferring the pages not recently used and by sending the modifications of log records instead of resending the dirty pages. However, parallelized migrations cannot be carried out by this method.(*reason*)
Virtualization technology for different hypervisor implementations [3] involves an approach in which a VM image that is dependent on the destination is generated before migration. This solves the problem of generation of dead copies of VM images during migration. 




For all the approaches to live migration discussed above, as the size of the data center and therefore, the number of active servers increase, the efficiency largely decreases. This is because all these migrations are carried out manually, which becomes increasingly difficult with the increasing number of active servers. This calls for the need for automation and consolidation of virtual machines.
 
##Proposed model


The proposed model tries to achieve automated consolidation and deconsolidation of the VMs across multiple servers implementing hypervisors while managing the varying load across systems and thereby load balancing across these servers.It takes into account different types of VM with different system requirements while migrating. SLA along with basic system requirements must be considered while consolidating the system. It also considers VM system and network requirements when migrating the VM. This helps in achieving quick live migration and system setup along with reducing useless migrations which adversely impacts system performance. .
(*add description about trhe diagram*)

  Fig 1- System Modules




##Modules Description
###Auto Consolidator/Deconsolidator

This module controls consolidation and deconsolidation of VMs on servers. It calculates the average maximum load (Loadmax) and average minimum load (Loadmin ) on servers to make decisions for  migration. For consolidation, average load (Loadavg) must be less than Loadmin and for deconsolidation, the Loadavg must be higher than the Loadmax. For every consolidation process, a low priority server is switched off while for every deconsolidation process a new server is switched on.Hence depending upon total VM load, optimal number of servers are kept active which ensures minimal power consumption.








###Load Balancer

This module balances load across servers such that all servers have equal number of VMs of each class (i.e. low load, medium load and high load VM). Keeping each class of VM equally distributed on  servers makes sure that load is balanced in real time.

###Abrupt Load Manager

This process is initiated when the server load abrubtly raises above  LoadMax and stalls the server. Load balancing is initiated to balance load across servers.  If this does not help then deconsolidation process is initiated which activates  a new server thereby keeping current server load (Loadi) below Loadmax.   


###Migration Predictor

From the a IEEE paper (will add later) , migration is efficient if class of the VM is changed before load on the VM reaches the boundary of the class change.This gives the load balancer enough time to move VM to high resource server. This prediction works by taking real-time system load and then changing VM  class whenever appropriate.


###MySQL Database for
####Server Data 
Server data provides server information to other modules that work on servers. The server data module updates this data in real-time. 
####VM Data
Real-time information related to VMs is collected here. Class of each VM is specified here along with its load history , resources allocated to it and its future load prediction.This is used by the Load Predictor to predict the load change that can occur and prepare the server for the increased or decreased load.
####Migration Data
All data related to migration from migration predictor, load balancer, auto consolidator / deconsolidator and abrupt load manager modules are added here. This synchronizes all migration involved modules and Migration Controller uses this information to make optimal migrations.
	
###Migration Controller
This module takes care of the migration for the VM across the servers. The resources in the migrating system is first checked making sure there won't be any useless migration .Then the network bandwidth is checked between the source and destination servers so that it is below the threshold value so that live migration process happens on very short interval of time. This makes sure that the VM downtime goes unnoticed. 



References 


[1] - Tusher Kumer Sarker and Maolin Tang, “Performance-driven Live Migration of Multiple Virtual Machines in Datacenters”, IEEE International Conference on Granular Computing(GrC), 2013.
[2] - Anju Mohan and Shine S., “An Optimized Approach for Live VM Migration using Log Records”, IEEE - 31661, 4th ICCCNT - 2013, July 4-6, 2013, Tiruchengode, India.
[3] - Y. Ashino and M. Nakae, “Virtual Machine Migration Method Between Different Hypervisor Implementations and its Evaluation”, 26th IEEE International Conference on Advanced Information Networking and Applications Workshops, WAINA 2012. 


