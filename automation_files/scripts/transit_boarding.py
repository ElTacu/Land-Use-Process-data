##############################################################
##
##  tranist_boarding.py
##
##  --Script that reads the 621 summary and reports lines by mode.
##
##  Daniel Jimenez, Metro, March 15, 2016
##
##############################################################

import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl import load_workbook
from collections import OrderedDict
import sys
import os

#Class that holds different dicts to hold all the report values according to the period and type of transit
class transit_summary(object):
    def __init__(self):
        self.pm_light = OrderedDict()
        self.pm_commuter = OrderedDict()
        self.pm_bus = OrderedDict()
        self.pm_street = OrderedDict()

        self.md_light = OrderedDict()
        self.md_commuter = OrderedDict()
        self.md_bus = OrderedDict()
        self.md_street = OrderedDict()
        
    def add_transit(self,input,period):
        row = input.split()
        type = row[1]
        name = row[0]
        boardings = int(row[7])

        if period == "PM":
            if type == 'l': 
                self.pm_light[name] = boardings
            if type == 'b': 
                self.pm_bus[name] = boardings
            if type == 'r': 
                self.pm_commuter[name] = boardings
            if type == 'e': 
                self.pm_street[name] = boardings
        elif period == "MD":
            if type == 'l': 
                self.md_light[name] = boardings
            if type == 'b': 
                self.md_bus[name] = boardings
            if type == 'r': 
                self.md_commuter[name] = boardings
            if type == 'e': 
                self.md_street[name] = boardings                

###
#Functions that read the report
##
                
#Function that determines time period from 621 report
def period(input):
    if "PM" in input:
        return "PM"
    if "MD" in input:
        return "MD"
        
#Reads the report and queries data lines. sends data to transit calss.
def read_report():                
    time = ""
    transit = transit_summary()
    
    #m_path = ../model
    m_path = os.path.dirname(os.path.dirname(sys.argv[1]))    
    
    report = os.path.join(m_path,"peak/assign/621_summary.rpt")
    with open(report, "rb") as file:
        for line in file:
            line = line.strip()
            if line:
                if not any(s in line for s in ["Emme","Database","T R A N S I T","line","type","(MI)","**","-","|","Total"]):
                    if any(s in line for s in ["PM","MD"]):
                        time = period(line)
                    #If statment that dertmines if the period is PM or MD and makes sure it isnt the line with the scenario number
                    #Scenario line nessesary to dertmine time period
                    if time in ["PM","MD"] and not line.startswith("Scenario"):
                        transit.add_transit(line,time)
    write_to_excel(transit)

    
###########
#Functions to that write to the final excel spreadsheet 
###########

#Function that takes both pm and md obejcts and writes the data
#Returns the row index plus 2 to account for the next block                        
def write_transit_routes(sheet,data, data_md, row, title):
    sheet["A{}".format(row)] = title
    bold_it(sheet["A{}".format(row)])
    write_columns(sheet,row)
    row += 1    
    for k,v in data.iteritems():
        sheet["A{}".format(row)] = k
        sheet["B{}".format(row)] = v
        sheet["C{}".format(row)] = data_md.get(k,"No service")
        row += 1
    sheet["A{}".format(row)] = "Total"
    bold_it(sheet["A{}".format(row)])
    sheet["B{}".format(row)] = sum(data.values())
    sheet["C{}".format(row)] = sum(data_md.values())
    return row + 2

def bold_it(cell):
    cell.font = Font(bold=True)
    
def write_columns(sheet,row):
    sheet["B{}".format(row)] = "PM"
    sheet["B{}".format(row)].alignment = Alignment(horizontal="center")
    bold_it(sheet["B{}".format(row)])
    
    sheet["C{}".format(row)] = "MD"
    sheet["C{}".format(row)].alignment = Alignment(horizontal="center")
    bold_it(sheet["C{}".format(row)])
        
#Function that opens the excel spreadsheet and calls wrtie_trasnit_routes to populate cells according to the transit object attributes    
def write_to_excel(transit):    
    excel_file = sys.argv[1]
    run_name = sys.argv[2]
    des_excel = excel_file
    des_book = load_workbook(des_excel)
    transit_sheet = des_book.get_sheet_by_name("Transit Boardings")
    transit_sheet["A2"].value = run_name    
    r = write_transit_routes(transit_sheet, transit.pm_light, transit.md_light ,3, "Light Rail")
    r = write_transit_routes(transit_sheet, transit.pm_bus, transit.md_bus,r, "Bus")
    r = write_transit_routes(transit_sheet, transit.pm_street, transit.md_street,r, "Street Car")
    r = write_transit_routes(transit_sheet, transit.pm_commuter, transit.md_commuter,r, "Commuter Rail")
    des_book.save(des_excel)
    
    
def main():    
    read_report()

    
if __name__ == "__main__":
    main()