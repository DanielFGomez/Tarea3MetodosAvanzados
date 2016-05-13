.PHONY: evolve

evolve:
	#gcc-5 tarea3.c -fopenmp	#para mac 
	cc  tarea3.c -lm -fopenmp
	time ./a.out 100 0.1
	python lee.py Estado_final.dat
clean: 
	rm *.dat
