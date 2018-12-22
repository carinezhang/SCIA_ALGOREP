from mpi4py import MPI
import time
import sys
import numpy as np
from enum import IntEnum
from slave import Slave

Tags = IntEnum('Tags', 'GET_SIZE ALLOC READ READY START DONE EXIT')
MAX_SIZE=6

class Master:
    """
    The main process creates one or more of this class that handle groups of
    slave processes
    """
    
    def __init__(self, slaves = None):
        
        if slaves is None:
            slaves = []
            
        self.comm = MPI.COMM_WORLD
        self.status = MPI.Status()        
        self.slaves = set(slaves)
    
    def get_size(self):
        '''
        get_size() get a list of tuple with the number of the processus and its size
        '''
        lens = []
        for i in range(1,self.comm.Get_size()):
            self.comm.send(None, dest=i, tag=Tags.GET_SIZE)
            length = self.comm.recv(source=i, tag=Tags.GET_SIZE)
            print("Total length :{} in the process {}.".format(length, i))
            lens.append((i,length))
        return lens


    def allocate(self, obj):
        lens = sorted(self.get_size(), key=lambda x: x[1], reverse=True)
        if lens[0][1] >= MAX_SIZE:
            print('not enough space')
        size = lens[0][1]
        if MAX_SIZE - size >= len(obj): #if we have enough space to stock everything at once
            p = lens[0][0]
            size = lens[0][1]
            self.comm.send((obj, time.time()), dest=p, tag=Tags.ALLOC)
            var = self.comm.recv(source=p, tag=Tags.ALLOC)
            return (type(obj), ['{}-{}'.format(p, var)])
        
        #when the list can't fit in one process
        list_var = []
        curr = 0
        for p, length in lens:
            disponible_size = MAX_SIZE - length
            up = curr + disponible_size
            if up > len(obj):
                up = len(obj) - 1
            self.comm.send((obj[curr:up], time.time()), dest=p, tag=Tags.ALLOC)
            list_var.append('{}-{}'.format(p, self.comm.recv(source=p, tag=Tags.ALLOC)))
            curr += disponible_size
            if curr > len(obj):
                break
        return (list, list_var)

    def read(self, var):
        var_list = var[1]
        if len(var[1]) <= 1:
            v = var_list[0].split('-')
            p = int(v[0])
            key = v[1]
            self.comm.send(key, dest=p, tag=Tags.READ)
            return self.comm.recv(source=p, tag=Tags.READ)
        res = []
        for v in var_list:
            p = int(v.split('-')[0])
            key = v.split('-')[1]
            self.comm.send(key, dest=p, tag=Tags.READ)
            tmp = (self.comm.recv(source=p, tag=Tags.READ))
            res.extend(tmp[0])
        return res



    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """

        for s in self.slaves:
            self.comm.send(obj=None, dest=s, tag=Tags.EXIT)
        for s in self.slaves:
            self.comm.recv(source=s, tag=Tags.EXIT)

def main():

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('I am  %s rank %d (total %d)' % (name, rank, size) )

    if rank == 0: # Master

        app = Master(slaves=range(1, size))
        v = app.allocate([i for i in range(1, 10)])
        print('read', app.read(v))
        app.terminate_slaves()
    else: # Any slave

        Slave().run()

    print('Task completed (rank %d)' % (rank) )

if __name__ == "__main__":
    main()