from mpi4py import MPI
import sys
import numpy as np
from tags import Tags
MAX_SIZE = 6
center = 0


class Slave:
    """
    A slave process extend this class, create an instance and invoke the run
    process
    """
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = 0
        self.mem = dict()
        self.history = dict()

    def allocate(self, var, timestamp):
        """
        Allocate a variable and return an id associate with the variable. 
        Increase the size taken.
        """
        name = str(self.rank) + "/" + str(len(self.mem.items()))
        self.mem[name] = var
        # Check if the var is int or list to increase the size
        if isinstance(var, int):
            self.size += 1
        else:
            self.size += len(var)
        self.history[name] = [timestamp]
        return name

    def modify(self, var_name, new_var, index, timestamp):
        """
        Replace a variable by a new one.
        Return True if the variable is modified, False otherwise.
        """
        if var_name not in self.mem:
            return False
        if var_name not in self.history or self.history[var_name][-1] > timestamp:
            return False
        var = self.mem[var_name]
        if isinstance(var, int):
            self.mem[var_name] = new_var
            self.history[var_name].append(timestamp)
        elif isinstance(var, list):
            if index is None or index >= len(var):
                return False
            self.mem[var_name][index] = new_var
            self.history[var_name].append(timestamp)
        else:
            return False
        return True

    def get_size(self):
        return self.size

    def read(self, var_name):
        """
        Return the variable associated with the var_name.
        Return None if 0 variable are found.
        """
        if var_name not in self.mem:
            return None
        return self.mem[var_name]

    def free(self, var_name, timestamp):
        """
        Remove a variable from the current variable space.
        Return True if variable has been erased, False otherwise.
        """
        var = self.mem.pop(var_name, None)
        if not var:
            return False
        if var_name in self.history or self.history[var_name][-1] > timestamp:
            return False
        self.history[var_name].append(timestamp)
        if isinstance(var, int):
            self.size -= 1
        else:
            self.size -= len(var)
        return True
        

    def run(self):
        """
        Invoke this method when ready to put this slave to work
        """
        status = MPI.Status()

        while True:
            data = self.comm.recv(source=center, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
    
            if tag == Tags.GET_SIZE:
                self.comm.send(self.size, dest=center, tag=Tags.GET_SIZE)
            if tag == Tags.ALLOC:
                # !!!!!!!!!!!!!!!!!!
                # TEMPORARY SOLUTION
                # Change 0 to the timestamp !
                # !!!!!!!!!!!!!!!!!!
                name = self.allocate(data[0], data[2])
                self.comm.send(name, dest=center, tag=Tags.ALLOC)
                self.size += data[1]
            if tag == Tags.READ:
                var = self.read(data)
                self.comm.send(var, dest=center, tag=Tags.READ)
            if tag == Tags.MODIFY:
                var = self.modify(data[0], data[1], data[2], data[3])
                self.comm.send(var, dest=center, tag=Tags.MODIFY)
            elif tag == Tags.EXIT:
                break
        
        self.comm.send(None, dest=center, tag=Tags.EXIT)
        
