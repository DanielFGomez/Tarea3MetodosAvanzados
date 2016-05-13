import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


if(len(sys.argv)!=2):
    print "Introduzca 1 archivo para correr el programa\n"
    print "Numero de parametros dados =", len(sys.argv)-1
    
    exit()
    

lectura1=str(sys.argv[1])


#existencia del archivo de entrada

try:
    archivo1=open(lectura1).read().split("\n")
except IOError:
    
   print "Error: el archivo "+lectura+ " no existe"
   exit()



r1=[]


for i in range((len(archivo1)-1)):
    a= archivo1[i].split()
    
    if(i==0):
        Rcmx=float(a[0])
        Rcmy=float(a[1])
        Rcmz=float(a[2])
    
    r1.append(((float(a[0])-Rcmx)**2+(float(a[1])-Rcmy)**2+(float(a[2])-Rcmz)**2)**0.5)

r1.sort()
    

h=plt.hist(r1,bins=15)
plt.title("Histograma en R")
plt.show()


num=np.zeros(len(h[0])-1)#numero de particulas en cada bin

rs=np.zeros(len(h[0])-1)#radio al bin en logaritmo

dens=np.zeros(len(h[0])-1)#densidad

radio=np.zeros(len(h[0])-1)#radio

print h[1][-1],  h[0][-1]

for i in range(1,len(h[0])-1):
	rs[i]=np.log(h[1][i+1])



print h[1][-1],  h[0][-1]

for i in range(1,len(h[0])-1):
	
	rs[i]=np.log(h[1][i+1])
		
	if(h[0][i+1]==0):
		print h[0][i+1],i
	
	num[i]=np.log(h[0][i+1]+1)
		
		
	dens[i]=h[0][i]/h[1][i]**2
		
	radio[i]=h[1][i]

densidad=num-2*rs-np.log(4*np.pi)-np.log(h[1][1]-h[1][0])#log de la densidad

f=open("Log_vs_Log.dat","w")

for i in range(len(densidad)):
   f.write(str(rs[i])+" "+str(densidad[i])+"\n")

f.close()

print "densidad\n\n\n", densidad 

plt.plot(radio,dens,label="Densidad")
plt.title("rho vs r ")
plt.legend()

plt.show()

plt.scatter(rs,densidad,label="Log(\rho)(N,r)")
plt.title(" log(rho) vs log(r) ")
plt.legend()
plt.show()



densdata=np.array(densidad)

alph=1
bet=2
log_R_c=np.log(1)
log_rho0=np.log(30)
r=np.array(rs)


def densities(alph,bet,log_R_c,log_rho0,r):
	rho=np.exp(log_rho0)/(((np.exp(r)/np.exp(log_R_c))**alph)*((1+np.exp(r)/np.exp(log_R_c))**bet))
	return (rho)

def loglikelihood(y_obs, y_model):
	chi_squared = (1.0/2.0)*np.sum((y_obs-y_model)**2)
	return (-chi_squared)


densmodel=[]

alph_walk = np.empty((0))
bet_walk = np.empty((0))
log_R_c_walk = np.empty((0))
log_rho0_walk = np.empty((0))
logl_walk = np.empty((0))

alph0=0.1
bet0=2
log_R_c0=np.log(1)
log_rho00=np.log(0.0007)

alph_walk = np.append(alph_walk, alph0)
bet_walk = np.append(bet_walk, bet0)
log_R_c_walk = np.append(log_R_c_walk, log_R_c0)
log_rho0_walk = np.append(log_rho0_walk, log_rho00)


densmodel = np.log(densities(alph_walk[0],bet_walk[0],log_R_c_walk[0],log_rho0_walk[0],r))
logl_walk = np.append(logl_walk, loglikelihood(densdata, densmodel))
print 'Los parametros iniciales fueron'
print 'alph0='+str(alph_walk[0])
print 'bet0='+str(bet_walk[0])
print 'R_c0='+str(log_R_c_walk[0])
print 'rho00='+str(log_rho0_walk[0])

print 'El logaritmo de la funcion de likelihood es='+str(logl_walk[0])

n_iterations = 1000
densprime=[]
for i in range(n_iterations):
	alph0_prime = np.random.normal(alph_walk[i],1)
	bet0_prime = np.random.normal(bet_walk[i],0.01)
	log_R_c0_prime = np.random.normal(log_R_c_walk[i],1)
	log_rho00_prime = np.random.normal(log_rho0_walk[i],1)
	
	
	densmodel = np.log(densities(alph_walk[i],bet_walk[i],log_R_c_walk[i],log_rho0_walk[i],r))
	densprime = np.log(densities(alph0_prime,bet0_prime,log_R_c0_prime,log_rho00_prime,r))
	
	logl_prime = loglikelihood(densdata, densprime)
	logl_init = loglikelihood(densdata, densmodel)
	
	alpha = np.exp(logl_prime-logl_init)
	if(alpha>=1.0):
		alph_walk  = np.append(alph_walk,alph0_prime)
		bet_walk  = np.append(bet_walk,bet0_prime)
		log_R_c_walk  = np.append(log_R_c_walk,log_R_c0_prime)
		log_rho0_walk = np.append(log_rho0_walk,log_rho00_prime)
	
		logl_walk = np.append(logl_walk, logl_prime)
	else:
		beta = np.random.random()
		if(beta<=alpha):
			alph_walk  = np.append(alph_walk,alph0_prime)
			bet_walk  = np.append(bet_walk,bet0_prime)
			log_R_c_walk  = np.append(log_R_c_walk,log_R_c0_prime)
			log_rho0_walk = np.append(log_rho0_walk,log_rho00_prime)
			
			logl_walk = np.append(logl_walk, logl_prime)
		else:
			alph_walk  = np.append(alph_walk,alph_walk[i])
			bet_walk  = np.append(bet_walk,bet_walk[i])
			log_R_c_walk  = np.append(log_R_c_walk,log_R_c_walk[i])
			log_rho0_walk = np.append(log_rho0_walk,log_rho0_walk[i])
			
			logl_walk = np.append(logl_walk, logl_init)




count, bins, ignored =plt.hist(alph_walk, 20, normed=True)
plt.title('Histograma de alpha', fontsize=12)
plt.show()



count, bins, ignored =plt.hist(bet_walk, 20, normed=True)
plt.title('Histograma de beta', fontsize=12)
plt.show()



count, bins, ignored =plt.hist(log_R_c_walk, 20, normed=True)
plt.title('Histograma de log_R_c', fontsize=12)
plt.show()



count, bins, ignored =plt.hist(log_rho0_walk, 20, normed=True)
plt.title('Histograma de log_rho0', fontsize=12)
plt.show()



Plot2=plt.figure(figsize=(10,10))
plt.plot((logl_walk))
plt.title('Evolucion de funcion de error de \chi^{2}', fontsize=12)
plt.grid()
plt.show()



max_likelihood_id = np.argmax(logl_walk)
best_alph = alph_walk[max_likelihood_id]
best_bet = bet_walk[max_likelihood_id]
best_log_R_c = log_R_c_walk[max_likelihood_id]
best_log_rho0 = log_rho0_walk[max_likelihood_id]

print 'Los parametros mas probables encontrados fueron'
print 'alph='+str(best_alph)
print 'bet='+str(best_bet)
print 'log_R_c='+str(best_log_R_c)
print 'log_rho0='+str(best_log_rho0)


denstest=[]
rtest=np.linspace(-r[0],r[len(h[0])-2],1000)
denstest=densities(best_alph,best_bet,best_log_R_c,best_log_rho0,rtest)
plt.scatter(r,densdata)
plt.plot(rtest,np.log(denstest))


plt.show()

