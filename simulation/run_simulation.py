"""
Wrapper function for easy simulation setup.

1) define the variables listed below
2) call "python3 run_simulation.py" from terminal

"""
# TODO: remove the data directory from the git repository?

"""  USER DEFINED STUFF  """

# define sim_settings
# import YYYYYY as sim_settings (YYYYY = sim_settings module name)
import settings_test_stp as sim_settings

# define other things here
sim_length = 0.5  # seconds
use_poisson = False
description = "testing the new simulation codebase"

"""  END USER DEFINED STUFF  """





""" don't mess with the stuff below """
from create_network import run_loops

run_loops(sim_settings.settings,
          sim_length,
          description,
          poisson_on=use_poisson)
