#!/usr/bin/env python2.7
# Simply run this python script
# Do python -i run.py to run interactively

from MakeConfigFiles import *

set_env()

# Can also set up parser
nevents = 5000
pt_string_list = set_pt()

#makeStep1ConfigFiles (pt_string_list, nevents)
#makeStep2ConfigFiles (pt_string_list, nevents)
#makeStep3ConfigFiles (pt_string_list, nevents)
#makeStep4ConfigFiles (pt_string_list, nevents)

# runSteps(): run these files in bash