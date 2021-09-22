##############################################################
## 
## Creates a new project and travel time histogram comparison
##
##############################################################


import os
import sys
import shutil
import inro.emme.desktop.app as _app
import inro.emme.desktop.printer as _printer


#get argument form callable
emmebank_path = sys.argv[1] #Call to the model/peak/assign/emmebank file
working_dir = os.path.dirname(emmebank_path) # Usually ../model/peak/assign

#need to check if project exists here
try:    
    shutil.rmtree(os.path.join(working_dir,"New_Project"))
    project = _app.create_project(working_dir,"New_Project")#change to relative path
except WindowsError:
    if os.path.exists(working_dir):
        project = _app.create_project(working_dir,"New_Project")
    else:
        print "Path does not exit. Please enter an existing path."
        sys.exit()        

    
my_app = _app.start_dedicated(False, "000", project)
data = my_app.data_explorer()
bank = data.add_database(emmebank_path)#change to relative path
bank.open() 

##Open work sheet and set x attributes
tt_histogram_ws = my_app.open_worksheet("V:/tbm/kate/macros_v1.0/shell/tt_histogram.emw")
hist = tt_histogram_ws.layer(layer_name = "Matrix histogram")
hist.par("XRange").set(-3.0, index=0)
hist.par("XRange").set(3.0, index=1)
hist.par("XRange").set(0.05, index=2)

##Set printing attributes
my_settings = _printer.Settings()
my_settings.margins.left = 5.0
my_settings.margins.top = 5.0
my_settings.margins.right = 5.0
my_settings.margins.bottom = 5.0
my_settings.orientation = "LANDSCAPE"
my_settings.extend_to_margins = True
my_settings.set_standard_paper("LETTER")

image_filepath = os.path.join(working_dir,"tt_histogram.pdf")
tt_histogram_ws.save_as_pdf(image_filepath, my_settings)

tt_histogram_ws.close()
bank.close()