import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if(len(sys.argv)!=3):
    print "Introduzca 2 archivos para correr el programa\n"
    print "Numero de parametros dados =", len(sys.argv)-1
    
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

r1=[]


x2=[]
y2=[]
z2=[]



for i in range(int(len(archivo2)-1)):
    a= archivo1[i].split()
    if(i==0):
        Radio=(float(a[0])**2+float(a[1])**2+float(a[2])**2)**0.5
    
    r1.append((float(a[0])**2+float(a[1])**2+float(a[2])**2)**0.5-Radio)
    r1.sort()
    

h=plt.hist(r1)

num=h[0]
rs=h[1]

print rs



'''
plt.plot(num,rs)
plt.show()
'''
