##############################################################
##
##  Coverage_factors.py
##
##  --Script to format csv factors from csv to emme format
##  --Input file must be named Coverage_Factors.csv
##  --Order of columns are TAZ,pk_hh,op_hh,pk_emp,op_emp
##
##  Daniel Jimenez, Metro, Feb 7, 2015
##
##############################################################

import csv, os
from collections import OrderedDict

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def write_covfac(mo,name,desc,dic):
    if os.path.exists("d311.txt"):
        mode = "a"
    else:
        mode = "w"
    with open("d311.txt", mode) as w:
        w.write("c\n")
        w.write("c\n")
        w.write("c\n")
        if mode is "w":
            w.write("t matrices\n")
        w.write("d matrix=mo{}\n".format(mo))
        w.write("a matrix=mo{0} {1} 0 {2}\n".format(mo,name,desc))
        for (k,v) in dic.iteritems():
            w.write("{} all: {}\n".format(k,v))
        for i in xrange(2148,2163):
            w.write("{} all: 0.000000\n".format(i))

pk_hh = OrderedDict()
pk_emp = OrderedDict()
op_hh = OrderedDict()
op_emp = OrderedDict()

with open("Coverage_Factors.csv", "rU") as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    for row in reader:
        t,phh,ohh,pemp,oemp = row
        pk_hh[t] = phh
        pk_emp[t] = pemp
        op_hh[t] = ohh
        op_emp[t] = oemp

write_covfac(10,"ohhcov","2035 Off-Peak HH Cvg Factors",op_hh)       
write_covfac(11,"phhcov","2035 Peak HH Cvg Factors",pk_hh)       
write_covfac(12,"oempco","2035 Off-Peak Emp Cvg Factors",op_emp)       
write_covfac(13,"pempco","2035 Peak Emp Cvg Factors",pk_emp)  
    
print "done"        
        
    