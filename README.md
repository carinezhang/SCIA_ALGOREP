# ALGOREP Project

The goal of this project is to implement a distributed memory with the MPI lib.


## Prerequisites

For this project, you need to have:
- Python3
- mpi4py (Python lib for MPI)


## API
To use the API, you need to import the lib:
```
from master import init
```

### Initialization
```
app = init()
```
### Allocation
```
v = app.allocate(1)
```
### Reading
```
app.read(v)
```
### Modifying
```
app.modify(v, 2)
```
### Free
```
app.free(v)
```

### End the program
To end the program, you must use this line:
```
app.terminate_slaves()
```
## Running the tests

To run the tests, you need to type:

```
make tests
```


## Authors

* **Guillaume DRAPALA-BIZOUARN** - *drapal_g* 
* **Ugo DUCHEMANN** - *ugo.duchemann* 
* **Carine ZHANG** - *zhang_d* 

