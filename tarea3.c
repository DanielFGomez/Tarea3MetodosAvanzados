#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
//#include "omp.h"
#define PI 3.14159265359
#define G 4.492E-3

void generar(int N,double R,double *r, double *v);

void imprime(FILE *f,int N,double *r,double *v, int A,double *Rcm,double m);

double calcular_masa(double radio2, double *r, double m, int N);

void calcular_cm(double *r, int N, double* Rcm);

void calcular_a(double *a,double *r, double *Rcm, int N, double m,double epsilon);

void leap_frog_step(double *Rcm,double m,double epsilon,double *r, double *v, double *a, double dt, int N);

int main(int arg, char **argc){

  int N=atoi(argc[1]);
  double epsilon=atof(argc[2]);
  int i; 
  double R=pow(N,1/3.0); //en Parsec
  double M=1.0; //masa solar
  double *Rcm;
  double rho=N/(4.0*PI*pow(R,3.0)/3);
  double rhoe=1.0/(4*PI*pow(epsilon,3.0)/3);
  double T=1.0/pow(rho*G,0.5);
  double dt=1.0/pow(rhoe*G,0.5);
  int TIME=(int) 10*T/dt;
  
  
  printf("\nNumero de cuerpos N=%d \n",N);
 
  printf("\nParamentros:\n \nG=%e \nM=%e \nR=%e\n",G,M,R);

  printf("\nParametros Temporales:\n");

  printf("\nTime=%f \n",T);

  printf("epsilon=%f \n",epsilon);
  
  printf("Time_step=%f \n",dt);

  printf("Pasos de tiempos dados:=%d \n",TIME);
  

  
  double *v;
  double *r;
  double *a;
  

  r=malloc(sizeof(double)*N*3);
  v=malloc(sizeof(double)*N*3);
  a=malloc(sizeof(double)*N*3);
  Rcm=malloc(sizeof(double)*3);

  
  generar(N,R,r,v);
 
  FILE *f;

  printf("\nGenerando datos iniciales\n");
  
  calcular_cm(r, N, Rcm);

  printf("Rcm x=%f, y=%f, z=%f \n",Rcm[0],Rcm[1],Rcm[2]);

  
  imprime(f,N,r,v,0,Rcm,M);

 
 
  printf("\n-----Comenzando leapfrog------\n");

  for(i=1;i<TIME;i++){//*dt<T;i++){
    
    leap_frog_step(Rcm,M,epsilon,r, v, a, dt, N);

  }
  
  FILE *F;


  printf("\nImprimiendo posiciones finales \n");

  
  imprime(F,N,r,v,1,Rcm,M);

  
 
   

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
    teta1=acos(2*(drand48()-0.5));
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


void imprime(FILE *f,int N,double *r,double *v, int A,double *Rcm,double m){
  if(A==0){
  f=fopen("Condiciones_iniciales.dat","w");
  }
 if(A==1){
  f=fopen("Estado_Final.dat","w");
  }
  int i;
  double zero=0.0;
  double V,Rdif,M,R2;

  fprintf(f,"%f %f %f %f %f %f %f %f\n",Rcm[0],Rcm[1],Rcm[2], zero,zero ,zero,zero, zero);
  

  for(i=0;i<N;i++){
    R2=((r[0+i]-Rcm[0])*(r[0+i]-Rcm[0])+(r[N+i]-Rcm[1])*(r[N+i]-Rcm[1])+(r[2*N+i]-Rcm[2])*(r[2*N+i]-Rcm[2]));
    M=calcular_masa(R2, r, m, N);
    V=(v[0+i]*v[0+i]+v[N+i]*v[N+i]+v[2*N+i]*v[2*N+i])*0.5*m;
    
    fprintf(f,"%e %e %e %e %e %e %e %e\n",r[0+i],r[N+i],r[2*N+i],v[0+i],v[N+i],v[2*N+i],V, G*M/sqrt(R2));	    
  }
  fclose(f);
}


double calcular_masa(double radio2, double *r, double m, int N){
  
  int i;
  int contador=0;
  double rad2;

  for(i=0;i<N;i++){

    rad2=r[i]*r[i] + r[i+N]*r[i+N] + r[i+2*N]*r[i+2*N];
    
    if(rad2<=radio2){
      contador+=1;
    }

  }

  return contador*m;

}

void calcular_cm(double *r, int N,double *Rcm){

  double x=0,y=0,z=0;
  int i=0;

  for(i=0;i<N;i++){
    x+=r[i] ;
    y+=r[i+N] ;
    z+=r[i+2*N] ;
   
}
  Rcm[0]=x/N;
  Rcm[1]=y/N;
  Rcm[2]=z/N;

}

void calcular_a(double *a,double *r, double *Rcm, int N, double m,double epsilon){
  
  double M=0;//calcular_masa()
  int i=0;
  double radio2=0;
  double RADIO;

  //#pragma omp parallel for private(radio2),private(M),private(RADIO)

  for(i=0;i<N;i++){

    radio2=r[i]*r[i]+r[i+N]*r[i+N]+r[i+2*N]*r[i+2*N];

    M=calcular_masa(radio2,r,m,N);

    RADIO=(r[i]-Rcm[0])*(r[i]-Rcm[0])+(r[i+N]-Rcm[1])*(r[i+N]-Rcm[1])+(r[i+2*N]-Rcm[2])*(r[i+2*N]-Rcm[2]);
    
    a[i]=-G*(r[i]-Rcm[0])*M/pow(RADIO + epsilon*epsilon,1.5);
    a[i+N]=-G*(r[i+N]-Rcm[1])*M/pow(RADIO + epsilon*epsilon,1.5);
    a[i+2*N]=-G*(r[i+2*N]-Rcm[2])*M/pow(RADIO + epsilon*epsilon,1.5);
    
  }
  
}

void leap_frog_step(double *Rcm,double m,double epsilon,double *r, double *v, double *a, double dt, int N){
  int i;
  //PRIMERA ACELERACION

  calcular_a(a,r, Rcm, N, m,epsilon);

  //kick
  for (i=0;i<N;i++){
    v[i]=v[i]+0.5*a[i]*dt;
    v[i+N]=v[i+N]+0.5*a[i+N]*dt;
    v[i+2*N]=v[i+2*N]+0.5*a[i+2*N]*dt;
  }
  //drift
 for (i=0;i<N;i++){
    r[i]=r[i]+v[i]*dt;
    r[i+N]=r[i+N]+v[i+N]*dt;
    r[i+2*N]=r[i+2*N]+v[i+2*N]*dt;
  }
  //kick

 calcular_a(a,r, Rcm, N, m,epsilon);

 for (i=0;i<N;i++){
    v[i]=v[i]+0.5*a[i]*dt;
    v[i+N]=v[i+N]+0.5*a[i+N]*dt;
    v[i+2*N]=v[i+2*N]+0.5*a[i+2*N]*dt;
  }
}
  
