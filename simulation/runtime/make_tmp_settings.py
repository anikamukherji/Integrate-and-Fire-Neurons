"""
Make temporary settings dicts.

This module should handle the creation of temporary "settings" dictionaries for
a simulation run.

The logic is that:
1) "default_settings" file contains all the current simulation parameters.
2) "sim_..." files contain the settings for a specific simulation (eg.
    medial areas, lateral area, fast/slow stp etc...)
3) "run_settings" is a dictionary created at runtime based off the values in the
    default_ and sim_ settings files.

Generating the run_settings (run-time) dictionary follows the following
process:
1) Make a copy of the "default_settings" dictionary
2) Load in the desired sim_  dictionary (e.g., "sim_hva_medial.py")
3) Iterate through the default_  dictionary.
    * throw an error if that value is not defined in the sim_ dict. This ensures
      that all default params are define correctly
    * Any param in sim_ that "is None" gets defined instead by default_ dict
    * Any param in sim_ that "is not None" gets defined by sim_
    * Keep param in sim_ that is a list gets flaged
    * return the run_settings dictionary, and the address of the
      list (for looping)
"""

import settings.default_settings as default_dict
import settings.test_stp_g as sim_dict


print(default_dict)
print(sim_dict)
