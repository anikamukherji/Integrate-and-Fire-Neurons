
from create_network import *
# import matplotlib.pyplot as plt
from chance_abbott_sim_settings import *
from loop_settings import *
from functools import reduce  
import operator
import dpath.util


def find_list(d):
    """
    Returns '/' separated path to location of list in loop_settings
    """


def find_list_recursive(d, path):
    for k,v in d.items():
        if isinstance(v,list):
            return v, path 
            print(v)
        if isinstance(v,dict):
            path += k
            path += "/"
            find_list(d[k], path) 

def find_list_it(d):
    """
    Max depth of 4
    """
    for k0, v in d.items():
        if type(v) == list:
            return d[k], v
        if type(v) == str or type(v) == int or type(v) == float:
           continue 
        for k1, v in d[k0].items():
            if type(v) == list:
                return "{}/{}".format(k0,k1), v
            if type(v) == str or type(v) == int or type(v) == float:
                continue 
            for k2, v in d[k0][k1].items():
                if type(v) == list:
                    return "{}/{}/{}".format(k0,k1,k2), v
                if type(v) == str or type(v) == int or type(v) == float:
                    continue 
                for k3, v in d[k0][k1][k2].items():
                    if type(v) == list:
                        return "{}/{}/{}/{}".format(k0,k1,k2,k3), v
                    if type(v) == str or type(v) == int or type(v) == float:
                        continue 



def run_loops(settings_dict, poisson=True):

    (path, values) = find_list_it(settings_dict)
    values_list = values

    for i in range(len(values_list)):
        mod_settings = settings
        dpath.util.set(mod_settings, path, str(values_list[i]))
        if poisson:
            net = create_network(mod_settings)
        if not poisson:
            net = create_network(mod_settings, poisson=False)
        net.run(3*second)
        mon = net['HVA_PY_V_mon']
        plt.plot(mon.t/ms, mon.V[0], 
                label="mod ={} Hz".format(values_list[i]))

    plt.legend()
    plt.show()


# print(find_list_it(loop_settings))
run_loops(loop_settings, poisson=False)


