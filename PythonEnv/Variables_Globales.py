# -*- coding: utf-8 -*-
"""
GLOSARIO DE VARIABLES GLOBALES
LOS CAMBIOS EN LOS PARAMETROS GLOBALES DE LA SIMULACION SE DEBEN HACER DESDE AQUI
"""
from numpy import pi
from numpy import sqrt

#%% Constantes gravitatorias
# G = 6.674e-11 # SI
G = 4.4797e-15 # pc^3 /(anno^2 MSol)


#%% Propiedades de la nube
# rho0 = 3e-17 kg / m^3; SI (Valor estandar de la densidad en nubes moleculares frias.)
rho0 = 443.37 # MSol / pc^3

# cs = 0.3 km / s; SI (Valor de la velocidad del sonido en este medio segun nuestras fuentes)
cs = 3.07e-7 # pc / year

A = 100*cs**2 # (pc / year)^2 (Intensidad de la presion.)

R = 60 # pc (Tamanno de la nube.)


N_cluster = 5*10**4 # Numero de cluster de particulas en la nube
numNeigh = 100 # Numeros de vecinos a considerar en los calculos (nunca mayor al numero de clusters)
if numNeigh > N_cluster:
    numNeigh = N_cluster

#%% Constantes de Mecanica Estadistica
kB = 8.6173E-05 # eV/K; Global para todas las funciones	
k_dis = 4*10**(-2) # Constante de disipacion, years**-1.


#%% Propiedades del cluster
#m = 10**7 # Kg
m = rho0 * (4/3 * pi * R**3)/N_cluster # Masas solares
h = 1. * (R/N_cluster**(1/3)) # pc / part^1/3 (Relacionado con el tamaño tipico del cluster.)



#%% Velocidades
#velMedia = 0.5 # SI (km/s)
velMedia = 5.11 * 10**(-7) #  (Velocidades medias encontradas en nubes moleculares.) Uds: pc/annos 

NCM = 1 # N de particulas para compensar la V_CM
if NCM > N_cluster:
    NCM = N_cluster//4
#%% De la simulacion en general
bar_refresh_rate = 10 # Ratio de actualizacion de la barra de progreso de tqdm
neighInfo_refresh_rate = 10 # Ratio de actualizacion de los vecinos

#%% Parámetros de Jeans

lambdaJ = sqrt(cs**2/(G*rho0))      #longitud de Jeans

MJ = rho0*lambdaJ**3        #masa de Jeans, nos dice a partir de qué masa la nube colapsa


#%% Variables de tiempo/Paso variable
eta = 0.03 # Factor de seguridad para el paso de tiempo (de 0.05 a 0.2). Es una escala de proporcionalidad
epsilon = 1.2*h # Si se hace el calculo, se observa que el paso de tiempo tiene sentido dimensionalmente
dt0 = None  # Initial dt considered (years)
dtmax = 500 # Max dt considered (years)
dtmin = 10e-3 # Min possible dt (years)
tmax = 6e5 # Tiempo total de simulacion (years)



#%% Paths
#path = r"ArchivosPosiciones/Pos.txt"
#path = r"D:\Carpetas de datos\Desktop\BuildNube\NubeMolecular_Data\StreamingAssets\8.txt"
path = r'/home/jmge55/projects/Proyecto_sim_formacion_estelar/BuildUnity_Data/StreamingAssets/8.txt'