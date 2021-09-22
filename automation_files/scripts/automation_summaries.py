##############################################################
##
##  Driver scritp that set variables copy excel template and call scripts
##
##   Daniel Jimenez, Metro, March 15, 2016
##
##############################################################

import os
import sys
import shutil


def create_working_folders(path):
    try:
        auto_files = os.path.join(path, "model/reports/auto_files")
        os.mkdir(auto_files)
        d2d_fodler = os.path.join(auto_files, "dist2dist")
        os.mkdir(d2d_fodler)
    except WindowsError:
        pass    

def copy_template(dir, file, name = "CutlineComparison"):
    file_name = "model/reports/{}_results.xlsx".format(name)
    destination = os.path.join(dir,file_name)
    shutil.copyfile(file, destination)
    return destination

def main():
    summary_source = "V:/tbm/kate/programs_v1.0/src/py/automation_files/summary_template.xlsx"
    template_source = "V:/tbm/kate/programs_v1.0/src/py/automation_files/2015_CutlineComparisonVehicles_template.xlsx"
    
    #Model root folder
    working_dir = os.path.dirname(os.path.realpath(__file__))
    path_list = working_dir.split(os.sep)
    run_name = path_list[-1]
    
    create_working_folders(working_dir)
    target_file = copy_template(working_dir, summary_source ,run_name)
    cut_file = copy_template(working_dir, template_source)
    
    ###Run Different Summaries Scripts
    ##For Mode shares needs to find out vector location
    print  "Running Mode Shares"
    os.system("python V:/tbm/kate/programs_v1.0/src/py/automation_files/scripts/mode_shares.py {} {}".format(target_file, run_name))
    
    ##For Tansit boardings need to find location of report
    print  "Transit Boardings"
    os.system("python V:/tbm/kate/programs_v1.0/src/py/automation_files/scripts/transit_boarding.py {} {}".format(target_file, run_name))
    
    ##Cutlines and RMSE
    print  "Cutlines"
    os.system("python V:/tbm/kate/programs_v1.0/src/py/automation_files/scripts/2015cutlines.py {}".format(cut_file))
    # os.system("python V:/tbm/kate/programs_v1.0/src/py/automation_files/scripts/RMSE_Summary.py {}".format(cut_file))
    
    ##AverageTripLength
    print "Runnin Avg Trips"
    os.system("python V:/tbm/kate/programs_v1.0/src/py/automation_files/scripts/average_trip_length.py {} {}".format(target_file, run_name))

    ##Dist2Dist
    print "Runnin Dist2Dist"
    os.system("python V:/tbm/kate/programs_v1.0/src/py/automation_files/scripts/dist_2_dist.py {} {}".format(target_file, run_name))
    

    print "Done"
if __name__ == "__main__":
    main()


