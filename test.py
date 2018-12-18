import mpi4py.MPI as mpi
import sys

MAX_SIZE = 4096
centre = 0
rank = mpi.COMM_WORLD.rank
size = mpi.COMM_WORLD.size

all_vars = []

def size_vars():
    res = 0
    for i in all_vars:
        res += sys.getsizeof(i)
    return res

def allocate(obj):
    if size_vars() + sys.getsizeof(obj) < MAX_SIZE:
        all_vars.append(obj)
    #else send a message to center ?



def ask_center(p):
    if rank == k:
        mpi.COMM_WORLD.send()


def main():
    if rang == centre:
        valeur = 100
        mpi.COMM_WORLD.send(valeur,dest=0)
        print("1 sends {} to 0.".format(valeur))
    elif rang == 0:
        valeur = mpi.COMM_WORLD.recv(source=1)
        print("received from 1 {}".format(valeur))

if __name__ == "__main__":
    allocate(rank+1)
    print("Vars: {1}\tSize: {0}.".format(size_vars(), all_vars))
    sys.stdout.flush()

