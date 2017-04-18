"""
Wrapper function for easy simulation setup.

1) Define the settings module
2) Enter a description
3) Specify the path to the directory where the data should be saved
4) Call "python3 run_simulation.py" from terminal

"""

###################################
# IMPORT THE NECESSARY MODULES    #
###################################
from hvasim import run_simulations

#######################################
# USER-DEFINE: THE SIMULATION SETTINGS
# import YYYYYY as sim_settings (YYYYY = sim_settings module name)
import settings_default as sim_settings

# define other things here
sim_length = 0.5  # seconds
use_poisson = False

######################################
# USER-DEFINE: ENTER A  DESCRIPTION  #
######################################
description = """ Using the default settings file to explore the
dependence of STP on modulation rate for different types of afferent synapses
(PY->PY, PY->FS, PY->SOM).

The interneurons in the HVA do not contact the PY cells (p_connect=0)
"""

"""  END USER DEFINED STUFF  """



########################################
# USER-DEFINE: PATH TO DATA DIRECTORY  #
########################################
dat_path = "~/Desktop/Integrate-and-Fire-Neurons/networks"

###################################
# DON'T MESS WITH THE STUFF BELOW #
###################################
run_simulations(sim_settings.settings, description, dat_path)
