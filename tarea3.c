#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#define PI 3.14159265359
void generar(int N,double R,double *r, double *v);
void imprime(FILE *f,int N,double *r,double *v);



int main(int arg, char **argc){

  int N=atoi(argc[1]);
  int i; 
  double R=pow(N,1/3.0); //en Parsec
  double M=1.0; //masa solar
  double G=4.49*pow(10,-3);

  printf("\nParametro N=%d \n",N);
 
  printf("\nParamentros:\n \nG=%e \nM=%e \nR=%e\n",G,M,R);
  
  printf("Generando datos iniciales\n");
 
  
  
  double *v;
  double *r;
  

  r=malloc(sizeof(double)*N*3);
  v=malloc(sizeof(double)*N*3);

  generar(N,R,r,v);
 
  FILE *f;
  imprime(f,N,r,v);
 
   

  return 0;
}

//------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------



void generar(int N,double R,double *r, double *v){
  int i;
  double r1,teta1,phi1;
  srand(N);
  
  for(i=0;i<N;i++){

    //numeros random
    
    r1=R*pow(drand48(),1.0/3.0);
    teta1=PI*drand48();
    phi1=2*PI*drand48();  
    
    //inicializando posiciones
    
    r[i]=r1*sin(teta1)*cos(phi1);
    r[i+N]=r1*sin(teta1)*sin(phi1);
    r[i+2*N]=r1*cos(teta1);  
    
    //inicializando velocidades
    v[i]=0.0;
    v[N+i]=0.0;
    v[2*N+i]=0.0;
  }

}


void imprime(FILE *f,int N,double *r,double *v){
  f=fopen("Condiciones_iniciales.dat","w");
  int i;
  for(i=0;i<N;i++){
    fprintf(f,"%e %e %e %e %e %e\n",r[0+i],r[N+i],r[2*N+i],v[0+i],v[N+i],v[2*N+i]);	    
  }
}
