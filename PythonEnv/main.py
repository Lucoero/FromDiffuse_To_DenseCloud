# -*- coding: utf-8 -*-
"""
MAIN SIMULATION
"""
# %% Seccion de importacion
import numpy as np
import Variables_Globales as variables
import write_file as wf
import forces
import verlet
import initialize_system as init_sys
import os
import time
#%% Aviso de que variables estamos usando
print("VARIABLES USED (Solar Mass, parsecs, years):")
print("---CLOUD INFO---\n")
print("CLOUD DENSITY (SM/pc^3):", variables.rho0)
print("CLOUD RADIUS (pc):", variables.R)
print("\n---CLUSTERS INFO---\n")
print("MASS PER CLUSTER (SM):", variables.m)
print("NUMBER OF CLUSTERS:", variables.N_cluster)
print("NEIGHBOURS CONSIDERED PER CLUSTER:", variables.numNeigh)
print("MEAN VELOCITY OF EACH CLUSTER (pc/yr):", variables.velMedia)
# print("NUMBER OF CLUSTERS USED TO COMPENSATE CoM:", variables.NCM)
print("DISSIPATION CONSTANT USED (yr^-1):", variables.k_dis)
print("\n---TIMES INFO---\n")
print("END TIME OF THE SIMULATION (yr):", variables.tmax)
print("MAXIMUM DT (yr):", variables.dtmax)
print('MINIMUM DT (yr):', variables.dtmin)
print("\n---JEANS MODEL ESTIMATES---\n")
print('CLOUD MASS NECCESSARY TO COLLAPSE (via JeanMass; SM):', variables.MJ)
print('JEANS LONGITUDE (pc):', variables.lambdaJ)
#print("FREE FALL TIME ESTIMATED (yr):", variables.tff  )
print("\n")
print("---SAVE PATH---\n", variables.path)
print("------------\n")
#%% Ejecucion principal
t0 = time.time()
print("Intializing System...\n")

pos0,vel0 = init_sys.Generacion_Sistema_Inicial(useSeed = True)

'''
pos0 = np.array([[-15.,0,0],
                 [15.,0,0],])
                 '''


print("System initialized. Simulating cloud...\n")

verlet.Temporal_Simulation(pos0,vel0)

print("\n \nSIMULATION ENDED. TIME SPENT (s):", time.time()-t0)
print("Positions saved in: \n",variables.path)