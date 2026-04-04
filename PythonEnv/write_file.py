import numpy as np
import Variables_Globales as variables

path = variables.path

def Pos_To_Txt(posArr, nIter = 0, dt = 0.):
    """
    Entrada:
        posArr: Array de posiciones a ese tiempo
        path: Path en el que colocar el fichero
        nIter: Numero de la iteracion temporal en la que nos encontramos (para unity)
        dt: Intervalo de tiempo actual. Para timeline de Unity
    Salida:
        -Un fichero Txt con las posiciones 
    """
    fichero = open(path,"a")
    try:
        fichero.write(str(nIter)+ " " + str(dt) + "\n")
        for i in range(len(posArr[:,0])):
            fichero.write("{:.6f} {:.6f} {:.6f}".format(posArr[i,0],posArr[i,1],posArr[i,2])+"\n")
    except:
        print("Ha ocurrido un error en Pos_To_TxT")
        fichero.close()
        raise
        return
    fichero.close()
    return 

def Create_File(nPart, endTime, pos0):
    """
    Create_File:
        Dada las particulas iniciales, el tiempo final de la simulacion, y las posiciones inciales,
        crea el fichero y rellena los datos basicos en el path deseado.
    """
    
    # Borramos el fichero
    fichero = open(path,"w")
    fichero.write(str(nPart) + " " + str(endTime) + "\n")
    fichero.close()
    # Escribimos en el fichero
    Pos_To_Txt(pos0)
    return 
