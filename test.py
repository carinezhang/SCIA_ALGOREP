import mpi4py.MPI as mpi
import sys
import numpy as np

MAX_SIZE = 4096
center = 0
rank = mpi.COMM_WORLD.rank
size = mpi.COMM_WORLD.size

all_vars = []

def size_vars():
    '''
    Return the cumulate size of each elements in all_vars in the current
    processs.
    '''
    res = 0
    for i in all_vars:
        res += sys.getsizeof(i)
    return res

def ask_size():
    '''
    ask_size() do actually more than just ask the size of each all_vars list.
    The function return True if the process had been choosen to be the var
    host process.
    '''
    lens = []
    if rank == center:
        for i in range(1,size):
            lenght = mpi.COMM_WORLD.recv(source=i)
            print("Total lenght :{} in the process {}.".format(lenght, i))
            lens.append(lenght)
        #The process chosen to take the var is the one with lowest vars size
        amin = np.argmin(lens)+1
        for i in range(1, size):
            #We can tell everybody who get the var
            mpi.COMM_WORLD.send(amin, dest=amin)
        return amin
    else:
        mpi.COMM_WORLD.send(size_vars(), dest=center)
        b = mpi.COMM_WORLD.recv(source=center)
        return b == rank
        

def allocate(obj, r):
    '''
    Obj is the object to allocate, r is the rank of the process who call this
    function.
    Allocate is just a way to find somewhere to stock the variable.
    We need to check the size on each process and add the variable on a
    process with free space.
    It return the location of the variable (typically an index).
    '''
    #First ask center where there is enough space
    #If b is set to True, the current process is the one choosen
    b = ask_size()
    if b == rank:
        print("I'm the process {} and was choosen for hold the new data.".format(rank))
    if rank == center:
        obj_size = mpi.COMM_WORLD.recv(source=r)
        mpi.COMM_WORLD.send(obj_size, dest=b)
        pos = mpi.COMM_WORLD.recv(source=b)
        if pos < 0:
            print("Variable couldn't be allocated on any process.")
        else:
            print("0 sends {} to {}".format(pos+MAX_SIZE*(b-1), r))
            mpi.COMM_WORLD.send(pos + MAX_SIZE*(b-1), dest=r)
            print("0 sends {} to {}".format(pos+MAX_SIZE*(b-1), r))

        #Do something nice
    if rank == r:
        mpi.COMM_WORLD.send(sys.getsizeof(obj), dest=center)
    if rank == b:
        lenght = mpi.COMM_WORLD.recv(source=center)
        if size_vars() + lenght < MAX_SIZE:
            mpi.COMM_WORLD.send(len(all_vars), dest=center)
            #obj = mpi.COMM_WORLD.recv(source=center) <-- This is the modify
            #function function
        else:
            mpi.COMM_WORLD.send(-1, dest=center)
    if rank == r:
        res = mpi.COMM_WORLD.recv(source=center)
        return res


def main():
    if rang == centre:
        valeur = 100
        mpi.COMM_WORLD.send(valeur,dest=0)
        print("1 sends {} to 0.".format(valeur))
    elif rang == 0:
        valeur = mpi.COMM_WORLD.recv(source=1)
        print("received from 1 {}".format(valeur))

if __name__ == "__main__":
    allocate(rank+1, rank)
    allocate([i for i in range(2*rank+1)], rank)
    print("Vars: {1}  \tSize: {0}.".format(size_vars(), all_vars))
    sys.stdout.flush()

