#!!!!!not done, need to take care of the emlocki file to rename the orignial back to emilocli at line 42, trying to close objects to accomplish this
import inro.emme.desktop.app as _app
import inro.modeller as _m
import inro.emme.database.emmebank as _bank
import os
import sys
import time

os.rename("emlocki","emlocki_temp")
#Bank and path settings
working_dir = os.getcwd()
emmebank_path = os.path.join(os.getcwd(),"emmebank")
emmebank = _bank.Emmebank(emmebank_path)

#Passed arguments from macro
from_scen = sys.argv[1]
new_scen = sys.argv[2]
title = sys.argv[3]
path = sys.argv[4]
if path > 0:
    path_ = True
else:
    path_ = False  

#need to check if project exists here
try:
    project = _app.create_project(working_dir,"New_Project")#change to relative path
except WindowsError:
    project = os.path.join(working_dir, "New_Project/New_Project.emp")
    
#Create tool and get inputs    
my_desktop = _app.start_dedicated(project = project, visible = False, user_initials = "user")
scenario = emmebank.scenario(from_scen) 
my_modeller = _m.Modeller(my_desktop)

# copy scenario tool
# scencopy = my_modeller.tool("inro.emme.data.scenario.copy_scenario")
# scencopy(from_scenario = scenario, scenario_id = new_scen, scenario_title = title, set_as_primary = True, copy_linkshapes = True, copy_paths = path_ )


print "close"
time.sleep(5)
os.rename("emlocki_temp","emlocki")  

