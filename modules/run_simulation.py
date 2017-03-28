
from brian2 import *
from create_network import create_network
from chance_abbott_sim_settings import settings
from loop_settings import loop_settings
import operator
import dpath.util
import dill as pickle
import weakref
import time

########################
## IMPORTANT############
### Increment RUN_NUM ##
### everytime you run ##
### A simulation #######
RUN_NUM = 0

def run_net_and_save(net, sim_length, description):
    global RUN_NUM
    net.run(sim_length)
    pickle.dump(net.get_states(), open("./networks/run_{}_".format(RUN_NUM) + time.strftime("%d/%m/%Y") + ".p", "wb"))
    with open("../networks/net_descriptions.txt", "w") as f:
        f.write("\n")
        f.write("Run #{}: ".format(RUN_NUM) + time.strftime("%d/%m/%Y"))
        f.write(description)
    RUN_NUM += 1
    print("Assign RUN_NUM to {} if you plan on running simulations later today".format(RUN_NUM))


def find_list_it(d):
    """
    Max depth of 4
    """
    for k0, v in d.items():
        if type(v) == list:
            return d[k], v
        if type(v) != dict:
           continue 
        for k1, v in d[k0].items():
            if type(v) == list:
                return "{}/{}".format(k0,k1), v
            if type(v) != dict:
                continue 
            for k2, v in d[k0][k1].items():
                if type(v) == list:
                    return "{}/{}/{}".format(k0,k1,k2), v
                if type(v) != dict:
                    continue 
                for k3, v in d[k0][k1][k2].items():
                    if type(v) == list:
                        return "{}/{}/{}/{}".format(k0,k1,k2,k3), v
    raise ValueError("Passed in dictionary does not contain a list")



def run_loops(settings_dict, sim_length, description, poisson=True):
    """
    Run several simulations based on settings_dict passed containing a list
    of values as the key for the parameter you want to modify per simulation

    Each simulation will be pickled and saved to networks directory

    Pass in string description for distinguishing purpose of simulation
    """

    (path, values) = find_list_it(settings_dict)

    for i in range(len(values)):
        mod_settings = settings.copy()
        dpath.util.set(mod_settings, path, values[i])
        poisson_on = poisson
        net = create_network(mod_settings, sim_length, poisson=poisson_on)
        run_net_and_save(net, sim_length, description)



# run_loops(loop_settings, 1*second, "Test simulation 3.26.17", poisson=True)

