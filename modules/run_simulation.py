
from brian2 import *
from create_network import create_network
import matplotlib.pyplot as plt
from chance_abbott_sim_settings import settings
from loop_settings import loop_settings
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



def run_loops(settings_dict, sim_length, poisson=True):

    (path, values) = find_list_it(settings_dict)

    f, axs = plt.subplots(len(values), 3)
    axs[0,0].set_title("G_tau = 1 ms,  D_tau = 10 ms, d = 0.8")
    axs[0,1].set_title("G_tau = 1 ms,  D_tau = 25 ms, d = 0.8")
    axs[0,2].set_title("G_tau = 1 ms, D_tau = 75 ms, d = 0.8")
    for i in range(len(values)):
        mod_settings = settings.copy()
        dpath.util.set(mod_settings, path, values[i])
        poisson_on = poisson
        net = create_network(mod_settings, sim_length, poisson=poisson_on)
        net.run(sim_length*second)
        hva_v_mon = net['HVA_PY_V_mon']
        fs_v_mon = net['FS_V_mon']
        som_v_mon = net['SOM_V_mon']
        hva_ge_mon = net['HVA_PY_Ge_total_mon']
        fs_ge_mon = net['FS_Ge_total_mon']
        som_ge_mon = net['SOM_Ge_total_mon']
        print("{} Hz:".format(values[i]))
        print(som_ge_mon.Ge_total[0])
        hva_gi_mon = net['HVA_PY_Gi_total_mon']
        fs_gi_mon = net['FS_Gi_total_mon']
        som_gi_mon = net['SOM_Gi_total_mon']
        # axs[i,0].plot(hva_v_mon.t/ms, hva_v_mon.V[0], 'black')
        # print(hva_v_mon.V[0][5])
        axs[i,0].plot(hva_ge_mon.t/ms, hva_ge_mon.Ge_total[0], 'red')
        # axs[i,0].plot(hva_gi_mon.t/ms, hva_gi_mon.Gi_total[0], 'blue')
        # axs[i,1].plot(fs_v_mon.t/ms, fs_v_mon.V[0], 'black')
        axs[i,1].plot(fs_ge_mon.t/ms, fs_ge_mon.Ge_total[0], 'red')
        # axs[i,1].plot(fs_gi_mon.t/ms, fs_gi_mon.Gi_total[0], 'blue')
        # axs[i,2].plot(som_v_mon.t/ms, som_v_mon.V[0], 'black')
        axs[i,2].plot(som_ge_mon.t/ms, som_ge_mon.Ge_total[0], 'red')
        # axs[i,2].plot(som_gi_mon.t/ms, som_gi_mon.Gi_total[0], 'blue')

    plt.show()
    # spike_mon = net['afferent_spike_mon']
    # plt.vlines(spike_mon.t/ms, ymin=-0.040, ymax=0, 'gray', lw=3)
    # plt.show()


run_loops(loop_settings, 2, poisson=False)


