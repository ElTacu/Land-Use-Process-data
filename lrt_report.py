##############################################################
##
##  lrt_report.py
##
##  Input: An EMME transit line itinerary report file. 
##  Output: An LRT summary by line
##
##  Steve Hansen, Metro, August 12, 2008
##  Modified by Daniel Jimenez, Metro, December 8, 2014 
##
##############################################################
import os,sys
pythondir = 'L:/modrf/model/joan/programs_v2.5/src/py'
if pythondir not in sys.path:
    sys.path.append(pythondir)
from Report import Report  

def main(scenario):
    path = os.chdir(os.path.dirname(os.path.realpath(__file__))) # changes working directory to script's location

    report = Report()
    stop_dic = report.transit_stops(path)

    ttf_dic = {}
    with open("L:/modrf/model/joan/ttfs.csv","rU") as ttfs:
        for line in ttfs:
            fields = line.replace("\n","").split(",")
            ttf_dic[fields[0]] = fields[1]
        
    #Read lrt_walk report
    from_to = {}
    to_lenght = {}
    length_connection = []
    with open("lrtwalk_links.rpt", "rU") as f:
        for line in f:
            if not any(s in line for s in ["Emme","Database","Scenario","L I N K S","from","node","--","**","Selected","|","&"]): 
                line = line.strip()
                if line != "":                
                    to_lenght[line.split()[1]] = line.split()[2]                
                    if from_to.has_key(line.split()[0]):
                        from_to[line.split()[0]] = from_to[line.split()[0]] + ";" + line.split()[1]                
                    else:
                        from_to[line.split()[0]] = line.split()[1]               
                    
                    if line.split()[2] not in length_connection:
                         length_connection.append(line.split()[2]) 

    #Read Stations name
    station_names = {}    
    with open("L:/modrf/model/joan/lrt_stations.csv","rU") as f:
        for line in f:
            line = line.replace("\n","").split(",")
            station_names[line[0]] = line[1]    
    
    #Creating walk connection header
    length_connection.sort()    
    if "0" in length_connection:
        length_connection.remove("0")
    length_header = " mi walk connection,".join(length_connection)
    length_header = length_header + " mi walk connection"

    #Walking Zones
    zone_dic={}
    walk_05 = {}
    walk_13 = {}
    walk_26 = {}
    warning_nodes = {}
    station_community_zones = []
    with open("centroid_connector_list.out","rU") as centroid_conn_list:
        for line in centroid_conn_list:
            fields = line.replace("\n","").split()
            if fields!=[] and fields[0] == "a":
                if not(zone_dic.has_key(fields[2])):
                    zone_dic[fields[2]] = fields[1] + ";"
                elif (zone_dic[fields[2]].find(fields[1]) == -1):
                    zone_dic[fields[2]] = zone_dic[fields[2]] + fields[1] + ";"
                    
                if float(fields[3]) == 0.05:
                    if not(walk_05.has_key(fields[2])):
                        walk_05[fields[2]] = fields[1] + ";"
                    elif (walk_05[fields[2]].find(fields[1]) == -1):
                        walk_05[fields[2]] = walk_05[fields[2]] + fields[1] + ";"  
                        
                elif .051 <= float(fields[3]) <= 0.25:
                    if not(walk_13.has_key(fields[2])):
                        walk_13[fields[2]] = fields[1] + ";"
                    elif (walk_13[fields[2]].find(fields[1]) == -1):
                        walk_13[fields[2]]= walk_13[fields[2]]+fields[1] + ";"                
                    if float(fields[3]) == .13:
                        pass
                    else:
                        warning_nodes[fields[1]] = fields[3]
                
                elif float(fields[3]) >= .26:
                    if not(walk_26.has_key(fields[2])):
                        walk_26[fields[2]] = fields[1] + ";"
                    elif (walk_26[fields[2]].find(fields[1]) == -1):
                        walk_26[fields[2]] = walk_26[fields[2]] + fields[1]+";"                    
                    if float(fields[3]) == .26:
                        pass
                    else:
                        warning_nodes[fields[1]] = fields[3]
                    
    #Below is a temporary fix to get program running...
    #this won't be needed in the next round because these stops have been connected to zones

    #			zone_dic['48004']="1"
    #			stop_dic['48004']="1"
    #			zone_dic['16150']="1"
    #			stop_dic['16150']="1"

    pkrd_dic = {}
    pkrd_name_id = {}
    try:
        pk_lots = open("../inputs/lots.csv", "rU")
    except IOError:
        pk_lots = open("L:/modrf/model/joan/lots.csv","rU")
    for lot in pk_lots:
        line = lot.replace("\n","").split(",")
        pkrd_dic[line[0]] = line[3]
        pkrd_name_id[line[0]] = line[1]
    pk_lots.close()
    
    a = []
    with open("transit_line_itinerary_lrt.rpt","rU") as f:
        for line in f:            
            if not any(s in line for s in ['Emme','Database','Scenario','mode:','vehicle','headway:','default','---segment---','from',"*****"]):
                line = line.strip()
                if line != "":
                    if "layover" in line:
                        a.append(line)
                    elif "----" not in line:
                        a.append(line)
                        
    with open("lrt_report_{}.csv".format(scenario),"w") as lrt_lines_file:   
        for item in a:
            if "Transit line" in item:
                line = item.split()[2]
                dist_between_stops = 0
                lrt_lines_file.write(line + "\n")
                lrt_lines_file.write("station_name,from,to,length,ttf,speed,time,speed with dwell time,dwell,connected zones (to node),connected zones .05 walk," +
                                     "connected zones .13 walk,connected zones .26 walk,pkrd name ,pkrd lot,pkrd capacity,connecting lines (to node)," + length_header + "\n")
                
            elif "layover" in item:
                layover = item.split()[1]
                lrt_lines_file.write("layover:{} minutes.\n\n".format(layover))
            
            else:
                if "#.00" in item:
                    if dist_between_stops == 0: 
                        dist_between_stops = float(item.split()[3])
                        from_stop = item.split()[0]
                    else:
                       dist_between_stops = dist_between_stops + float(item.split()[3])                               
                else:
                    dist_between_stops = dist_between_stops + float(item.split()[3])
                    to_stop = item.split()[1]
                    ttf = item.split()[5]
                    speed = ttf_dic[ttf]
                    travel_time = (dist_between_stops/float(speed))*60
                    dwell = float(item.split()[4])
                    average_speed_with_dwell = dist_between_stops/((travel_time/60)+(dwell/60))
                    
                    #station_name
                    if station_names.has_key(from_stop):
                        station_name = station_names[from_stop]
                    else:
                        station_name = ""                        
                    
                    #Connecting lines
                    # if(6000<=fields[1]<=6999 or 65000<=fields[1]<=69999):
                        # print fields
                        # print "a"
                        # connecting_lines = stop_dic[to_stop].replace(",",";").replace(line+";","").replace(line,"")
                        # connecting_lines = connecting_lines + ";" + stop_dic[lrt_dic[from_stop + "," + to_stop]].replace(",",";").replace(line + ";", "").replace(line, "")
                    # else:
                        # print "b"
                        # connecting_lines = stop_dic[to_stop].replace(",",";").replace(line+";","").replace(line,"")
                    connecting_lines = stop_dic[to_stop].replace(",",";").replace(line+";","").replace(line,"")    
                    connecting_lines = report.format_connecting_lines(connecting_lines)  
                    
                    #Connecting zones
                    if zone_dic.has_key(to_stop):
                        connecting_zones = zone_dic[to_stop]
                        cz = connecting_zones.split(";")
                    else:
                        connecting_zones = ""
                        cz = ""
                        
                    #Connecting .05 walk zones
                    if walk_05.has_key(to_stop):
                        connecting_05_walk_zones = walk_05[to_stop]
                    else:
                        connecting_05_walk_zones = ""
                        
                    #Connecting .13 walk zones
                    if walk_13.has_key(to_stop):
                        connecting_13_walk_zones = walk_13[to_stop]
                    else:
                        connecting_13_walk_zones = ""
                        
                    #Connecting .26 walk zones
                    if walk_26.has_key(to_stop):
                        connecting_26_walk_zones = walk_26[to_stop]
                    else:
                        connecting_26_walk_zones = ""
                    
                    #Park n Ride fields                
                    pkrd_lot = ""
                    pkrd_cap = ""
                    pkrd_name = ""
                    for x in range(0,len(cz)):
                        if(pkrd_dic.has_key(cz[x])):
                            pkrd_lot = pkrd_lot + cz[x]
                            pkrd_cap = pkrd_cap + pkrd_dic[cz[x]]    
                            pkrd_name = pkrd_name + pkrd_name_id[cz[x]]

                    #Walking connecting transit
                    if from_to.has_key(to_stop):
                        routes_walking = {}                   
                        if ";" in from_to[to_stop]:
                            routes = from_to[to_stop].split(";")
                        else:
                            routes = from_to[to_stop].split()
                        
                        for route in routes:                        
                            if stop_dic.has_key(route):
                                if to_lenght[route] == "0":
                                   connecting_lines = connecting_lines + ";" + stop_dic[route]
                                else:
                                    distance = to_lenght[route]
                                    for i in range(0,len(length_connection)):
                                        if distance == length_connection[i]:
                                            if routes_walking.has_key(distance) and stop_dic.has_key(to_stop):
                                               routes_walking[distance] = routes_walking[distance] + ";" +stop_dic[route] 
                                            else:
                                                routes_walking[distance] = stop_dic[route]                                             
                        
                        for routes in routes_walking:
                            routes_walking[routes] = report.format_connecting_lines(routes_walking[routes])                  

                        fr = []
                        for i in length_connection:
                            fr.append(routes_walking.get(i,""))
                        final_routes_string = ",".join(fr)

                    lrt_lines_file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(station_name, from_stop, to_stop, dist_between_stops, ttf, speed, travel_time, average_speed_with_dwell, dwell,
                                                                                                    connecting_zones, connecting_05_walk_zones, connecting_13_walk_zones, connecting_26_walk_zones, 
                                                                                                    pkrd_name, pkrd_lot, pkrd_cap, connecting_lines, final_routes_string))                                  
                    dist_between_stops = 0
        
        #Create txt file if miscoded cc
        if len(warning_nodes) > 0:
            lrt_lines_file.write("\nWARNING. There are {} centroid connectors that need to be revised. Check centroid_connector_report.txt for more info". format(len(warning_nodes)))
            with open("centroid_connector_report{}.txt".format(scenario), "w") as revised:
                revised.write("The following centroid connectors have a distance that need to be revised\n\n")
                revised.write("Centroid connector\tDistance\n")
                for key, value in warning_nodes.iteritems() :
                    revised.write("{}\t\t\t{}\n".format(key,value))
  
if __name__ == "__main__":
    try:
        scen = int(raw_input("\nEnter scenario number: "))
        Report.write_lrt_mac(scen)
    except ValueError:
        print "Not a valid scenario number"
        sys.exit()
    os.system("emme -ng -m lrt_report")
    main(scen)
    print "DONE"