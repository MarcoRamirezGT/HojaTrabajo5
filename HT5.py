#Algoritmos y estructura de datos
#Seccion 
import simpy
import random


def processes(name, env,arrivalT, cpu, ram, waiting):
    
    global totalT 
    global processT 
    
    yield env.timeout(arrivalT) 
    startT = env.now 
    departureT = 0
    print (' Proceso %d en el tiempo %s ' % (name, startT))
    
    procesdeata = random.randint(1,200) 
    ram_needed = random.randint(1,10) 
    
    with ram.get(ram_needed) as queue1:
        
        print ('Proceso %d entra a la RAM en %s' % (name, env.now))
        print ('Ocupa %d en la RAM: %s' % (name, ram_needed))
        
        while procesdeata>0:
            
            with cpu.request() as queue2: 
                
                yield queue2
                print ('Proceso %d entra al CPU en %s' % (name, env.now))
                
                yield env.timeout(1)
                procesdeata = procesdeata -3 
                
                if procesdeata<=0: 
                    
                    procesdeata = 0
                    departureT = env.now 
                    print ('Proceso %d sale del CPU en el momento %s' %(name,departureT))
                    
                else: 
                    alternData = random.randint(1,2)
                    
                    if alternData == 1:
                        
                        with waiting.request() as queue3:
                            
                            yield queue3
                            yield env.timeout(1)
                            
    timeTotalData = departureT - startT 
    processT.append(timeTotalData) 
    totalT = departureT 
                          
def desviacionEstandar (data, average):
    
    totaldE = 0
    for i in range(len(data)):
        
        totaldE = (data[i]-average)**2
        
    de = (totaldE/(len(data)-1.0))**(0.5)
    
    return de




env = simpy.Environment()
ram = simpy.Container(env, capacity=100)
cpu = simpy.Resource(env, capacity=2)
waiting = simpy.Resource(env, capacity = 1)
random.seed(12345)
interval = 10.0
totalT = 0
processT = []
totalDataProcess=200


for i in range (totalDataProcess):
    
    env.process(processes(i,env,random.expovariate(1.0/interval),cpu,ram,waiting))


env.run()
Average = float(totalT)/float(totalDataProcess)
desviacionEstandar = desviacionEstandar(processT,Average)
4
print ('Tiempo total: %d \nPromedio de tiempo por instruccion: %s \nDesviacion Estandar: %f' % (totalT, Average, desviacionEstandar))
