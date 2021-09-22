import inro.emme.database.emmebank as _bank
from pandas import DataFrame
import numpy as np
from datetime import datetime
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict


class Emmys(object):
    def __init__(self):
        self.df = DataFrame(data=np.arange(24), columns=["Hour"])
        
#Public Methods    
    
    #Method to create vmt, vhd, vht and vc, speed 
    #Check function dict for definitions
    # Kargs
    # -Bank's Path, 
    # -Measure: such as vmt, vhd, vht and vc, speed. check self.functions for definitions
    # -F_type: for facility type query in a list type
    # -Assigment: different type of assigment. Peak, Non peak at the moment
    # -Links: Only for selected links in list type  
    def create(self, **kargs):
        self.__get_bank(kargs['path'])        
        d = []
        measure = kargs['measure'].upper()
        for s in self.__fetch_scenario(self.bank):
            agr = []
            self.severe = []
            self.congested = []
            hour =  self.__get_hour(s)
            for link in self.__fetch_links(s.number):
                if  link["@speed"] > 0 and self.__is_auto(link):  
                    if kargs.get('f_type'):
                        link = self.__f_type(link, kargs['f_type'])
                    if kargs.get('links'):
                         link = self.__links(link, kargs['links'])
                    if link is not None:
                        if measure == "VC":
                            self.__v_c(link)                        
                            cname = ["Hour","CONGESTED MILES_PS","SEVERELY CONGESTED MILES_PS"]                    
                        else:        
                            agr.append(self.functions[measure])
                            cname = ["Hour","{}_PS".format(measure)]

            if measure == "VC":
                d.append([hour,sum(self.congested),sum(self.severe)])
            elif measure == "SPEED":
                d.append([hour,sum(agr)/len(agr)])
            else:    
                d.append([hour,sum(agr)])

        columns = self.__columns(kargs['assignment'],cname)
        temp = DataFrame(d, columns = columns)       
        self.df = DataFrame.merge(self.df, temp, how="left", on="Hour")    

    
    def by_tti(self,path = None, assignment = None, f_type = None, measure = None):
        self.__get_bank(path)
        d = [] 
        measure = measure.upper()
        for s in self.__fetch_scenario(self.bank):
            hour = self.__get_hour(s)
            self.res = defaultdict(list)       
            for link in self.__fetch_links(s.number):                
                if self.__is_auto(link) and link["@speed"] > 0:                   
                    link = self.__f_type(link, f_type)
                    if link is not  None:
                        c_tti = self.__tti(link)                    
                        self.__result_tti(c_tti, measure, link)                       
            d.append([hour,sum(self.res[measure]),sum(self.res["a"]),sum(self.res["b"]),sum(self.res["c"]),sum(self.res["d"])])                                                         
        columns = self.__columns(assignment,["Hour","{}_P".format(measure),"{}A_P".format(measure),
                                             "{}B_P".format(measure),"{}C_P".format(measure),"{}D_P".format(measure)])
        temp = DataFrame(d, columns = columns)
        try:
            if isinstance(self.df_tti,DataFrame):
                self.df_tti = DataFrame.merge(self.df_tti, temp, how = "left", on = "Hour")
            else:
                self.df_tti = DataFrame.merge(self.df, temp, how = "left", on = "Hour")                
        except AttributeError: 
            self.df_tti = DataFrame.merge(self.df, temp, how = "left", on = "Hour")
            
            
    def get_links_volume(self, **kargs):
        self.__get_bank(kargs['path'])
        d = []
        if kargs.get('one_way'):
            one_way = True
            if kargs['dire'].upper() == "N":
                cnames = ["Hour","NB_PS"]
            if kargs['dire'].upper() == "S":
                cnames = ["Hour","SB_PS"]
            if kargs['dire'].upper() == "E":
                cnames = ["Hour","EB_PS"]                
            if kargs['dire'].upper() == "W":
                cnames = ["Hour","WB_PS"]
        else:     
            one_way = False
            if kargs['dire'].upper() == "S":
                cnames = ["Hour","SB_PS","NB_PS"]
            elif kargs['dire'].upper() == "W": 
                cnames = ["Hour","WB_PS","EB_PS"]
                
        for s in self.__fetch_scenario(self.bank):
            volume = 0
            r_volume = 0
            hour = self.__get_hour(s)
            for link in self.__fetch_links(s.number):                 
                if link.id in kargs['links']:
                    if one_way:
                        volume += link.auto_volume
                    else:    
                        volume += link.auto_volume
                        r_volume += link.reverse_link.auto_volume           
            if one_way:
                d.append([hour,volume])
            else:
                d.append([hour,volume, r_volume])
        columns = self.__columns(kargs['assignment'], cnames)    
        temp = DataFrame(d, columns = columns)
        self.df = DataFrame.merge(self.df, temp, how="left", on="Hour")
        


        
        
    def plot_volumes(self, **kargs):        
        if kargs.get("one_way"):
            color = ["b","r"]
            if kargs["dire"].upper() == "N":
                d = "N"
                columns = ["NB_PS","NB_NPS"]
                labs = ["NB Peak Spread","NB Non Peak Spread"]
            elif kargs["dire"].upper() == "E":
                d = "E"
                columns = ["EB_PS","EB_NPS"]
                labs = ["EB Peak Spread","EB Non Peak Spread"]
            elif kargs["dire"].upper() == "W":
                d = "W"
                columns = ["WB_PS","WB_NPS"]
                labs = ["WB Peak Spread","WB Non Peak Spread"]
            elif kargs["dire"].upper() == "S":
                d = "S"
                columns = ["SB_PS","SB_NPS"]
                labs = ["SB Peak Spread","SB Non Peak Spread"]            
            the_format =  "Total Daily {d1}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}\
                           \n\nTotal 4 to 6 PM {d1}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}\
                           \n\nTotal 7 to 9 AM {d1}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}".format(                          
                                self.df[columns [0]].sum(), self.df[columns [1]].sum(),                     
                                self.df[columns [0]].loc[self.df['Hour'].isin([16,17,18])].sum(),
                                self.df[columns [1]].loc[self.df['Hour'].isin([16,17,18])].sum(),                          
                                self.df[columns [0]].loc[self.df['Hour'].isin([7,8,9])].sum(),
                                self.df[columns [1]].loc[self.df['Hour'].isin([7,8,9])].sum(), d1=d)                 
 
        else:
            color = ["b","g","r","c"]
            if kargs["dire"].upper() == "S":
                d1,d2 = "S","N"
                columns = ["SB_PS","NB_PS","SB_NPS","NB_NPS"]
                labs = ["SB Peak Spread","NB Peak Spread","SB Non Peak Spread","NB Non Peak Spread"]
            elif kargs["dire"].upper() == "W":
                d1,d2 = "W","E"
                columns = ["WB_PS","EB_PS","WB_NPS","EB_NPS"]
                labs = ["WB Peak Spread","EB Peak Spread","WB Non Peak Spread","EB Non Peak Spread"]
            the_format =  "Total Daily {d1}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}\
                            \n\nTotal Daily {d2}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}\
                            \n\nTotal 4 to 6 PM {d1}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}\
                            \n\nTotal 4 to 6 PM {d2}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}\
                            \n\nTotal 7 to 9 AM {d1}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}\
                            \n\nTotal 4 to 6 PM {d2}B Volume\nPeak Spread = {:2,.0f}\nNon Peak Spread = {:2,.0f}".format(
                                    self.df[columns [0]].sum(), self.df[columns [2]].sum(),
                                    self.df[columns [1]].sum(), self.df[columns [3]].sum(),
                                    self.df[columns [0]].loc[self.df['Hour'].isin([16,17,18])].sum(),
                                    self.df[columns [2]].loc[self.df['Hour'].isin([16,17,18])].sum(),
                                    self.df[columns [1]].loc[self.df['Hour'].isin([16,17,18])].sum(),
                                    self.df[columns [3]].loc[self.df['Hour'].isin([16,17,18])].sum(),                             
                                    self.df[columns [0]].loc[self.df['Hour'].isin([7,8,9])].sum(),
                                    self.df[columns [2]].loc[self.df['Hour'].isin([7,8,9])].sum(),
                                    self.df[columns [1]].loc[self.df['Hour'].isin([7,8,9])].sum(),
                                    self.df[columns [3]].loc[self.df['Hour'].isin([7,8,9])].sum(), d1=d1,d2=d2)               
                
                

        self.ax = self.df[columns].plot(kind='bar', title= kargs['title'], color = color,  
                                                                   figsize =(15,10),legend=False, fontsize=12, grid=False)
        self.ax.set_xlabel("Hour",fontsize=12)
        self.ax.set_ylabel("Auto Volume",fontsize=12)
        patches, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(patches, labs, 
                  loc = 2, title = "Assigment Method by Directionality")

        self.ax.text(.01, .80, the_format,       
                    horizontalalignment='left',
                    verticalalignment='top',
                    transform = self.ax.transAxes,
                    fontsize = 10)                 
            
    def plot(self, **kargs):       
        columns = ["{}_{}".format(kargs["measure"].upper(), i) for i in ["PS","NPS"]]
        if kargs.get('speed'):            
            the_format =  'Daily Mean Speed\nPeak Spread = {:2,.1f} Mi/Hr\nNon Peak Spread = {:2,.1f} Mi/Hr\
                          \n\n4 to 6 PM Mean Speed\nPeak Spread = {:2,.1f} Mi/Hr\nNon Peak Spread = {:2,.1f} Mi/Hr\
                          \n\n7 to 9 AM Mean Speed\nPeak Spread = {:2,.1f} Mi/Hr\nNon Peak Spread = {:2,.1f} Mi/Hr'\
                           .format(self.df[columns[0]].mean(), self.df[columns[1]].mean(), 
                                self.df[columns[0]].loc[self.df['Hour'].isin([16,17,18])].mean(),
                                self.df[columns[1]].loc[self.df['Hour'].isin([16,17,18])].mean(), 
                                self.df[columns[0]].loc[self.df['Hour'].isin([7,8,9])].mean(),
                                self.df[columns[1]].loc[self.df['Hour'].isin([7,8,9])].mean())
        else:
            if kargs["measure"].upper() == "CONGESTED MILES":
                lab = "Congested Miles"
            elif kargs["measure"].upper() == "SEVERELY CONGESTED MILES": 
                lab =    "Severely Congested Miles" 
            else:
                lab = kargs['measure']
            the_format = 'Total Daily {mes}\nPeak Spread = {0:2,.0f}\nNon Peak Spread = {1:2,.0f}\
                          \n\nTotal 4 to 6 PM {mes}\nPeak Spread = {2:2,.0f}\nNon Peak Spread = {3:2,.0f}\
                          \n\nTotal 7 to 9 AM {mes}\nPeak Spread = {4:2,.0f}\nNon Peak Spread = {5:2,.0f}'\
                          .format(self.df[columns[0]].sum(), self.df[columns[1]].sum(), 
                                  self.df[columns[0]].loc[self.df['Hour'].isin([16,17,18])].sum(),
                                  self.df[columns[1]].loc[self.df['Hour'].isin([16,17,18])].sum(), 
                                  self.df[columns[0]].loc[self.df['Hour'].isin([7,8,9])].sum(),
                                  self.df[columns[1]].loc[self.df['Hour'].isin([7,8,9])].sum(), mes = lab)
        
        self.ax = self.df[columns].plot(kind='bar', title = kargs['title'], color = ["#66A3C2","red"],
                                            figsize =(15,10),legend = False, fontsize = 12, grid = False)
        self.ax.set_xlabel("Hour",fontsize=12)
        self.ax.set_ylabel(kargs['y_label'],fontsize=12)
        if kargs.get('y_limit'):
            self.ax.set_ylim(0, kargs['y_limit'])   
        patches, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(patches, ["Peak Spread Assigment","Non Peak Spread Assigment"], loc = 2, title = "Assigment Method")
        self.ax.text(.01, .88,kargs['description'], 
                  horizontalalignment='left',
                  verticalalignment='top',
                  transform = self.ax.transAxes,
                  fontsize = 8)
        self.ax.text(.01, .83, the_format,
             horizontalalignment='left',
             verticalalignment='top',
             transform = self.ax.transAxes,
             fontsize = 10)
        
        
    def plot_by_tti(self, **kargs):
        p_columns = ["{}{}".format(kargs["measure"].upper(),i) for i in ["A_P","B_P","C_P","D_P"]]
        self.ax = self.df_tti[p_columns].plot(kind='bar', title=kargs['title'],figsize =(15,10),legend=False, 
                                       fontsize=12, grid=False, stacked=True, 
                                       color =['#0000FF', '#006B00', '#FF9900', '#CC0000'],position = 1,width=.35)
        self.ax.set_xlabel("Hour",fontsize=12)
        self.ax.set_ylabel(kargs['y_label'],fontsize=12)
        if kargs.get('y_limit'):
            self.ax.set_ylim(0, kargs['y_limit'])   

        np_columns = ["{}{}".format(kargs["measure"].upper(),i) for i in ["A_NP","B_NP","C_NP","D_NP"]] 
        self.df_tti[np_columns].plot(ax=self.ax, kind='bar',figsize =(15,10),legend=False, 
                                               fontsize=12, grid=False, stacked=True, 
                                               color =['#9999FF', '#99C499', '#FFD699', '#FFB2B2'],position = 0,width=.35)
        patches, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(patches, ["1.0 - 1.10", "1.10 - 1.25", "1.25 - 1.50","1.50 >"], loc ='upper left', title = "Travel Time Index")

        if kargs["measure"].upper() == "MILES":
            the_format = 'Notes:\nDarker Bar = Peak Spread Assigment\nTTI = link.free_flow / link.congested speed\
                          \n{:2,.0f} Total Road Lane Miles'.format(e1.df_tti['MILES_P'].max())
        else:
            the_format = 'Notes:\nDarker Bars = Peak Spread Assigment\
                          \nTTI = link.free_flow / link.congested_speed\n{des}\
                          \n\nTotal Daily {mes}\nPeak Spread = {0:2,.0f}\nNon Peak Spread = {1:2,.0f}\
                          \n\nTotal 4 to 6 PM {mes}\nPeak Spread = {2:2,.0f}\nNon Peak Spread = {3:2,.0f}\
                          \n\nTotal 7 to 9 AM {mes}\nPeak Spread = {4:2,.0f}\nNon Peak Spread = {5:2,.0f}'\
                          .format(self.df_tti[p_columns].sum(axis = 1).sum(), self.df_tti[np_columns].sum(axis = 1).sum(), 
                                  self.df_tti[p_columns].loc[self.df_tti['Hour'].isin([16,17,18])].sum(axis = 1).sum(),
                                  self.df_tti[np_columns].loc[self.df_tti['Hour'].isin([16,17,18])].sum(axis = 1).sum(), 
                                  self.df_tti[p_columns].loc[self.df_tti['Hour'].isin([7,8,9])].sum(axis = 1).sum(),
                                  self.df_tti[np_columns].loc[self.df_tti['Hour'].isin([7,8,9])].sum(axis = 1).sum(), 
                                  mes = kargs['measure'], des = kargs['description'])
        
        self.ax.text(.01, .80,the_format,
             horizontalalignment='left',
             verticalalignment='top',
             transform = self.ax.transAxes,
             fontsize = 8)
        
        self.ax.text(.01, .80,the_format,
             horizontalalignment='left',
             verticalalignment='top',
             transform = self.ax.transAxes,
             fontsize = 8)
        
    
    def save_plot(self, path, vc = "False"):
        fig = self.ax.get_figure()
        fig.savefig(path)
        if vc == "False":
            self.__clear_data()
       
            
            
# private methods
    def __get_hour(self, scenario):
        return int(scenario.id[2:])

    def __clear_data(self):
        self.df = DataFrame(data=np.arange(24), columns=["Hour"]) 
        self.df_tti = None

    def __speed(self,link):
        return link.length / (link.auto_time/60)
    
    def __volume(self,link):
        return link.auto_volume
    
    def __lane_miles(self, link):
        return link.length * link.num_lanes

    def __v_c(self, link):
        if link.volume_delay_func in [1,2,3,5,6,7]:            
            vol_cap =  float(link.auto_volume) / link.data3 
        elif link.volume_delay_func in [4,8]:
            vol_cap =  float(link.auto_volume) / link["@mb"] 
        else:
            vol_cap = 0
        
        if .9 <= vol_cap < 1.0:
            #self.congested.append(link.length * self.__vmt(link))
            self.congested.append(link.length)
        elif vol_cap >= 1.0:
            #self.severe.append(link.length * self.__vmt(link))
            self.severe.append(link.length)
    
    def __vmt(self, link):
        return link.length * link.auto_volume
    
    def __vht(self, link):
        return (link.auto_time/60) * link.auto_volume
    
    def __vhd(self, link):
        return self.__vht(link) - self.__vhtff(link)
    
    def __vhtff(self, link):        
        return (link.length / link["@speed"]) * link.auto_volume
    
    def __tti(self, link):
        speedau =  (60 * link.length) / link.auto_time #congested speed
        tti = link["@speed"] / speedau
        return tti 

    def __fetch_scenario(self, bank):
        for scenario in bank.scenarios():
            if 2000 <= scenario.number < 3000:
                yield scenario                
                        
    def __fetch_links(self, s):            
        network_links = self.bank.scenario(s).get_network().links()            
        for link in network_links:
            yield link

    def __get_bank(self, path):
        self.bank = _bank.Emmebank(path) 
                             
    def __columns(self, assignment, names):
        if  assignment.lower().startswith('peak'):
            return names
        else:
            for i, n in  enumerate(names):
                if n != "Hour":
                    temp = n.split("_")             
                    nps_name = "{}_N{}".format(temp[0],temp[1])         
                    names[i] = nps_name
            return names
    
    def __is_auto(self, link):
        self.functions = {"VMT":self.__vmt(link), "VHT":self.__vht(link), "VHD":self.__vhd(link),
                                     "SPEED":self.__speed(link), "VOLUME":self.__volume(link)}
        if 1 <= link.volume_delay_func <= 9 and any("c" in str(m) for m in link.modes):            
            return True
        return False
    
    def __result_tti(self, tti, measure, link):
        functions = {"VMT":self.__vmt(link), "VHT":self.__vht(link), "VHD":self.__vhd(link), "MILES":self.__lane_miles(link)}
        self.res[measure].append(functions[measure])
        if  tti < 1.10:
            self.res["a"].append(functions[measure])
        elif 1.10 <= tti < 1.25:    
            self.res["b"].append(functions[measure])
        elif 1.25 <= tti < 1.50:
            self.res["c"].append(functions[measure])
        elif tti >= 1.50:
            self.res["d"].append(functions[measure])    

    def __f_type(self, link, f_type):
        if link.volume_delay_func in f_type:
            return link      
            
    def __links(self, link, links):
        if link.id in links:
            return link
    ##########################################################

 