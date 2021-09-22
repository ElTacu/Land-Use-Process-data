##############################################################
## 
## 24 Hr performance measure gui
## Front end to the Emmys 24 hr performance measures class
## Daniel Jimenez, Metro, June 21, 2015 
##
##############################################################

#####Notes Finished hours option. Set graph options and move to tti (links for create not defined. might be left out)

import Tkinter
from Tkinter import *
import ttk
import os, sys
from PIL import ImageTk, Image
import tkFileDialog
from permer import Emmys
from collections import OrderedDict

class simpleapp_tk(Tkinter.Tk):       
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.protocol('WM_DELETE_WINDOW', self.Exit)
        
    
    def initialize(self):    
        #main_frame 
        mainframe = ttk.Frame(self, padding=("5","5","12","0"))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)  

        # State variables    
        self.path1 = StringVar() 
        self.path2 = StringVar() 
        self.output = StringVar() 
        self.description = StringVar()
        self.warning = StringVar()
        type_list = ["Create Profile","Create Profile by TTI", "Get Link Volume"]
        #controls index of measure combobox
        self.mesures = OrderedDict({0:"VMT - Vehicle Miles Traveled", 1:"VHD - Vehicle-Hours of Delay", 2:"VHT - Vehicle Hours Traveled", 3:"V/C - Volume/Capacity", 4:"Speed", 5:"Volume"})  
        #Same but for graph
        self.graphs = OrderedDict({0:"Bar Graph", 1:"Linear Graph"})        

        #Button Scen 1
        self.scen1_btn = ttk.Button(self, text = "Select 1st Scenario Bank", command = lambda: self.askfile("1st", self.path1), width = 2) 
        self.scen1_btn.grid(row = 0, column = 0, padx = 10,pady = 5, sticky = (N,S,E,W))  
        #Entry Scen 1
        self.path1_entry = Entry(self, textvariable = self.path1, width = 99, state = "readonly") 
        self.path1_entry.grid(row = 0, column = 1, padx = 10,pady = 8, sticky = N) 
        
        #Button Scen 2
        self.scen2_btn = ttk.Button(self, text = "Select 2nd Scenario Bank", command = lambda: self.askfile("2nd", self.path2))
        self.scen2_btn.grid(row = 1, column = 0, padx = 10,pady = 5, sticky = (N,S,E,W))   
        #Entry Scen 2
        self.path2_entry = Entry(self, textvariable = self.path2, width = 99, state = "readonly") 
        self.path2_entry.grid(row = 1, column = 1, padx = 10,pady = 8, sticky = N) 
        
        #Button Output Folder
        self.output_btn = ttk.Button(self, text = "Select Output Folder", command = self.askfolder)
        self.output_btn.grid(row = 2, column = 0, padx = 10,pady = 5, sticky = (N,S,E,W)) 
        #Button Output Folder
        self.output_entry = Entry(self, textvariable = self.output, width = 99, state = "readonly") 
        self.output_entry.grid(row = 2, column = 1, padx = 10,pady = 8, sticky = N)       
        
        
        #Type label
        self.type_lbl = ttk.Label(self, text = "Select Type of Analysis")
        self.type_lbl.grid(row = 3, column = 0, padx = 10, pady = 0, sticky = (W))
        #ComboBox Type of analysis: Normal profile, By tti, link's volume
        self.type_box = ttk.Combobox(self, values = type_list)      
        self.type_box.grid(row = 4, column = 0, padx = 10,pady = 5, sticky = (N,S,E,W))
        self.type_box.bind('<<ComboboxSelected>>', self.show_description)
        self.type_box.set("Choose Analysis")       
        #Type of analysis Description
        self.analysist_text = Text(self, width = 50, height = 10)        
        self.analysist_text.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = (N,S,E,W), rowspan = 3)

        #Options
        #Measure type        
        self.measure_lbl = ttk.Label(self, text = "Select Measure", anchor="center")
        self.measure_lbl.grid(row = 8, column = 0, padx = 10, pady = 0, sticky = (E))
        #ComboBox Measure: VMT, VHD, etc..
        self.mesure_box = ttk.Combobox(self, values = [v for k, v in self.mesures.iteritems()]) 
        self.mesure_box.grid(row = 8, column = 1, padx = 10,pady = 5, sticky = (N,S,E,W))
        self.mesure_box.current(0)
        
        #---Description 1
        self.d1_lbl = ttk.Label(self, text = "--- Facility types must be separated by commas", anchor='center')
        self.d1_lbl.grid(row = 9, column = 0, padx = 10, pady = 0, columnspan = 1, sticky = (E)) 
        
        #---Facility type        
        self.faty_lbl = ttk.Label(self, text = "Insert Facility Types", anchor="center")
        self.faty_lbl.grid(row = 10, column = 0, padx = 10, pady = 0, sticky = (E))
        #Facility Types entry box
        self.faty_entry = Entry(self, width = 99) 
        self.faty_entry.grid(row = 10, column = 1, padx = 10,pady = 5, sticky = (N,S,E,W))
        
        #---links ids        
        self.links_lbl = ttk.Label(self, text = "Insert Link's id", anchor="center")
        self.links_lbl.grid(row = 11, column = 0, padx = 10, pady = 0, sticky = (E))
        #links entry box
        self.link_entry = Entry(self, width = 99) 
        self.link_entry.grid(row = 11, column = 1, padx = 10,pady = 5, sticky = (N,S,E,W))
        
        #Hours
        self.hours_lbl = ttk.Label(self, text = "From-To in (24hr). Blank if all day ", anchor = "center")
        self.hours_lbl.grid(row = 12, column = 0, padx = 10, pady = 0, sticky = (E))
        #links entry box
        self.hours_entry = Entry(self, width = 99) 
        self.hours_entry.grid(row = 12, column = 1, padx = 10,pady = 5, sticky = (N,S,E,W))
        
        #---output file name        
        self.outputfile_lbl = ttk.Label(self, text = "Name of Output File", anchor = "center")
        self.outputfile_lbl.grid(row = 13, column = 0, padx = 10, pady = 0, sticky = (E))
        #links entry box
        self.outfile_entry = Entry(self, width = 99) 
        self.outfile_entry.grid(row = 13, column = 1, padx = 10,pady = 5, sticky = (N,S,E,W))
        
        #Type of Graph
        self.graph_lbl = ttk.Label(self, text = "Select type of Graph", anchor="center")
        self.graph_lbl.grid(row = 14, column = 0, padx = 10, pady = 0, sticky = (E))
        #graph entry box
        self.graph_box = ttk.Combobox(self, values = [v for k, v in self.graphs.iteritems()]) 
        self.graph_box.grid(row = 14, column = 1, padx = 10, pady = 0, columnspan = 1, sticky = (W))
        self.graph_box.current(0)
        
        #Create Button
        self.create_btn = Button(self, text = "Create Profile", width = 15, bd = 4, command = self.crate_profile) 
        self.create_btn.grid(row = 15, column = 1, padx = 10,pady = 5, sticky = E) 

        #Create Warning
        self.warnme = ttk.Label(self, textvariable = self.warning) 
        self.warnme.grid(row = 16, column = 0, padx = 10, pady = 5, sticky = W)       
      
        
    def crate_profile(self, *args):
        self.warning.set("")  
        type_ana = self.type_box.current() # Current type combobox index
        graph_id = self.graph_box.current()
        #self.path1.get() is path of first bank
        #self.path2.get() is path of second bank
        #self.output.get() is path of output folder


        #Check for inputs send warning if missing info
        #If ok create object and get data from class
        if self.check_inputs():
            options_plot = {"VMT":{"TITLE":"Vehicle Miles Traveled (VMT)", "DES":"VMT = sum(link.length * link.auto_volume) by hour", "YLAB":"Miles Traveled"},
                "VHD":{"TITLE":"Vehicle Hours of Delay (VHD)", "DES":"VHD = sum(VHT - VHT(Free Flow)) by hour", "YLAB":"Hours Delayed"},
                "VHT":{"TITLE":"Vehicle Hours Traveled (VHT)", "DES":"VHT = sum(link.auto_time/60) * link.auto_volume by hour", "YLAB":"Hours Traveled"},
                "V/C":{"TITLE":"Congested Miles (V/C)", "DES":"V/C = link.auto_volume / link.capacity by hour\nCongested where V/C between .9 and 1", "YLAB":"Congested Miles"},
                "V/C_S":{"TITLE":"Severely Congested Miles (V/C)", "DES":"V/C = link.auto_volume / link.capacity by hour\nSeverely Congested where V/C >= 1", "YLAB":"Congested Miles"},
                "SPEED":{"TITLE":"Mean Speed", "DES":"Speed = sum(link.length / (link.auto_time/60)) by hour", "YLAB":"Mi/Hr"},
                "VOLUME":{"TITLE":"Auto Volume", "DES":"Volume = sum(link.auto_volume)) by hour", "YLAB":"Volume"}}

            
            e = Emmys()
            #Block to check that there are values for each option. if not, defaults to an empty string
            try:
                fa_types = [int(x) for x in self.faty_entry.get().split(",")]
            except ValueError:
                fa_types = None       
            
            #Other variables settings
            link_id = self.link_entry.get()     
            output_name = self.outfile_entry.get()
            hours = self.hours_entry.get()
            graph = self.graphs[graph_id].split()[0]
            
            print "Creating Data... Please wait"
            #------ For 'create performance' method ------
            if type_ana == 0: 
                measure = self.get_mesure().upper() #Selects among vht, vmt, vhd etc...
                
                if measure == "SPEED": sp = True #block that changes the plot format to display mean speed instead of sum
                else: sp = None   
                
                #Create dataframe with passed paramaters
                e.create(banks = (self.path1.get(),self.path2.get()), 
                          measure = measure, 
                          f_type = fa_types, 
                          links = link_id)
                          
                #Gets max number from dataframe to set the y limit in the graph. mostly useful for speed graph          
                y_max = int(e.df[[1,2]].max().max() * 1.8) 
                
                #Check for vc case. Graphing is unique becasue of dataframe structure
                if measure == "V/C":
                    e.plot(title = "Scen 1 and Scen 2 {}\n in a 24 Hr. Assigment".format(options_plot["V/C_S"]['TITLE']),
                       description = options_plot["V/C_S"]['DES'], measure = "Severely Congested Miles", y_label = options_plot["V/C_S"]['YLAB'], y_limit = y_max, speed = sp)
                    
                    e.save_plot(os.path.join(self.output.get(),"Sev{}.pdf".format(self.outfile_entry.get())), vc = True)                          
                #-------------------------------------------------------------------------------------------------------#
                
                e.plot(title = "Scen 1 and Scen 2 {}\n in a 24 Hr. Assigment".format(options_plot[measure]['TITLE']),
                       description = options_plot[measure]['DES'], measure = measure, y_label = options_plot[measure]['YLAB'], y_limit = y_max, speed = sp)

                #----- Get hours csv if requested
                if hours:
                    start,end =  map(int,a.split("-")) # get int hour from splitting input
                    hrs_period = range(start, end + 1) # create list with all the hours in between
                    out_cols = list(e.df.columns)[1:]   # get all the columns to export
                    csv_file = e.df[out_cols].loc[d["Hour"].isin(hrs_period)]                    
                    csv_file.to_csv(os.path.join(self.output.get(),"{}.csv".format(self.outfile_entry.get())), index = False)
                else:
                    e.df.to_csv(os.path.join(self.output.get(),"{}.csv".format(self.outfile_entry.get())), index = False)                
                
                #Saves plot and clear all data
                e.save_plot(os.path.join(self.output.get(),"{}.pdf".format(self.outfile_entry.get())))
                
                
                
            elif type_ana == 1:
                mer = self.get_mesure()

            else:
                print "nah"
            self.warning.set("*Performance Measure Created.") #Letting user know its getting data      
            print "Data Created"
    
    def check_inputs(self, *args):
        if not self.path1.get():
            self.warning.set("*WARNING:\nPlease select an Emmy bank for 1st scenario.")
            return False
        elif not self.path2.get():   
            self.warning.set("*WARNING:\nPlease select an Emmy bank for 2nd scenario.") 
            return False            
        elif not self.output.get():   
            self.warning.set("*WARNING:\nPlease select an output folder.")
            return False
        elif self.type_box.current() == -1:
            self.warning.set("*WARNING:\nPlease select type of analysis from options.")
            return False
        elif not self.outfile_entry.get():    
            self.warning.set("*WARNING:\nPlease enter a name for the output file.") 
            return False
        else:
            return True
           

    def get_mesure(self, *args):       
        mer_index = self.mesure_box.current() # Current measure's combobox index
        return self.mesures[mer_index].split("-")[0].strip()  

        
    def askfile(self, trun, path_var):        
        filename = tkFileDialog.askopenfilename(parent = self, title = 'Choose {} Scenario Folder'.format(trun))
        path_var.set(filename)
        
    def askfolder(self):
        dirname = tkFileDialog.askdirectory(parent = self, title = 'Choose output Scenario Folder')
        self.output.set(dirname)
        
    def show_description (self, *args):
        id = self.type_box.current()
        self.analysist_text.config(state = NORMAL)
        normal = ("Creates a VMT, VHD, VHT, V/C, speed or volumes profile.\n"
                  "Facility types - Includes selected facility types.\n" 
                  "Links - If only selected links are desired. Entered as i_node-j_node.\n")
        tti = ("Creates a VMT, VHD, VHT, V/C, speed  or volumes profile by Travel Time Index (TTI).\n"
               "Facility types - Includes selected facility types.\n" 
               "Links - If only selected links are desired. Entered as i_node-j_node.\n"
               "TTI levels defined as:\nA = TTI < 1.10\nB = 1.10 <= TTI <= 1.25\nC = <=1.25 TTI <= 1.50\nD = TTI >= 1.50")                    
        link = "Gets volume of a specific link. Entered as i_node-j_node.\n"             
        if id == 0:            
            self.analysist_text.delete(1.0, END)       
            self.analysist_text.insert(INSERT ,normal)
            self.mesure_box.config(state = NORMAL)
            self.faty_entry.config(state = NORMAL)
        elif id == 1:
            self.analysist_text.delete(1.0, END)       
            self.analysist_text.insert(INSERT ,tti)
            self.mesure_box.config(state = NORMAL)
            self.faty_entry.config(state = NORMAL)
        else:
            self.analysist_text.delete(1.0, END)       
            self.analysist_text.insert(INSERT ,link)
            self.mesure_box.config(state = DISABLED)
            self.faty_entry.config(state = DISABLED)          
        self.analysist_text.config(state = DISABLED)
        
    def Exit(self):
        self.destroy()    
        self.quit()


        
        
if __name__ == "__main__":        
    app = simpleapp_tk(None)
    app.title('24 Hours Profiles')
    app.mainloop() 
    