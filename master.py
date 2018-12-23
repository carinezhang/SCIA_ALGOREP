from mpi4py import MPI
import time
import sys
import numpy as np
from tags import Tags
from slave import Slave

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
        """
        Allocate the variable 'obj' and return an id associate with the variable. 
        Can handle 'int' and 'list' of 'int' types.
        """
        lens = sorted(self.get_size(), key=lambda x: x[1])
        if lens[0][1] >= MAX_SIZE:
            raise Exception('not enough space')
        size = lens[0][1]
        #if we have enough space to stock everything at once
        if MAX_SIZE - size >= len(obj):
            if isinstance(obj, int):
                send_size = 1
            else:
                send_size = len(obj)
            p = lens[0][0]
            size = lens[0][1]
            self.comm.send((obj, time.time()), dest=p, tag=Tags.ALLOC)
            var = self.comm.recv(source=p, tag=Tags.ALLOC)
            return (type(obj), ['{}-{}-{}'.format(p,send_size, var)])
        
        total_lens = sum(MAX_SIZE - n for _, n in lens)
        if total_lens < len(obj):
            raise Exception('not enough space')
        #when the list can't fit in one process
        list_var = []
        curr = 0
        for p, length in lens:
            disponible_size = MAX_SIZE - length
            up = curr + disponible_size
            if up > len(obj):
                up = len(obj)
            send_size = up-curr
            self.comm.send((obj[curr:up], time.time()), dest=p, tag=Tags.ALLOC)
            list_var.append('{}-{}-{}'.format(p, send_size, self.comm.recv(source=p, tag=Tags.ALLOC)))
            curr += disponible_size
            if curr > len(obj):
                break
        return (list, list_var)

    def read(self, var):
        """
        Return the value associated with the var.
        """
        var_list = var[1]
        if len(var[1]) <= 1:
            v = var_list[0].split('-')
            p = int(v[0])
            key = v[2]
            self.comm.send(key, dest=p, tag=Tags.READ)
            return self.comm.recv(source=p, tag=Tags.READ)
        res = []
        for v in var_list:
            p = int(v.split('-')[0])
            key = v.split('-')[2]
            self.comm.send(key, dest=p, tag=Tags.READ)
            tmp = (self.comm.recv(source=p, tag=Tags.READ))
            res.extend(tmp)
        return res

    def modify(self, var_name, new_val, index):
        """
        Replace a variable by a new one.
        Return True if the variable is modified, False otherwise.
        """
        if var_name[0] == int:
            p = int(var_name[1][0].split('-')[0])
            key = var_name[1][0].split('-')[2]
            self.comm.send((key, new_val, 0, time.time()), dest=p, tag=Tags.MODIFY)
            return self.comm.recv(source=p, tag=Tags.MODIFY)
        pos = 0

        for v in var_name[1]:
            tmp = v.split('-')
            p = int(tmp[0])
            size = int(tmp[1])
            key = tmp[2]
            if pos + size > index:
                self.comm.send((key, new_val, index-pos, time.time()), dest=p, tag=Tags.MODIFY)
                return self.comm.recv(source=p, tag=Tags.MODIFY)
            pos += size
        return False


    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """
        for s in self.slaves:
            self.comm.send(obj=None, dest=s, tag=Tags.EXIT)
        for s in self.slaves:
            self.comm.recv(source=s, tag=Tags.EXIT)

def init():

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    if rank == 0: # Master
        return Master(slaves=range(1, size))
     # Any slave
    Slave().run()

def main():
    app = init()
    if (MPI.COMM_WORLD.Get_rank() == 0):
        v = app.allocate([i for i in range(1, 10)])
        print('read', app.read(v))
        print('modify', app.modify(v, 56, 7))
        print('read', app.read(v))
        app.terminate_slaves()

if __name__ == "__main__":
    main()