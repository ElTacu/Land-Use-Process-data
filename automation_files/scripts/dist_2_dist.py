##############################################################
##
##  Dist_2_Dist.py
##
##  --Script that populates the dist2dist summary.
##
##  Daniel Jimenez, Metro, March 5, 2016
##
##############################################################

import openpyxl
from openpyxl import load_workbook
import sys
import subprocess
import os
from dist2dist_1 import create_d2d


def run_r(root):
    subprocess.call("Rscript --slave --vanilla V:/tbm/kate/programs_v1.0/src/py/automation_files/scripts/dist2dist_valid.R {}".format(root))

root = os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[1])))
run_r(root)    
excel_file = sys.argv[1]
data_folder = os.path.join(os.path.dirname(sys.argv[1]),"auto_files/dist2dist")

des_excel = excel_file
des_book = load_workbook(des_excel)
dtd_sheet = des_book.get_sheet_by_name("dist2dist")
dtd_raw_sheet = des_book.get_sheet_by_name("dist2dist_raw")
create_d2d(dtd_raw_sheet,dtd_sheet,data_folder)

des_book.save(des_excel)   