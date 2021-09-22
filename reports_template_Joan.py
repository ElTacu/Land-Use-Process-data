##############################################################
##
##  reports_template_Joan.py
##
##  --Script to populate reports_template_Joan.xmlm with different vector files.
##
##  Daniel Jimenez, Metro, Feb 23, 2015
##
##############################################################

import csv, os
import win32com.client
import easygui as eg
from collections import OrderedDict

data = OrderedDict() 
num_files = int(eg.enterbox(msg="How many files are you processing?", title=' ', default=''))
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
for i in xrange(1,num_files + 1):
    vector = eg.fileopenbox(msg="Select {} Vector".format(ordinal(i)), title=None, default=None)      
    if vector == None:
        good = False
        break 
    name = eg.enterbox(msg="Select {} Vector Name".format(ordinal(i)), title=' ', default='')
    if name == None:
        good = False
        break        
    with open(vector,"r")as f:
        reader = csv.reader(f)
        data[name] = [v[0] for v in reader]
        good = True

if good == True:
    reports_template_joan = eg.fileopenbox(msg="Select reports_template_Joan file", title=None, default=None) 
f_path = os.path.dirname(reports_template_joan)
next_col = os.path.join(f_path,"next_col.txt")

try:
    with open(next_col,"r") as f:
        column = int(f.readline())
except IOError:
    column = 3
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
wb = excel.Workbooks.Open(reports_template_joan)
mcss = wb.Worksheets(2) #Mode Choice Summary Sheet 
for k, v in data.iteritems():
    mcss.Cells(3, column).Value = k
    for i,z in enumerate(v):
        row = 139 + i
        mcss.Cells(row, column).Value = z
    column += 4
wb.Save()
wb.Close()
excel.Quit()

with open(next_col,"w") as w:
    w.write(str(column))