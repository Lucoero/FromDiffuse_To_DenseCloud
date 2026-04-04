import numpy as np
import numpy.random as rd
import write_file as wf
import Variables_Globales as variables

# IMPORTACION DE VARIABLES GLOBALES

m = variables.m
velMedia = variables.velMedia

R = variables.R
N = variables.N_cluster

tmax = variables.tmax
path = variables.path

def Initialize_Velocities(red):
    velScale = np.random.random_sample(size = (np.shape(red)[0],3))
    velScale = Adjust_CM_Velocity(velScale)
    return velScale*velMedia

def Adjust_CM_Velocity(vel):
    ##Para que la velocidad del centro de masas sea ínfima
    velScale = vel-np.sum((m*vel), axis = 0)/(m*N)
    return velScale
def Generacion_Sistema_Inicial(useSeed = False, seed = 0): 
    '''
    Entrada: 
    N:número de partículas, m:masa de las partículas, r:radio de las partículas, T:temperatura inicial del sistema,
    R:radio de la nube molecular, sigma:radio de los primeros vecinos
    tmax: Tiempo maximo que va a durar la simulacion (en años)
    Salida: 
    pos: posición inicial de las partículas, vel: velocidad inicial de las partículas
    useSeed: Para fijar los numeros random
    '''
    if useSeed:
        np.random.seed(seed)
    else:
        np.random.seed() # Al no pasarle parametros es random
     
     #rho = R*np.random.random_sample(N) - R/2    # nos da la coordenada radial
    
    u = np.random.random_sample(N)
    rho = R*(u**(1/3))
    
    theta = np.random.rand(N)*2*np.pi
    #phi = np.random.rand(N)*np.pi
    phi = np.arccos(2*np.random.rand(N)-1)      #phi más correcto
    
    pos = np.zeros((N,3))
    
    pos[:,0] = rho*np.sin(phi)*np.cos(theta)    # x
    pos[:,1] = rho*np.sin(phi)*np.sin(theta)    # y
    pos[:,2] = rho*np.cos(phi)                  # z

    vel = Initialize_Velocities(pos)
    
    wf.Create_File(nPart = N, endTime = tmax, pos0 = pos) # Creando el fichero
    return pos, vel
