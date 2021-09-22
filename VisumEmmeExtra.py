##############################################################
##  This scripts automates the extra steps to fully convert the network
##  1 - It removes the A mode and from the original network 
##  2 - It exports the base network, shape and special fields 
##  3 - It creates a new scenario with the proper modes, transit vehicles specification, 
##      extra attribute fields and link shape. 
##
##  Daniel Jimenez, Metro, 8, 11, 2015 
##
##############################################################


import inro.emme.desktop.app as _app
import inro.modeller as _m
import os
from Emmy_Functions import Emmy_Functions

e = Emmy_Functions()
#Change working directory to location of emme bank
os.chdir(e.bank_location_path)
#Get input scenario number
network = e.get_network("Select newly converted V2E scenario:")


#Start an instance of modeller
project_path = os.path.join(os.getcwd(), "New_Project/New_Project.emp")
my_desktop = _app.start_dedicated(project = project_path, visible = False, user_initials = "user")
data = my_desktop.data_explorer()
my_modeller = _m.Modeller(my_desktop)
scenario = e.scen_id  #int that holds the scenario number of the original scenario

#Export only turns before removing A mode.
#If the A mode is removed, all the turn penalites are lost as well
export_turns = my_modeller.tool("inro.emme.data.network.turn.export_turns")
export_turns(export_file = "turns_{}.txt".format(scenario), selection = "all", scenario = e.bank.scenario(e.scen_id))

#Remove A mode from all links
links = network.links()
for link in links:    
    modes = e.get_All_Modes(link) 
    if "A" in modes:
        link.modes -= set([network.mode('A')])
e.commit_network(network)

#Export BaseNetwork, Baseshape and extra attributes
export_base_net = my_modeller.tool("inro.emme.data.network.base.export_base_network")
export_base_net(export_file = "base_network_{}.txt".format(scenario), selection = {'node':"all", "link":"all"})
export_link_shape = my_modeller.tool("inro.emme.data.network.base.export_link_shape")
export_link_shape(export_file = "link_shape_{}.txt".format(scenario), selection = "all")
export_extra_attributes = my_modeller.tool("inro.emme.data.extra_attribute.export_extra_attributes")
export_extra_attributes(extra_attributes = ["@amrmp","@cap","@centerturn","@fwcap","@mdrmp","@pmrmp","@speed","@tkpth","@tknet"], scenario = e.bank.scenario(e.scen_id))


#Create new scenario and set it as the primary
while 1:
    try: 
        scenario_num = int(raw_input("Enter id of new scenario: "))
    except ValueError: 
        print "Please enter an integer"
    else:
        break    
scenario_name = raw_input("Enter name of new scenario: ")   
create_scenario = my_modeller.tool("inro.emme.data.scenario.create_scenario")
create_scenario(scenario_id = scenario_num, scenario_title = scenario_name, set_as_primary = True, overwrite = True)

# batch in modes, turns, and transit vehicles    
mode_transaction =  my_modeller.tool("inro.emme.data.network.mode.mode_transaction")
mode_transaction(transaction_file = "V:/allStreetsNetwork/EMMEfiles/modes_new.bout")
vehicle_transaction = my_modeller.tool("inro.emme.data.network.transit.vehicle_transaction")
vehicle_transaction(transaction_file = "V:/allStreetsNetwork/EMMEfiles/trveh")

#import network and shape files
import_network = my_modeller.tool("inro.emme.data.network.base.base_network_transaction")
import_network(transaction_file = "base_network_{}.txt".format(scenario))
import_shape = my_modeller.tool("inro.emme.data.network.base.link_shape_transaction")
import_shape(transaction_file = "link_shape_{}.txt".format(scenario))
#Import Turns
turn_transaction = my_modeller.tool("inro.emme.data.network.turn.turn_transaction")
turn_transaction(transaction_file = "turns_{}.txt".format(scenario), revert_on_error = False)

#add fields
#To add future fields, add the name to the fields tuple and to the export_extra_attributes function list
add_attribute = my_modeller.tool("inro.emme.data.extra_attribute.create_extra_attribute")
fields = ("tkpth","speed","fwcap","cap","mdrmp","pmrmp","amrmp","mb","trkad","htkad","mtkad","htvol","mtvol","svol","hvol","centerturn","tknet")
for i in fields:
    add_attribute(extra_attribute_default_value = 0, extra_attribute_name = i, extra_attribute_type = "LINK")
import_attribute = my_modeller.tool("inro.emme.data.network.import_attribute_values")
import_attribute(file_path = "extra_links_{}.txt".format(scenario))

#Delete incorrect scenario
delete_scen = my_modeller.tool("inro.emme.data.scenario.delete_scenario")
delete_scen(scenario = e.bank.scenario(e.scen_id))