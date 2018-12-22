from mpi4py import MPI
import sys
import numpy as np
from enum import IntEnum
MAX_SIZE = 4096
center = 0

Tags = IntEnum('Tags', 'GET_SIZE ALLOC READ READY START DONE EXIT')

class Slave:
    """
    A slave process extend this class, create an instance and invoke the run
    process
    """
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = 0
        self.mem = []


    def run(self):
        """
        Invoke this method when ready to put this slave to work
        """
        status = MPI.Status()
        
        while True:
            self.comm.send(None, dest=0, tag=Tags.READY)
            data = self.comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
    
            if tag == Tags.GET_SIZE:
                self.comm.send(self.size, dest=0, tag=Tags.GET_SIZE)
            if tag == Tags.ALLOC:
                self.mem.append(data)
                self.comm.send(self.size, dest=0, tag=Tags.ALLOC)
                self.size += 1
            if tag == Tags.READ:
                self.comm.send(self.mem[data], dest=0, tag=Tags.READ)

            elif tag == Tags.EXIT:
                break
        
        self.comm.send(None, dest=0, tag=Tags.EXIT)
        
