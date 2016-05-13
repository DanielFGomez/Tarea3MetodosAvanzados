.PHONY: evolve

evolve:
	#gcc-5 tarea3.c -fopenmp	#para mac 
	gcc  tarea3.c -lm -fopenmp -o evolve
	time ./evolve 500 0.1
	python lee.py "Estado_Final.dat"
clean: 
	rm *.dat
