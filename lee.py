import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if(len(sys.argv)!=3):
    print "introduzca 2 parametros para correr el programa\n"
    print "parametros dados=", len(sys.argv)-1
    
    exit()
    

lectura1=str(sys.argv[1])
lectura2=str(sys.argv[2])

#existencia del archivo de entrada
try:
    archivo1=open(lectura1).read().split("\n")
except IOError:
    
   print "Error: el archivo "+lectura+ " no existe"
   exit()
try:
    archivo2=open(lectura2).read().split("\n")
except IOError:
    
   print "Error: el archivo "+lectura+ " no existe"
   exit()

x1=[]
y1=[]
z1=[]

x2=[]
y2=[]
z2=[]

for i in range(int(len(archivo1)-1)):
    a= archivo1[i].split()
    x1.append(a[0])
    y1.append(a[1])
    z1.append(a[2])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.scatter(x1,y1)
plt.show()
