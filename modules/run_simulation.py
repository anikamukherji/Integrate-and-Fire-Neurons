
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



def run_loops(settings_dict, sim_length, poisson=True):

    (path, values) = find_list_it(settings_dict)
    values_list = values

    f, axs = plt.subplots(len(values_list), 3)
    axs[0,0].set_title("HVA_PY response")
    axs[0,1].set_title("FS response")
    axs[0,2].set_title("SOM response")
    for i in range(len(values_list)):
        mod_settings = settings
        dpath.util.set(mod_settings, path, str(values_list[i]))
        if poisson:
            net = create_network(mod_settings, sim_length)
        if not poisson:
            net = create_network(mod_settings, sim_length, poisson=False)
        net.run(sim_length*second)
        hva_mon = net['HVA_PY_V_mon']
        fs_mon = net['FS_V_mon']
        som_mon = net['SOM_V_mon']
        axs[i,0].plot(hva_mon.t/ms, hva_mon.V[0])
        axs[i,1].plot(fs_mon.t/ms, fs_mon.V[0])
        axs[i,2].plot(som_mon.t/ms, som_mon.V[0])

    plt.show()
    spike_mon = net['afferent_spike_mon']
    plt.plot(spike_mon.t/ms)


run_loops(loop_settings, 2, poisson=False)


