##############################################################
## 
## Script that creates a .net file from Emme's network 
## To use - copy script to working space and run 
## If errors contact Daniel
##
##  Daniel Jimenez, Metro, May 21, 2015 
##
##############################################################

import inro.emme.database.emmebank as _bank
import os 
import csv 
import time
import itertools
import sys


pythondir = 'L:/modrf/model/joan/programs_v2.5/src/py'
if pythondir not in sys.path:
    sys.path.append(pythondir)
from Emme2Visum import *
from Emmy_Functions import * 

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def create_201_interdelay_modes(network):
    modes = network.modes()
    m = {"AUTO":1, "TRANSIT":2, "AUX_AUTO":4, "AUX_TRANSIT":3}
    with open("interdelay_modes.csv", "wb")as f:
        w = csv.writer(f)
        w.writerow(["id","description","type","cost","cost_time_coeff","cost_dist_coeff","energy_dist_coeff","energy_time_coeff","aux_speed"])
        for mode in modes:
            operating, cost, ener, consum, speed = modes_types(mode)
            w.writerow([mode.id,mode.description,m[mode.type],1,operating,cost,ener,consum,speed])

def create_all_nodes(network):
    links = list(network.links())
    nodes = network.nodes()
    nodes_list, zone_list = [], []
    for node in nodes:
        centroid  = is_Centroid(node)
        if not centroid:
            #nodeType(links,node)
            #node structure = id, x, y            
            nodes_list.append([node.id,round(node.x, 6) * 5280, round(node.y, 6) * 5280]) 
        else:
            #zone structure = id, x, y
            zone_list.append([node.id, round(node.x, 6) * 5280, round(node.y, 6) * 5280])
    return nodes_list, zone_list

def create_links(network):
    links = list(network.links())
    links_in = set()
    links_list = []
    con_list = []
    toll = is_it("toll")
    over_dict = over_ride("1hr. override")
    no = 1
    for i, link in enumerate(links):
        if link.id not in links_in and is_Centroid(link.i_node) == False and is_Centroid(link.j_node) == False:                
            link_final = format_links(link, toll, over_dict)
            link_final.insert(0,no)
            links_list.append(link_final)
            r_link = link.reverse_link
            links_in.update([link.id])                        
            if r_link != None:                
                link_final = format_links(r_link, toll, over_dict)
                link_final.insert(0,no)
                links_list.append(link_final)                
                links_in.update([link.reverse_link.id])
            no += 1
        #Create connectors
        elif link.id not in links_in and is_Centroid(link.i_node) == True: 
            con_list.append(create_connectors(link))     
    return links_list, con_list 
    
def create_turns(network):
    turns = network.turns()
    turns_list = []
    over_dict = over_ride("turn cap override")
    #Turn list structure =  i_node, j_node, k_node, penalty_func where 0 = turn prohibited
    for turn in turns:
        if turn.penalty_func == 0 and not is_Centroid(turn.i_node):
            turns_list.append(create_turn(turn, over_dict))   
    return turns_list
    
def wrtie_net_file(nodes, zones, links, turns, connectors):
    with open("net_out.net", "w") as w:
        #Writing intro
        w.write("$VISION\n")
        w.write("* Portland Metro\n")
        w.write("* {time}\n".format(time = time.strftime("%m/%d/%Y")))
        w.write("*\n")
        w.write("* Table: Version block\n")
        w.write("*\n") 
        w.write("$VERSION:VERSNR;FILETYPE;LANGUAGE;UNIT\n")
        w.write("9;Net;ENG;MI\n\n*\n* Table: User-defined attributes\n*\n")
        #Writing Table: User-defined attributes
        w.write("$USERATTDEF:OBJID;ATTID;CODE;NAME;DATA_TYPE;DEFAULTVALUE;NUMDECPLACES\n")
        w.write("LINK;ACTUAL_RAMP_LENGTH;ACTUAL_RAMP_LENGTH;ACTUAL_RAMP_LENGTH;Double;0;2\n")
        w.write("LINK;AM_METER;AM_METER;AM_METER;Double;0;2\n")
        w.write("LINK;APP_CAP_1HR;APP_CAP_1HR;APP_CAP_1HR;Double;0;2\n")
        w.write("LINK;EMME_LANES;Emme_Lanes;Emme_Lanes;Double;0;6\n")
        w.write("LINK;FWY_CAP_1HR;FWY_CAP_1HR;FWY_CAP_1HR;Double;0;2\n")
        w.write("LINK;HOV_ONLY;HOV_ONLY;HOV_ONLY;Int;0;0\n")
        w.write("LINK;MB_CAP_1HR;MB_CAP_1HR;MB_CAP_1HR;Double;0;2\n")
        w.write("LINK;MB_CAP_1HR_OVERRIDE;MB_CAP_1HR_OVERRIDE;MB_CAP_1HR_OVERRIDE;Int;0;0\n")
        w.write("LINK;MD_METER;MD_METER;MD_METER;Double;0;2\n")
        w.write("LINK;OP_HOV_TOLL;OP_HOV_TOLL;OP_HOV_TOLL;Double;0;2\n")
        w.write("LINK;OP_HVY_TRUCK_TOLL;OP_HVY_TRUCK_TOLL;OP_HVY_TRUCK_TOLL;Double;0;2\n")
        w.write("LINK;OP_MED_TRUCK_TOLL;OP_MED_TRUCK_TOLL;OP_MED_TRUCK_TOLL;Double;0;2\n")
        w.write("LINK;OP_SOV_TOLL;OP_SOV_TOLL;OP_SOV_TOLL;Double;0;2\n")
        w.write("LINK;PK_HOV_TOLL;PK_HOV_TOLL;PK_HOV_TOLL;Double;0;2\n")
        w.write("LINK;PK_HVY_TRUCK_TOLL;PK_HVY_TRUCK_TOLL;PK_HVY_TRUCK_TOLL;Double;0;2\n")
        w.write("LINK;PK_MED_TRUCK_TOLL;PK_MED_TRUCK_TOLL;PK_MED_TRUCK_TOLL;Double;0;2\n")
        w.write("LINK;PK_SOV_TOLL;PK_SOV_TOLL;PK_SOV_TOLL;Double;0;2\n")
        w.write("LINK;PM_METER;PM_METER;PM_METER;Double;0;2\n")
        w.write("LINK;RAMP_TYPE_NO;RAMP_TYPE_NO;RAMP_TYPE_NO;Int;0;0\n")
        w.write("LINK;TOLL_CRC;TOLL_CRC;TOLL_CRC;Double;0;2\n")
        w.write("LINK;TRUCK_PATH;TRUCK_PATH;TRUCK_PATH;Double;0;2\n")
        w.write("TURN;TURN_CAP_1HR;TURN_CAP_1HR;TURN_CAP_1HR;Double;99999;2\n")
        w.write("TURN;TURN_CAP_1HR_OVERRIDE;TURN_CAP_1HR_OVERRIDE;TURN_CAP_1HR_OVERRIDE;Int;0;0\n\n")
        #Writing Table: Network
        w.write("*\n")
        w.write("* Table: Network\n")
        w.write("*\n") 
        w.write("$NETWORK:NETVERSIONID;SCALE;UNIT;LEFTHANDTRAFFIC;COORDDECPLACES;PROJECTIONDEFINITION\n")
        w.write('1.21;0.18939399729;MI;0;4;PROJCS["NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl",GEOGCS["GCS_North_American_1983_HARN",DATUM["D_North_American_1983_HARN",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",8202099.737532808],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-120.5],PARAMETER["Standard_Parallel_1",44.33333333333334],PARAMETER["Standard_Parallel_2",46.0],PARAMETER["Latitude_Of_Origin",43.66666666666666],UNIT["Foot",0.3048]]\n\n')
        #Writing Table: Transport systems
        #Warning!! For Table: Transport systems make sure to add extra modes when necessary
        w.write("*\n")
        w.write("* Table: Transport systems\n")
        w.write("*\n") 
        w.write("$TSYS:CODE;NAME;TYPE\n")
        w.write("a;a;PuT\n")
        w.write("b;b;PuT\n")
        w.write("c;c;PrT\n")
        w.write("e;e;PuT\n")
        w.write("h;h;PrT\n")
        w.write("ht;ht;PrT\n")
        w.write("l;l;PuT\n")
        w.write("mt;mt;PrT\n")
        w.write("p;p;PuTWalk\n")
        w.write("r;r;PuT\n")
        w.write("s;s;PrT\n")
        w.write("t;t;PrT\n")
        w.write("w;w;PuTWalk\n\n")
        #Writing Table: Table: Modes
        w.write("*\n") 
        w.write("* Table: Modes\n")
        w.write("*\n") 
        w.write("$MODE:CODE;NAME;TSYSSET\n")
        w.write("C;Car;c\n")
        w.write("H;HOV;h\n")
        w.write("HT;Heavy Trucks;ht\n")
        w.write("MT;Medium Trucks;mt\n")
        w.write("T;Transit;a,b,e,l,p,r,w\n")
        w.write("S;SOV;s\n")
        w.write("TRK;Truck;t\n\n")
        #Writing  Demand segments
        w.write("*\n") 
        w.write("* Table: Demand segments\n")
        w.write("*\n") 
        w.write("$DEMANDSEGMENT:CODE;NAME;MODE\n")
        w.write("C;Car;C\n")
        w.write("H;HOV;H\n")
        w.write("HT;Heavy Trucks;HT\n")
        w.write("MT;Medium Trucks;MT\n")
        w.write("Transit;Transit;T\n")
        w.write("S;SOV;S\n")
        w.write("TRK;Truck;TRK\n\n")
        ##Write nodes
        w.write("*\n") 
        w.write("* Table: Nodes\n")
        w.write("*\n")
        w.write("$NODE:NO;XCOORD;YCOORD\n") 
        for node in nodes:
            line = wrtie_format(node)
            w.write("{}\n".format(line))
        w.write("\n")
        #Writing Zones
        w.write("*\n") 
        w.write("* Table: Zones\n")
        w.write("*\n")
        w.write("$ZONE:NO;XCOORD;YCOORD\n")        
        for zone in zones:
             line = wrtie_format(zone)
             w.write("{}\n".format(line))
        w.write("\n") 
        #Writing Link types 
        w.write("*\n") 
        w.write("* Table: Link types\n")
        w.write("*\n")
        with open("L:/modrf/model/joan/visum/network_files/linkTypes.net", "r") as infile:
            file = itertools.islice(infile, 9, None) #iterator that skips first 9 lines of in file
            link_types = [line.strip() for line in file if line.startswith("*") == False]
            for link_type in link_types:
                w.write("{}\n".format(link_type))
        #Writing Link types
        w.write("\n")        
        w.write("*\n")
        w.write("* Table: Links\n")
        w.write("*\n")
        w.write("$LINK:NO;FROMNODENO;TONODENO;TYPENO;TSYSSET;LENGTH;NUMLANES;CAPPRT;V0PRT;ACTUAL_RAMP_LENGTH;AM_METER;APP_CAP_1HR;EMME_LANES;FWY_CAP_1HR;HOV_ONLY;MB_CAP_1HR;MB_CAP_1HR_OVERRIDE;MD_METER;OP_HOV_TOLL;OP_HVY_TRUCK_TOLL;OP_MED_TRUCK_TOLL;OP_SOV_TOLL;PK_HOV_TOLL;PK_HVY_TRUCK_TOLL;PK_MED_TRUCK_TOLL;PK_SOV_TOLL;PM_METER;RAMP_TYPE_NO;TOLL_CRC;TRUCK_PATH\n")
        for link in links:            
            line = wrtie_format(link)
            w.write("{}\n".format(line))
        w.write("\n")
        #Writing Turns
        w.write("*\n")
        w.write("* Table: Turns\n")
        w.write("*\n")
        w.write("$TURN:FROMNODENO;VIANODENO;TONODENO;TSYSSET;CAPPRT;TURN_CAP_1HR_OVERRIDE\n") 
        for turn in turns:
            line = wrtie_format(turn)
            w.write("{}\n".format(line)) 
        w.write("\n")
        #Writing Connectors
        w.write("*\n")
        w.write("* Table: Connectors\n")
        w.write("*\n")
        w.write("$CONNECTOR:ZONENO;NODENO;DIRECTION;TSYSSET;LENGTH;T0_TSYS(C);T0_TSYS(H);T0_TSYS(HT);T0_TSYS(MT);T0_TSYS(P);T0_TSYS(S);T0_TSYS(T);T0_TSYS(W)\n")
        for c in connectors:
            line = wrtie_format(c)
            w.write("{}\n".format(line))        

       

def main(): 
    #bank = _bank.Emmebank(select_bank())
    #bank = _bank.Emmebank("G:/corridors/swcorr/preDEIS/2035_Base_BRT/traffic/noConv/iter1/model/peak/assign/emmebank")
    #network = bank.scenario(get_scen_number(bank)).get_network()  
    network = get_network()    
    nodes, zones = create_all_nodes(network)
    links, connectors = create_links(network)
    turns = create_turns(network)
    wrtie_net_file(nodes, zones, links, turns, connectors)
    
if __name__ == "__main__":
    main()
    print "\nDONE"