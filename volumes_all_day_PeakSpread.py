##############################################################
##
##  volume_all_day.py
##
##  --Creates a new scenario with aggreagated volumes from a peak spread bank 
##  --
##
##  Daniel Jimenez, Metro, Oct 6, 2015
##
##############################################################

import inro.emme.desktop.app as _app
import inro.modeller as _m
import os
from emmy_24 import Emmys
from Emmy_Functions import Emmy_Functions 

#get bank from the emmy functions methods
emmy = Emmy_Functions()
scen_id = 1

try:
    project = _app.create_project(emmy.bank_location_path,"New_Project")#change to relative path
except WindowsError:
    project = os.path.join(emmy.bank_location_path, "New_Project/New_Project.emp")
    
#Create tool and get inputs    
my_desktop = _app.start_dedicated(project = project, visible = False, user_initials = "user")
my_modeller = _m.Modeller(my_desktop)

create_scenario = my_modeller.tool("inro.emme.data.scenario.copy_scenario")
create_scenario(from_scenario = emmy.bank.scenario(2021), scenario_id = scen_id, scenario_title = "All day volumes",  overwrite = True)

links_dic = {}
#check emmy_24.py to see scenarios being returned. It only yields scenarios between 2000 and 3000
print "fetching"
for s in Emmys.fetch_scenario(emmy.bank): 
    for link in Emmys.fetch_links(emmy.bank, s):
        #check if link id key exist
        if links_dic.get(link.id): 
            links_dic[link.id]["volau"] += link.auto_volume
            links_dic[link.id]["htvol"] += link["@htvol"]
            links_dic[link.id]["mtvol"] += link["@mtvol"]
            links_dic[link.id]["svol"] += link["@svol"]
            links_dic[link.id]["hvol"] += link["@hvol"]
            links_dic[link.id]["vehvol"] += link["@vehvol"]
            
        #if key does not exist, iniziale values    
        else:
            links_dic[link.id] = {"volau":link.auto_volume,
                                  "htvol":link["@htvol"],
                                  "mtvol":link["@mtvol"],
                                  "svol":link["@svol"],
                                  "hvol":link["@hvol"],
                                  "vehvol":link["@vehvol"]}

network = emmy.bank.scenario(scen_id).get_network()
#Set object scenario id to scen_id to cbe able to commit the network. see method structrue.
emmy.scen_id = scen_id 
print "network"
for link in network.links():
    link.auto_volume = links_dic[link.id]["volau"] 
    link["@htvol"] = links_dic[link.id]["htvol"] 
    link["@mtvol"] = links_dic[link.id]["mtvol"] 
    link["@svol"] = links_dic[link.id]["svol"] 
    link["@hvol"] = links_dic[link.id]["hvol"]
    link["@vehvol"] = links_dic[link.id]["vehvol"]
emmy.commit_network(network)    

#Export shape links to be used in the new scenario.
print "Shape"
export_link_shape = my_modeller.tool("inro.emme.data.network.base.export_link_shape")
export_link_shape(export_file = "link_shape_{}.txt".format(2021), selection = "all")
import_shape = my_modeller.tool("inro.emme.data.network.base.link_shape_transaction")
import_shape(transaction_file = "link_shape_{}.txt".format(2021))