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
    a= archivo2[i].split()
    if(i==0):
        Rcmx=float(a[0])
        Rcmy=float(a[1])
        Rcmz=float(a[2])
    
    r1.append(((float(a[0])-Rcmx)**2+(float(a[1])-Rcmy)**2+(float(a[2])-Rcmz)**2)**0.5)

r1.sort()
    
binRadios=np.linspace(0,np.sqrt(max(r1)))**2
varh=plt.hist(r1,bins=binRadios)
plt.show()

h=plt.hist(r1,bins=30)
plt.show()


num=np.zeros(len(h[0])-1)
rs=np.zeros(len(h[0])-1)
dens=np.zeros(len(h[0])-1)
radio=np.zeros(len(h[0])-1)

suma=0
print("h[0]",h[0],"\n")
print("h[1]",h[1],"\n")

for i in range(len(h[0])-1):
    rs[i]=np.log(h[1][i+1])
    suma=h[0][i+1]
    num[i]=np.log(suma)

    
    dens[i]=h[0][i]/h[1][i]**2
    radio[i]=h[1][i]
   
print("num=",num)
print("rs=",rs)
print(np.pi)

densidad=num-2*rs-np.log(4*np.pi)-np.log(h[1][1]-h[1][0])
plt.plot(radio,dens,label="Densidad")
plt.legend()
plt.show()

plt.scatter(rs,densidad,label="$Log(\rho)(N,r)$")
plt.legend()
plt.show()

