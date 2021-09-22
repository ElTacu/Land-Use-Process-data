##############################################################
##
##  621comp.py
##
##  -- Move the script to the rpt's location and run it
##  -- Script that uses the 621_summary.rpt to compare the 
##     abs. value routes' times and distance
##  -- It display the top 5 routes in screen and outputs all 
##     of the routes in descending order to a csv
##
##  Daniel Jimenez, Metro, March 2, 2015
##
##############################################################

from collections import defaultdict, OrderedDict
from math import fabs
from operator import itemgetter
import os

Working_dir = os.path.dirname(os.path.realpath(__file__))

def get_pairs(lst):
    length = defaultdict(list)
    time = defaultdict(list)    
    for k, l, t in lst:
        length[k].append(l)
        time[k].append(t)    
    return length,time
    
def get_values(d):   
    abs_d = {} 
    for k, v in d.iteritems():
        r,v1,v2 = k, v[0],v[1]
        abs_d[k] = fabs(v1-v2)    
    return abs_d
    
def write_check(*args):
     with open(os.path.join(Working_dir,"621_Comp.csv"),"wb") as f:
        names = ["PM_Length","PM_Time","MID_Length","MID_Time"]
        for (name,item) in zip(names,args):
            if "Length" in name:
                dif = "Miles Dif."
            else:
                dif = "Min. Dif"
            results = OrderedDict()
            f.write("{},{}\n".format(name,dif))
            for z,(key, value) in enumerate(sorted(item.iteritems(), key=itemgetter(1), reverse=True)):                
                f.write("{},{}\n".format(key,value))
                if z < 5:
                    results[key] = value
            #`if block` used for Pm time print output.  
            #needed an extra tab for some reason.        
            if "PM_Time" in name: 
                print "{}\t\t{}".format(name,dif)
            else:
                print "{}\t{}".format(name,dif)
            for k,v in results.iteritems():                
                print "{}\t\t{}".format(k,v) 
            raw_input()
            f.write("\n")       
    
pm = []
mid = []
with open(os.path.join(Working_dir,"621_summary.rpt"), "rb") as f:
    for line in f:
        if line.strip():
            if "PM2" in line:
                per = "PM"
            elif "MD1" in line:
                per = "Mid"
            if not any(l in line for l in["Emme","Database","Scenario","-------","T R A N S I T","*****","line","type","(mi)","Total","above"]):          
                row = line.strip().split()
                if any( i in row[0] for i in["a","b"]) and "94X" not in line:
                    ##route = row[0]  length = row[5] time = row[6]
                    new_l = [row[0][:-1],float(row[5]),float(row[6])]
                    if per == "PM":
                        pm.append(new_l)
                    else:
                        mid.append(new_l)
    
pm_length,pm_time = get_pairs(pm)
md_length,md_time = get_pairs(mid)      
pl = get_values(pm_length)
pt = get_values(pm_time)
ml = get_values(md_length)
mt = get_values(md_time)                
write_check(pl,pt,ml,mt)                    