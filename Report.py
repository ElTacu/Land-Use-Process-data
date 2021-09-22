##############################################################
##
##  Report.py
##
##  --Class used to for lrt_report.py and zones_report.py
##
##  Daniel Jimenez, Metro, December 12, 2014
##
##############################################################

from collections import OrderedDict

class Report(object):
    def __init__(self):
        self.data = []
    
    def transit_stops(self,path):
        line_dic = {}                        
        with open("transit_line_itinerary.rpt", "rU") as f:
            for line in f:
                if not any(s in line for s in ["Emme","Database","Scenario","mode:","vehicle","headway:","default","segment","from","***","----"]):
                    line = line.strip()
                    if line != "":
                        fields = line.replace("\n","").split()
                        if "Transit" in line:              
                           trline = fields[2]
                           line_dic[trline] = [] 
                        elif "#.00" not in line:
                            line_dic[trline].append(fields[1])                        
        stop_dic={}
        for x in range(0,len(line_dic)):
            item = line_dic.popitem()        
            for stop in range(0,len(item[1])):
                if(stop_dic.has_key(item[1][stop])):
                    stop_dic[item[1][stop]] = stop_dic[item[1][stop]]+ ";" + item[0]
                else:
                    stop_dic[item[1][stop]] = item[0]    
        return stop_dic
    
    def format_connecting_lines(self,input):
        holder = input.split(";")
        unique_lines = list(OrderedDict.fromkeys(holder))         
        unique_lines.sort()
        formatted = ";".join(unique_lines)
        try:
            if ";" in formatted[0]:
                formatted = formatted[1:]
        except IndexError:
            pass
        return formatted

    @staticmethod
    def write_lrt_mac(scen):    
        with open("V:/tbm/joan/macros_v2.5/lrt_report.mac" , "w") as f:
            f.write("~<centroid_connector_list 2162\n")
            f.write("~<transit_line_itinerary {}\n".format(scen))
            f.write("~<lrtwalk_links\n")
            f.write("q")

    @staticmethod
    def write_zone_mac(scen):    
        with open("V:/tbm/joan/macros_v2.5/zone_report.mac" , "w") as f:
            f.write("~<centroid_connector_list 2162\n")
            f.write("~<transit_line_itinerary {0}\n".format(scen))
            f.write("~<lrtwalk_links\n")
            f.write("q")   

    
    def walk_from2(self,path):
        from_to = {}
        with open("lrtwalk_links.rpt", "rU") as f:
            for line in f:
                if not any(s in line for s in ["Emme","Database","Scenario","L I N K S","from","node","--","**","Selected","|","&"]): 
                    line = line.strip()
                    if line != "":             
                        if from_to.has_key(line.split()[0]):
                            from_to[line.split()[0]] = from_to[line.split()[0]] + ";" + line.split()[1]                
                        else:
                            from_to[line.split()[0]] = line.split()[1]
        return from_to
        
    def walk_2len(self,path):
        to_lenght = {}
        with open("lrtwalk_links.rpt", "rU") as f:
            for line in f:
                if not any(s in line for s in ["Emme","Database","Scenario","L I N K S","from","node","--","**","Selected","|","&"]): 
                    line = line.strip()
                    if line != "":                
                        to_lenght[line.split()[1]] = line.split()[2]
        return to_lenght
        
        
    def length_connection(self,path):
        length_connection = []
        with open("lrtwalk_links.rpt", "rU") as f:
            for line in f:
                if not any(s in line for s in ["Emme","Database","Scenario","L I N K S","from","node","--","**","Selected","|","&"]): 
                    line = line.strip()
                    if line != "": 
                        if line.split()[2] not in length_connection:
                            length_connection.append(line.split()[2]) 
        return to_lenght