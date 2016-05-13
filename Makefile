.PHONY: evolve
N:=500
epsilon:=0.1

evolve:
	#gcc-5 tarea3.c -fopenmp	#para mac 
	gcc  tarea3.c -lm -fopenmp -o evolve
	time ./evolve $(N) $(epsilon)
	python lee.py "Estado_Final.dat"
clean: 
	rm *.dat
