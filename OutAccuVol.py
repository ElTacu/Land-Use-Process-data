#Script use to format danyust outputs

import math

link_info = []
minutes = 0
counter = 0
string_attacher = ""
#num_links = math.ceil(32/10.0)
num_links = math.ceil(2302/10.0)
#print num_links

for line in open('L:\\modrf\\DTA\\utilities\\_forConversion\\DynusT_inputs_red\\OutAccuVol.dat'):  
    s = line.strip()    
    if "=" in line or s[0:1].isalpha() == True:
        pass
    else:
        s = line.strip()         
        if len(s) >= 3 and len(s) <= 5: 
            minutes += 1    
        if len(s) > 9: 
            string_attacher += "\t" + s
            counter +=1
            #print counter
            if  counter == num_links:
                string_attacher = string_attacher.strip()
                #print string_attacher
                holder = string_attacher.split() 
                #print holder
                link_info.append(holder)
                #print link_info
                counter = 0                
                string_attacher = ""
        else:
            pass
time_header = ""
for r in range(1,(minutes+1)):
    time_header += "time{},".format(r)    
time_header = time_header[0:-1]
writer = open("L:\\modrf\\DTA\\utilities\\_forConversion\\outputs_green\\volume_.csv", 'w')
writer.write(time_header)


for i in range(0,len(link_info[0])):
    link_row = ""
    for idx, links in enumerate(link_info):     
        link_row += link_info[idx][i] + "," 
    link_row = link_row[:-1]
    writer.write("\n" + link_row)
writer.close()
print "done"