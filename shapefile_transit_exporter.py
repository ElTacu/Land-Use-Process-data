#Script that will export all individual fields based on name attribute from master shapefile_transit_exporter
#Update to select shapefile and get env path to complete the script


import arcpy

arcpy.env.workspace = "I:/ModServStaff/jimenez/shapefile_transit_exporter"

fieldList = arcpy.ListFields("2040FC_tlines.shp")

fields = {i:str(field.baseName) for i,field in enumerate(fieldList)}

for k,v in fields.iteritems():
    print k,v

transit_field = int(raw_input("Select index to select by"))

rows = arcpy.SearchCursor("2040FC_tlines.shp")

for row in rows:
    row_name = row.getValue(fields[transit_field])
    SQL = "{} = '{}'".format(fields[transit_field], row_name) 
    arcpy.MakeFeatureLayer_management("2040FC_tlines.shp", 'lyr', SQL) 
    arcpy.management.CopyFeatures("lyr", "{}.shp".format(row_name))
