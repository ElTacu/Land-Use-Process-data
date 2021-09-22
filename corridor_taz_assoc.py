#Script that outputs taz coverage in special format. 
#Ask Cindy about the file and format

import csv,os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

corridors = []
with open("Corridor_TAZ_assoc.csv","r") as f:
    reader = csv.reader(f)
    for line in reader:
        corridors.append(line)    

tot_rows = len(corridors[0]) 
tot_lines = len(corridors) #222
header = ",".join(corridors[0])

#print corridors[1]
def check(taz,e):
    if str(taz) == e:
        return e
    else:
        return "-"

def checker(taz,l):
    a = False
    for x in l:
        if str(taz) == x:
            a = True
    return a

def clean(li, sep=','):
    splitted = [i.split(sep) for i in li]
    if not splitted:
        return "invalid input" # or anything you like
    amount = len(splitted[0])
    if any(len(s) != amount for s in splitted):
        return "invalid input 2" # or anything you like
    d = ['-'] *  amount
    for s in splitted:
        for z, (dz, sz) in enumerate(zip(d, s)):
            d[z] = max(dz, sz)
    return sep.join(d)  
    
with open("ECorridor_TAZ_assoc.csv","w") as f:
    f.write("TAZ,{}\n".format(header))  
    for i in range (1,2163):
        con = i
        final = []    
        for l in range(1,tot_lines):
            lw = []
            con = i            
            for x in corridors[l]:             
                se = check(i,x)
                lw.append(se)
            good = checker(i,lw)
            if good is True:
                s = ",".join(lw)
                if con == i:
                    print "{}  {} {} {}".format(i,con,l,s)
                    final.append(s) 
        sf = clean(final)
        f.write("{},{}\n".format(i,sf))  