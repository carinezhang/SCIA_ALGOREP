

test:
	mpirun --hostfile hostfile -n 4 python3 tests.py


example:
	mpirun --hostfile hostfile -n 4 python3 example.py


