##############################################################
##
##  mode_shares.py
##
##
##  Daniel Jimenez, Metro, March 15, 2016
##
##############################################################


import openpyxl
from openpyxl import load_workbook
from collections import defaultdict
import sys
import os
   

def load_vector(path):
    #Folder ../../model/reports    
    folder = os.path.dirname(os.path.realpath(path))
    #Notebook = ../../model/reports/notebook
    notebook_folder = os.path.join(folder,"notebook")
    for root, dirnames, filenames in os.walk(notebook_folder):
        for file in filenames:
            if "mode_share_summary_vector" in file:
                return [float(x.strip()) for x in open(os.path.join(notebook_folder,file),'r')]
   
def load_data(sheet, name, vector):
    sheet["C3"].value = name
    dic_data = defaultdict(int)
    reference = [int(x) for x in open("V:/tbm/kate/programs_v1.0/src/py/automation_files/joan_summary_cell_references.csv", 'r')]
    data = zip(reference,vector)
    
    #Zip reference cell and value. Reference cell should point to where value should go in the report
    for r,v in data:
        dic_data[r] += v
    
    #Write value referencing the key cell and the value
    for k,v in dic_data.iteritems():
        sheet["C{}".format(k)].value = int(round(v,0))

def main():
    #Passed arguments
    excel_file = sys.argv[1]
    run_name = sys.argv[2]
    
    #Load mode_share_summary_vector into a list
    summary_vector = load_vector(excel_file)
    
    des_excel = excel_file
    des_book = load_workbook(des_excel)
    mode_sheet = des_book.get_sheet_by_name("Mode Choice Summary")
    load_data(mode_sheet,run_name,summary_vector)
    des_book.save(des_excel)        
        
        
if __name__ == "__main__":    
    main()        
