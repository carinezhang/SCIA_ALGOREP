from enum import IntEnum

class Tags(IntEnum):
    GET_SIZE = 1
    ALLOC = 2
    READ = 3
    MODIFY = 4
    EXIT = 5
    FREE = 6