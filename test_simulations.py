from simulations import *
from PY_FS_SOM_neurons_init import *  # TODO is this redundant with import statement inside simulations.py?

test_dict = sim_caller(3, 0.5*second)
print(test_dict)
