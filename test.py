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
        compteur = 0
        indices = []
        st = mpi.Status()
        while(compteur < size - 1):
            lenght = mpi.COMM_WORLD.recv(source=mpi.ANY_SOURCE, status=st)
            #print("Total lenght: {} in the process {}.".format(lenght, st.source))
            lens.append(lenght)
            indices.append(st.source)
            compteur += 1
        #The process chosen to take the var is the one with lowest vars size
        amin = indices[np.argmin(lens)]
        for i in range(1, size):
            #We can tell everybody who get the var
            mpi.COMM_WORLD.send(amin, dest=i)
        return amin
    else:
        mpi.COMM_WORLD.send(size_vars(), dest=center)
        #print("Process {} sends {}(size_var) to {}.".format(rank, size_vars(), center))
        b = mpi.COMM_WORLD.recv(source=center)
        #print("Process {} receives {}(b) from {}.".format(rank, b, center))
        return b == rank
        

def allocate(obj, src):
    '''
    Obj is the object to allocate, src is the rank of the process who call this
    function.
    Allocate is just a way to find somewhere to stock the variable.
    We need to check the size on each process and add the variable on a
    process with free space.
    It return the location of the variable (typically an index).
    '''
    #First ask center where there is enough space
    #If b is set to True, the current process is the one choosen
    b = ask_size()
    #if b == True and rank != center:
    #    print("I'm the process {} and I was choosen for hold the new data.".format(rank))
    if rank == center:
        obj_size = mpi.COMM_WORLD.recv(source=src)
     #   print("Center receives {}(obj_size) from {}.".format(obj_size, src))
        mpi.COMM_WORLD.send(obj_size, dest=b)
    #    print("Center sends {}(obj_size) to {}.".format(obj_size, b))
        pos = mpi.COMM_WORLD.recv(source=b)
    #    print("Center receives {}(pos) from {}.".format(pos, b))
        if pos < 0:
            print("Variable couldn't be allocated on any process.")
        else:
            mpi.COMM_WORLD.send(pos + MAX_SIZE*(b-1), dest=src)
    #        print("0 sends {}(update pos) to {}".format(pos+MAX_SIZE*(b-1),src))
    if rank == src:
        mpi.COMM_WORLD.send(sys.getsizeof(obj), dest=center)
    #    print("Source, process {}, sends {}(obj_size) to center.".format(rank, sys.getsizeof(obj)))
    if b == True and rank != center:
        lenght = mpi.COMM_WORLD.recv(source=center)
    #    print("Process {} receives {}(lenght) from center.".format(rank, lenght))
        if size_vars() + lenght < MAX_SIZE:
            mpi.COMM_WORLD.send(len(all_vars), dest=center)
    #        print("Process {} sends {}(indice) to center.".format(rank, len(all_vars)))
            #obj = mpi.COMM_WORLD.recv(source=center) <-- This is the modify
            #function function
        else:
            mpi.COMM_WORLD.send(-1, dest=center)
    if rank == src:
        res = mpi.COMM_WORLD.recv(source=center)
        print("Process {} receives {}(indice) from center.".format(rank, res))
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
    al = allocate(rank+1, 2)
    print(al)
    print("-----")
    allocate([i for i in range(2*rank+1)], 3)
    print("Vars: {1}  \tSize: {0}.".format(size_vars(), all_vars))
    sys.stdout.flush()

