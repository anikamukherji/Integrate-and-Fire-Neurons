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
import settings_test_stp as sim_settings


######################################
# USER-DEFINE: ENTER A  DESCRIPTION  #
######################################
description = """ converting the stp_test settings dict back to it's original
form. Now there are three different types of STP onto the HVA neurons.

This model lacks the double Ge decay (from the original model).
"""

########################################
# USER-DEFINE: PATH TO DATA DIRECTORY  #
########################################
dat_path = "/Users/charliehass/Dropbox/Duke on Dropbox/hva_sim_data"

###################################
# DON'T MESS WITH THE STUFF BELOW #
###################################
run_simulations(sim_settings.settings, description, dat_path)
