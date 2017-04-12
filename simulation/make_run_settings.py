"""
Make runtime settings dicts.

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

import copy


def create_run_settings(settings_default, settings_sim):

    # override default values with non-None vals in settings_sim
    run_settings = settings_default.copy()
    run_settings, _, _ = enforce_sim_params(settings_default,
                                            settings_sim,
                                            run_settings
                                            )

    # find any param values that are type=list, return the dpath
    list_dpaths = find_param_lists(run_settings)

    # return the run_settings dictionary
    return list_dpaths, run_settings


def enforce_sim_params(d_def, d_sim, d_run) -> dict:
    """Copies or over-rides default parameters."""

    # use the d_def dict as a template and crawl down it's tree
    for key in d_def.keys():
        assert key in d_sim.keys(), "ERROR: param in default but not simulation"
        if type(d_def[key]) is dict:
            d_def[key], d_sim[key], d_run[key] = enforce_sim_params(d_def[key],
                                                                    d_sim[key],
                                                                    d_run[key]
                                                                    )
        elif d_sim[key] is not None:
            d_run[key] = copy.copy(d_sim[key])  # REVIEW: is shallow copy necessary?
    return d_run, d_sim, d_def


def find_param_lists(runtime_dict, dpath_list=None, addr=None) -> str:

    # recursively walk the dictionary looking for lists
    dpath_list = find_param_lists_dict_walker(runtime_dict)

    # Current code only allows for one list of params. Enforce here
    assert len(dpath_list) <= 1, "ERROR: only allowed 1 list of params"

    # Return dpath as a string
    if len(dpath_list) == 0:
        dpath_list = str()  # empty string
    else:
        dpath_list = dpath_list[0]  # path as string

    return dpath_list


def find_param_lists_dict_walker(runtime_dict, dpath_list=None, addr=None):

        # define a dpath_list for return arg and for recursion
        if dpath_list is None:
            dpath_list = []

        # initialize an "address" list for glob addresses for dpath_list
        if addr is None:
            addr = []

        # print(runtime_dict)
        # print('/n')

        for key in runtime_dict.keys():
            addr.append(key)  # add to the address when you dive into a key
            val_type = type(runtime_dict[key])
            assert val_type is not tuple, "ERROR: tuple type not supported"

            if val_type is dict:
                dpath_list = find_param_lists_dict_walker(runtime_dict[key],
                                                          dpath_list,
                                                          addr.copy()
                                                          )
            elif val_type is list:
                dpath_list.append("/" + "/".join(addr))

            addr.pop()  # remove key so that addr is correct for the next key

        return dpath_list


# test directories for find_param_list. Some should fail the assert tests
d_listsss = {
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
    'three': [1, 2, 3],
    'four': {'eggs': [1, 2, 3],
             'spam': "green",
             'sam': {"dr.": [1, 2, 3],
                     "strange": 'love',
                     "movie": "hello"
                     }
             }
}

d_tuple = {
    'one': 1,
    'two': {'a': 2,
            'b': 'one',
            'c': {'foo': "string",
                  'bar': "buzz",
                  'bust': {'x': {'y': {'z': [1, 2, 3]},
                                 'toro': "zeuse",
                                 'junk': "gg"
                                 }
                           }
                  }
            },
    'three': (1, 2, 3),
    'four': {'eggs': 1,
             'spam': "green",
             'sam': {"dr.": 2,
                     "strange": 'love',
                     "movie": "hello"
                     }
             }
}

d_good = {
    'one': 1,
    'two': {'a': 2,
            'b': 'one',
            'c': {'foo': "string",
                  'bar': "buzz",
                  'bust': {'x': {'y': {'z': [1, 2, 3]},
                                 'toro': "zeuse",
                                 'junk': "gg"
                                 }
                           }
                  }
            },
    'three': 1,
    'four': {'eggs': 1,
             'spam': "green",
             'sam': {"dr.": 2,
                     "strange": 'love',
                     "movie": "hello"
                     }
             }
}

d_none = {
    'one': 1,
    'two': {'a': 2,
            'b': 'one',
            'c': {'foo': "string",
                  'bar': "buzz",
                  'bust': {'x': {'y': {'z': 1},
                                 'toro': "zeuse",
                                 'junk': "gg"
                                 }
                           }
                  }
            },
    'three': 1,
    'four': {'eggs': 1,
             'spam': "green",
             'sam': {"dr.": 2,
                     "strange": 'love',
                     "movie": "hello"
                     }
             }
}
