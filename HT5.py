#Algoritmos y estructura de datos
#Seccion 20
#Marco Ramirez 19588

#Importa libreria simpy  y random
import simpy
import random


#Funcion para procesar los datos
def processes(name, env,arrivalT, cpu, ram, waiting):
    #Tiemp totalT, tomara el tiempo total del proceso
    global totalT
    #Almacen el tiempo del proceso 
    global processT 
    
    #Tiempo de llegada 
    yield env.timeout(arrivalT)
    #Empieza el proceso 
    startT = env.now 
    departureT = 0
    print (' Proceso %d en el tiempo %s ' % (name, startT))
    #Genera un numero aleatorio del 1 al 200 donde sera la cantidad de datos que procese
    procesdeata = random.randint(1,200)
    #Genera un numero aleatorio del 1 al 10 donde le asignara la Ram
    ram_needed = random.randint(1,10) 
    
    with ram.get(ram_needed) as queue1:
        
        print ('Proceso %d entra a la RAM en %s' % (name, env.now))
        print ('Ocupa %d en la RAM: %s' % (name, ram_needed))
        
        while procesdeata>0:
            #Uso del CPU con colas
            with cpu.request() as queue2: 
                
                yield queue2
                print ('Proceso %d entra al CPU en %s' % (name, env.now))
                
                yield env.timeout(1)
                #Ejecuta 3 procesos (velocidad del procesador)
                procesdeata = procesdeata -3 
                
                #Si la informacion del proceso es menos que 0 este lo concluye
                if procesdeata<=0: 
                    
                    procesdeata = 0
                    departureT = env.now 
                    print ('Proceso %d sale del CPU en el momento %s' %(name,departureT))
                #De lo contrario determina si tiene instruciones 
                else: 
                    alternData = random.randint(1,2)
                    
                    if alternData == 1:
                        
                        with waiting.request() as queue3:
                            
                            yield queue3
                            yield env.timeout(1)
                            
    #Tiempo total del proceso
    timeTotalData = departureT - startT
    #Se agregua el tiempo a la lista
    processT.append(timeTotalData)
    #Indica el tiempo exacto
    totalT = departureT 
                          
#Funcion para calcular la desviacion estandar
def desviacionEstandar (data, average):
    
    totaldE = 0
    for i in range(len(data)):
        
        totaldE = (data[i]-average)**2
        
    de = (totaldE/(len(data)-1.0))**(0.5)
    
    return de



#Informacion de la simulacion

env = simpy.Environment()
ram = simpy.Container(env, capacity=100)
cpu = simpy.Resource(env, capacity=2)
waiting = simpy.Resource(env, capacity = 1)
random.seed(12345)
interval = 10.0
totalT = 0
processT = []
totalDataProcess=200

#Funcion de todos los datos procesados
for i in range (totalDataProcess):
    
    env.process(processes(i,env,random.expovariate(1.0/interval),cpu,ram,waiting))

#Corre la simulacion
env.run()
Average = float(totalT)/float(totalDataProcess)
desviacionEstandar = desviacionEstandar(processT,Average)
4
#Datos
print ('Tiempo total: %d \nPromedio de tiempo por instruccion: %s \nDesviacion Estandar: %f' % (totalT, Average, desviacionEstandar))
