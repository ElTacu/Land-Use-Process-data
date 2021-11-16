import arcpy
from collections import defaultdict
import time

start_time = time.time()

arcpy.env.workspace = "C:/Users/jimenez/Desktop/vincent_map_data-master"
arcpy.env.overwriteOutput = True

# input,output, and interim Shapefiles
bikeNodesFeatures = "C:/Users/jimenez/Desktop/vincent_map_data-master/BikeNetwork_Nodes.shp"
bikeNetwork = "C:/Users/jimenez/Desktop/vincent_map_data-master/BikeNetwork.shp"

#Create x-y field and calculate coordinates for Bike points
arcpy.AddField_management(bikeNodesFeatures, "x","DOUBLE")
arcpy.AddField_management(bikeNodesFeatures, "y","DOUBLE")

arcpy.CalculateField_management(bikeNodesFeatures,"x","!Shape!.Centroid.X","PYTHON")
arcpy.CalculateField_management(bikeNodesFeatures,"y","!Shape!.Centroid.Y","PYTHON")


dup_points = defaultdict(list)
#Creates a dic that holds all the nodes that share the same x-y coordinates
with arcpy.da.SearchCursor(bikeNodesFeatures, ["NODEID","x","y"]) as cursor:
    for row in cursor:
        xy = "{}-{}".format(row[1],row[2])
        dup_points[xy].append(row[0])

#Update each from and to node field to the first index of dup_points values if values has more than 1 node id
with arcpy.da.UpdateCursor(bikeNetwork, ["FROMNODE","TONODE"]) as cursor:
    for row in cursor:
        for v in dup_points.values():
            if len(v) > 1:
                if row[0] in v:
                    row[0] = v[0]
                if row[1] in v:
                    row[1] = v[0]
                cursor.updateRow(row)

####create points shapefile to get mid point of flagged links
spatial_reference = arcpy.Describe(bikeNetwork).spatialReference
midpoints = arcpy.CreateFeatureclass_management(arcpy.env.workspace, "BikeDubPoints.shp", "POINT", spatial_reference = spatial_reference)

nodes_combinations = []
nodes_combinations_reverse = []

with arcpy.da.SearchCursor(bikeNetwork,["FROMNODE","TONODE","SHAPE@"]) as in_cursor, arcpy.da.InsertCursor(midpoints, "SHAPE@") as out_cursor:
    for row in in_cursor:
        #Get current node from to and to from combination
        fromToNodes = "{}-{}".format(row[0],row[1])
        toFromNodes = "{}-{}".format(row[1],row[0])        
        
        #Check if this combination already exists
        #If it does is a flagged link and a point to that link is assigned in the midpont shapefile
        if fromToNodes not in nodes_combinations:
            nodes_combinations.append(fromToNodes)
        else:
            midpoint = row[2].positionAlongLine(0.50,True).firstPoint
            out_cursor.insertRow([midpoint]) 

        #Same to check in case the link has the same combination but backwards.
        if fromToNodes not in nodes_combinations_reverse:
            nodes_combinations_reverse.append(toFromNodes)
        else:
            midpoint = row[2].positionAlongLine(0.50,True).firstPoint
            out_cursor.insertRow([midpoint])              
        
        # check for links that have the same end and start point coordinates. looped links
        #If loop link, add 2 split points to split the link into 3 parts.
        if  row[0] == row[1]:
            midpoint = row[2].positionAlongLine(0.33,True).firstPoint
            out_cursor.insertRow([midpoint])             
            midpoint = row[2].positionAlongLine(0.66,True).lastPoint
            out_cursor.insertRow([midpoint]) 

arcpy.SplitLineAtPoint_management(bikeNetwork, midpoints, "Bike_split_links.shp", "10 Meters")
                
print("--- {} seconds ---".format(time.time() - start_time))             