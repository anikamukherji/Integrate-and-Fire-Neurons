"""
Make temporary settings dicts.

This module should handle the creation of temporary "settings" dictionaries for
a simulation run.

The logic is that:
1) "settings_default" file contains all the current simulation parameters.
2) "settings_sim_..." files contain the settings for a specific simulation (eg.
    medial areas, lateral area, fast/slow stp etc...)
3) "run_settings" is a dictionary created at runtime based off the values in the
    default_ and settings_sim_ settings files.

Generating the run_settings (run-time) dictionary follows the following
process:
1) Make a copy of the "settings_default" dictionary
2) Load in the desired settings_sim_  dictionary (e.g., "settings_sim_hva_medial.py")
3) Iterate through the default_  dictionary.
    * throw an error if that value is not defined in the settings_sim_ dict. This ensures
      that all default params are defined correctly
    * Any param in settings_sim_ that "is None" gets defined instead by default_ dict
    * Any param in settings_sim_ that "is not None" gets defined by settings_sim_
    * Any param in settings_sim_ that is a list gets flaged
    * return the run_settings dictionary, and the address of the
      list (for looping)
"""


def create_run_settings(default_dict, settings_sim):

    # override default values with non-None vals in settings_sim
    run_settings = enforce_sim_params(default_dict, settings_sim)

    # find any param values that are type=list, return the dpath
    list_dpaths = find_param_lists(run_settings)

    # error check the list_dpaths

    # return the run_settings dictionary
    return list_dpaths, run_settings


def enforce_sim_params(d1, d2):
    pass


def find_param_lists(runtime_dict, dpath_lists=None, addr=None) -> str:

    # define a dpath_list for return arg and for recursion
    if dpath_lists is None:
        dpath_lists = []

    # initialize an "address" list for glob addresses for dpath_list
    if addr is None:
        addr = []

    for key in runtime_dict.keys():
        # add to the address when you dive into a key
        addr.append(key)

        if type(runtime_dict[key]) is dict:
            dpath_lists = find_param_lists(runtime_dict[key],
                                           dpath_lists,
                                           addr.copy()
                                           )
        elif type(runtime_dict[key]) is list:
            dpath_lists.append("/" + "/".join(addr))
            # FIXME: add error checking for len(list)=1

        # remove the key so that the address is correct for the next key
        addr.pop()

    # FIXME: add error checking for len(dpaht_lists)>1
    # FIXME: return only the first element of the list (a string)
    return dpath_lists


# test directory for find_param_list
d = {
    'one': [1, 2, 3, 4],
    'two': {'a': [1, 2, 3],
            'b': 'one',
            'c': {'foo': "string",
                  'bar': ["baz", "buzz"],
                  'bust': {'x': {'y': {'z': [1, 2]},
                                 'toro': "zeuse",
                                 'junk': ["gg", "hh", "jj"]
                                 }
                           }
                  }
            },
    'three': (1, 2, 3),
    'four': {'eggs': [1, 2, 3],
             'spam': "green",
             'sam': {"dr.": [1, 2, 3],
                     "strange": 'love'
                     }
             }
}
