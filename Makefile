.PHONY: evolve

evolve:
	gcc-5 tarea3.c -fopenmp	 
	time ./evolve 100 0.1
	python lee.py Estado_final.dat
clean: 
	rm *.dat
