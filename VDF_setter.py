##############################################################
## 
## Script that sets VDF to an Emme Network
## To use - copy script to working space and run
## A new_project.emp must exist in order to execute 
## If errors contact Daniel
##
##  Daniel Jimenez, Metro, May 21, 2015 
##
##############################################################

import os 
import sys
from Emmy_Functions import Emmy_Functions 

def vdf_setter(link, net):    
    modes = e.get_All_Modes(link) #Gets all the modes for the specific link. Check class for definition.
    if "h" in modes and "s" not in modes and link.length < 0.05: #Check for hov lanes transfers. 
        return 13
    elif link["@cap"] == 9999 and link["@speed"] == 10: #Check for dt vdfs
        return 9    
    elif link.type in [10,19] and link.volume_delay_func != 13: #Highway links excluding hov transfer lanes  
        return 1
    elif link.type not in [10,19] and link["@fwcap"] > 0:
        print "Check {}. Possible fwcap error ".format(link.id)
        return 99
    elif any([link["@amrmp"],link["@mdrmp"],link["@pmrmp"]]) > 0: #Looks for any ramp cap 
        return 10
    elif link.volume_delay_func == 14: #Set connectors to default 14 from Visum. To set connector value edit specification_for_VISUM_2_Emme_ file in the Emmefiles folder.   
        return 14    
    elif link.type == 1: #Transit only
        return 6  
    elif "w" in modes and not any(mode in modes for mode in ["l","e","r","b","a","c","h","s"]):
        return 0           
    elif link["@cap"] > 99:  ##Previously Known as @apcap
        # Block that determines number of intersections for links
        #It uses count to update the number of intersections.
        count = 0
        j_node = link.j_node #Gets end node of current link
        for j in net.links(): #Iterate through a new passed network copy 
            if j.i_node == j_node and j.volume_delay_func != 14: #Analyse end node to count number of outgoing links excluding connectors                       
                if link.reverse_link == None:
                    count += 1
                else:
                    if j.id != link.reverse_link.id: #Exclude end node opposite direction to only count out going links
                        count += 1
        #Depending on 'count' set the vdf to appropriate value. Count comes from the passed list iteration 
        if count <= 1:
            return 4
        elif count > 1:
            return 2  
    else:
        return 99    

#function to set ul3 depedning of links cap and fwcap value
def cap2ul3(link):
    if link['@fwcap'] > 0:
        return link['@fwcap']
    else:
        return link['@cap'] 

        
def main():   
    network = e.get_network("Select scenario for final conversion:")    
    links = network.links()
    for link in links:        
        vdf = vdf_setter(link, network)
        link.volume_delay_func = vdf        
        if link.volume_delay_func == 14:
            link['@speed'] = 12
            link['@cap'] = 9999
        link.data3 = cap2ul3(link)
        link.num_lanes = link.num_lanes + 0.5 * link['@centerturn']
    e.commit_network(network)
    print "\n\nRunning mb_lookup.mac"
    e.run_macro("mb_lookup")
   
if __name__ == "__main__":
    e = Emmy_Functions()
    os.chdir(e.bank_location_path)
    main()
    print "\nDONE"
           