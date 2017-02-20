# TODO: convert the "import *" notation to named imports when possible
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
    # TODO: this function allows for only one list, and should thow an error if it encounters another one?
    for k0, v in d.items():
        if type(v) == list:
            return d[k], v
            # TODO: I think the pythonic way of writing this is: type(v) is str or type(v) is int or ... (i.e., don't use the ==)
        if type(v) == str or type(v) == int or type(v) == float:
            continue
        for k1, v in d[k0].items(): # TODO: this will bonk if d[k0] is not a dict (for example, type = complex).
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
                        # TODO: include an if type(v) is dict -> throw error b/c your code only works for depth = 4 and should error otherwise



def run_loops(settings_dict, sim_length, poisson=True):

    (path, values) = find_list_it(settings_dict)
    values_list = values # TODO: delete re-definition of "values"?

    f, axs = plt.subplots(len(values_list), 3)
    axs[0,0].set_title("HVA_PY response")
    axs[0,1].set_title("FS response")
    axs[0,2].set_title("SOM response")
    for i in range(len(values_list)):
        """
        FIXME: If you were hoping that this re-initializes the settings dict on
        each loop, it may not be the case b/c Python binds mod_settings to
        settings. Changes to mod_settings by default changes settings too?
        """
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

"""
TODO: save (pickle) each simulation along with it's settings dictionary.
This will help identify any errors in assigning the simulation's state and
ensure that we always can back track to the ground truth.

Do the plotting later (un-pickle).
"""
