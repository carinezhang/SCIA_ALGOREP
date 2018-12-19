import mpi4py.MPI as mpi
import sys
import numpy as np

MAX_SIZE = 4096
centre = 0
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
            lenght = mpi.recv(source=i)
            lens.append(lenght)
        #The process chosen to take the var is the one with lowest vars size
        amin = np.argmin(lens)
        for i in range(1, size):
            #We can tell everybody who get the var
            mpi.COMM_WORLD.send(amin, dest=amin)
        return 0
    else:
        mpi.COMM_WORLD.send(size_vars(), dest=center)
        b = mpi.COMM_WORLD.recv(source=center)
        return b == rank
        

#Il manque un truc, il faut que le process qui appelle ca soit le seul a
#a envoyer obj
def allocate(obj):
    '''
    Allocate is just a way to find somewhere to stock the variable.
    We need to check the size on each process and add the variable on a
    process with free space.
    It return the location of the variable (typically an index).
    '''
    #First ask center where there is enough space
    b = ask_size()
    if rank == center:
        mpi.COMM_WORLD.send(sys.getsizeof(obj),dest=b) #<-- that is something to do in
        #modify I think
        #Do something nice
    elif rank == b:
        lenght = mpi.COMM_WORLD.recv(source=center)
        if size_vars() + lenght < MAX_SIZE:
            mpi.COMM_WORLD.send(1, dest=center)
            obj = mpi.COMM_WORLD.recv(source=center)

        #Do something nice
    else:
        lenght = mpi.COMM_WORLD.recv(source=center)
        if size_vars() + lenght < MAX_SIZE:
            #all_vars.append(obj)

        #Do something interesting
        

    #else send a message to center ?



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
    allocate([i for i in range(2*rank+1)])
    print("Vars: {1}  \tSize: {0}.".format(size_vars(), all_vars))
    sys.stdout.flush()

