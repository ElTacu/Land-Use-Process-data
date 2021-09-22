##############################################################
##
##  Coverage_factors.py
##
##  --Uses series of shapefiles to calculate coverage factors 
##  --Final output are Coverage_Factors and Coverage_Factors_Full
##
##  Daniel Jimenez, Metro, Feb 11, 2015
##
##############################################################

import arcpy,os,shutil,traceback,csv
import easygui as eg
from dbfpy import dbf
  

class CovFac(object):
    def __init__(self, wd, hhshp, empshp, taz, period=["PK","OP"]):
        self.working_dir = wd
        self.hh_shape = hhshp
        self.emp_shape = empshp
        self.taz = taz
        self.period = period        
        arcpy.env.workspace = wd
        arcpy.env.overwriteOutput = True
        self.imp_nodes(self.working_dir,self.period)
        
    def imp_nodes(self, workdir, p):
        for i in p:
            pe_fold = eg.diropenbox(msg="Select {} Folder".format(i), #change to Aaron request
                                    title="Browse for {} Folder".format(i), 
                                    default=workdir)
            self.rename_files(pe_fold,i)
            self.copyfiles(pe_fold,workdir)
            self.set_projection("{}_emme_nodes.shp".format(i))
        self.move_source_shps(workdir)
    
    def rename_files(self, f, p):
        for root, dirs, files in os.walk(f):
            for fname in files:
                s = os.path.join(f,fname)
                n = os.path.join(f,"{}_{}".format(p,fname))
                os.rename(s,n)       

    def copyfiles(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
                
    def set_projection(self, shpf):
        coordinateSystem = "PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',8202099.737532808],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Foot',0.3048]]"
        arcpy.DefineProjection_management(shpf,coordinateSystem) 

    def move_source_shps(self, wl):     
        in_data_loc = "G:/corridors/swcorr/seed/preDEIS/inputs/cvg_factors/original_shapefiles_input"
        if os.path.isdir(in_data_loc):
            arcpy.Copy_management(os.path.join(in_data_loc,self.hh_shape),os.path.join(wl,self.hh_shape))
            arcpy.Copy_management(os.path.join(in_data_loc,self.emp_shape),os.path.join(wl,self.emp_shape))
            arcpy.Copy_management(os.path.join(in_data_loc,self.taz),os.path.join(wl,self.taz))
            self.buffer_things(self.period)
        else:
            print "{} \nDoes not exist please make sure the hhlds and emp  shps points are in this folder".format(in_data_loc)
            
    def buffer_things(self, p):
        for i in p:
            arcpy.MakeFeatureLayer_management("{}_emme_nodes.shp".format(i), "{}_emme_nodes_bs".format(i), "DATA1 = 1")
            arcpy.Buffer_analysis("{}_emme_nodes_bs".format(i),"{}_buffer_bus.shp".format(i),".2 Miles",dissolve_option = "All")
            arcpy.MakeFeatureLayer_management("{}_emme_nodes.shp".format(i), "{}_emme_nodes_SC_BRT".format(i), "DATA2 = 1")
            arcpy.Buffer_analysis("{}_emme_nodes_SC_BRT".format(i),"{}_buffer_SC_BRT.shp".format(i),".35 Miles",dissolve_option = "All") 
            arcpy.MakeFeatureLayer_management("{}_emme_nodes.shp".format(i),"{}_emme_nodes_LRT".format(i), "DATA3 = 1")
            arcpy.Buffer_analysis("{}_emme_nodes_LRT".format(i),"{}_buffer_LRT.shp".format(i),".5 Miles",dissolve_option = "All")
            inFeatures = ["{}_buffer_LRT.shp".format(i), "{}_buffer_SC_BRT.shp".format(i), "{}_buffer_bus.shp".format(i)]
            arcpy.Union_analysis (inFeatures, "{}_buffer_union.shp".format(i))
            arcpy.Dissolve_management("{}_buffer_union.shp".format(i),"{}_buffer.shp".format(i))
            self.selector(self.emp_shape,self.hh_shape,"{}_buffer.shp".format(i),"{}".format(i))
        self.spatial_join(self.emp_shape,self.taz,"Emp_SJ.shp")
        self.spatial_join(self.hh_shape,self.taz,"HH_SJ.shp")    
        self.taz_summaries()        

    def selector(self, empshape, hhshape, buffer_shpe, filed):
        arcpy.MakeFeatureLayer_management(empshape, 'elyr') 
        arcpy.SelectLayerByLocation_management('elyr', 'COMPLETELY_WITHIN',buffer_shpe)
        arcpy.CalculateField_management('elyr',filed,1,"PYTHON_9.3")
        arcpy.MakeFeatureLayer_management(hhshape, 'hlyr') 
        arcpy.SelectLayerByLocation_management('hlyr', 'COMPLETELY_WITHIN',buffer_shpe)
        arcpy.CalculateField_management('hlyr',filed,1,"PYTHON_9.3")
        
    def spatial_join(self, ishp, taz, outshp):
        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(taz)
        fieldmappings.addTable(ishp)
        arcpy.SpatialJoin_analysis(ishp,taz,outshp,"#","#",fieldmappings) 

    def taz_summaries(self):
        statsFields = [["PK","SUM"],["OP","SUM"]]
        t_s = "Taz_Sum.shp"
        arcpy.Statistics_analysis("Emp_SJ.shp", "Emp_sum.dbf", statsFields, "TAZ")
        arcpy.Statistics_analysis("HH_SJ.shp", "HH_sum.dbf", statsFields, "TAZ")
        arcpy.MakeFeatureLayer_management("taz_cvg.shp","lyl")
        arcpy.AddJoin_management("lyl","TAZ","Emp_sum.dbf","TAZ") 
        arcpy.AddJoin_management("lyl","TAZ","HH_sum.dbf","TAZ") 
        arcpy.CopyFeatures_management("lyl", t_s)
        self.final_taz(t_s)

    def final_taz(self,in_shape):        
        codeblock = """def getc_f(cnt,cv):
        if cnt == 0:
            return float(cnt)
        else: 
            return float(cv/cnt) """
        ##Rename taz_sum fields 
        #Taz field
        arcpy.AddField_management(in_shape, "TAZ", "FLOAT", "", "")
        arcpy.CalculateField_management(in_shape,"TAZ","!taz_cvg_TA!","PYTHON_9.3")
        #Emp_CNT
        arcpy.AddField_management(in_shape, "Emp_CNT", "FLOAT", "", "")
        arcpy.CalculateField_management(in_shape,"Emp_CNT","!Emp_sum_FR!","PYTHON_9.3")
        #Emp_PK_CNT
        arcpy.AddField_management(in_shape, "Emp_PK_CNT", "FLOAT", "", "")
        arcpy.CalculateField_management(in_shape,"Emp_PK_CNT","!Emp_sum_SU!","PYTHON_9.3")
        #Emp_OP_CNT
        arcpy.AddField_management(in_shape, "Emp_OP_CNT", "FLOAT", "", "")
        arcpy.CalculateField_management(in_shape,"Emp_OP_CNT","!Emp_sum__1!","PYTHON_9.3")
        #HH_CNT
        arcpy.AddField_management(in_shape, "HH_CNT", "FLOAT", "", "")
        arcpy.CalculateField_management(in_shape,"HH_CNT","!HH_sum_FRE!","PYTHON_9.3")
        #HH_PK_CNT
        arcpy.AddField_management(in_shape, "HH_PK_CNT", "FLOAT", "", "")
        arcpy.CalculateField_management(in_shape,"HH_PK_CNT","!HH_sum_SUM!","PYTHON_9.3")
        #HH_OP_CNT
        arcpy.AddField_management(in_shape, "HH_OP_CNT", "FLOAT", "", "")
        arcpy.CalculateField_management(in_shape,"HH_OP_CNT","!HH_sum_S_1!","PYTHON_9.3")    
        #HH_PK_cf
        arcpy.AddField_management(in_shape, "HH_PK_cf", "FLOAT", "7", "6")
        arcpy.CalculateField_management(in_shape,"HH_PK_cf","getc_f(!HH_CNT!,!HH_PK_CNT!)","PYTHON_9.3", codeblock)
        #HH_OP_cf
        arcpy.AddField_management(in_shape, "HH_OP_cf", "FLOAT", "7", "6")
        arcpy.CalculateField_management(in_shape,"HH_OP_cf","getc_f(!HH_CNT!,!HH_OP_CNT!)","PYTHON_9.3", codeblock)
        #EMP_PK_cf
        arcpy.AddField_management(in_shape, "EMP_PK_cf", "FLOAT", "7", "6")
        arcpy.CalculateField_management(in_shape,"EMP_PK_cf","getc_f(!EMP_CNT!,!EMP_PK_CNT!)","PYTHON_9.3", codeblock)
        #EMP_OP_cf
        arcpy.AddField_management(in_shape, "EMP_OP_cf", "FLOAT", "7", "6")
        arcpy.CalculateField_management(in_shape,"EMP_OP_cf","getc_f(!EMP_CNT!,!EMP_OP_CNT!)","PYTHON_9.3", codeblock)    
        deleted_fileds = ["taz_cvg_Sh","Emp_sum_OI","HH_sum_OID","HH_sum_TAZ","Emp_sum_TA","taz_cvg_TA","Emp_sum_FR","Emp_sum_SU","Emp_sum__1","HH_sum_FRE","HH_sum_SUM","HH_sum_S_1"]
        arcpy.DeleteField_management("Taz_Sum.shp",deleted_fileds)

        
def create_work_folder():
    wf_loc = eg.diropenbox(msg=None, title=None, default="c:/")
    while True:
        try:
            wf = eg.enterbox(msg ="Enter working folder's name ", title =' ', default ='')
            folder = os.path.join(wf_loc,wf)
            os.makedirs(folder)
            break
        except OSError as exception: 
             eg.msgbox("A folder with this name already exist. Please enter a new name")
    return folder 

def dbf2csv(w):
    in_dbf = dbf.Dbf(os.path.join(w,"Taz_Sum.dbf"))
    csv_f = os.path.join(w,"Coverage_Factors_Full.csv")
    csv_e = os.path.join(w,"Coverage_Factors.csv")
    names = [field.name for field in in_dbf.header.fields]
    data = [rec.fieldData for rec in in_dbf]
    in_dbf.close()
    sor_dat = []
    for i in xrange(0,len(data)+1):
        for item in data:
            if int(item[0]) == i:
                sor_dat.append(item)    
    with open(csv_f,"wb") as f, open(csv_e,"wb") as e:
        csv_writer = csv.writer(f)
        csv_writer.writerow(names)
        for i in sor_dat:
            csv_writer.writerow(i)        

        h = [names[0],names[7],names[8],names[9],names[10]]       
        csv_writer = csv.writer(e)
        csv_writer.writerow(h)
        for i in sor_dat:
            taz = int(i[0])
            r = [taz,"{0:.6f}".format(i[7]),"{0:.6f}".format(i[8]),"{0:.6f}".format(i[9]),"{0:.6f}".format(i[10])] 
            csv_writer.writerow(r)    

def main(): 
    print "Creating Coverage Factors"
    emp_shape = "emp05_30_011306.shp"
    hh_shape = "hh05_30_011106.shp"
    taz_cvg = "taz_cvg.shp"
    working_loc = create_work_folder()
    my_coverage_project = CovFac(working_loc,hh_shape,emp_shape,taz_cvg)
    dbf2csv(working_loc)
    shutil.copyfile("L:/modrf/model/joan/programs_v2.5/src/py/format_coverage_factors.py",os.path.join(working_loc,"format_coverage_factors.py"))      
    print "Program ran successfully"

if __name__ == "__main__":
    main()
