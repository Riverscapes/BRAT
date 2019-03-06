﻿# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Name:             Find Braided Reaches in Stream Network                          #
# Purpose:          Find Braided Reaches as part of network preprocessing steps.    #
#                                                                                   #
# Author:           Kelly Whitehead (kelly@southforkresearch.org)                   #
#                   Jesse Langdon                                                   #
#                   South Fork Research, Inc                                        #
#                   Seattle, Washington                                             #
#                                                                                   #
# Created:          2014-Sept-30                                                    #
# Version:          2.0 beta                                                        #
# Modified:         2017-Feb-16                                                     #
# Documentation:    http://gnat.riverscapes.xyz/                                    #
#                                                                                   #
# Copyright:        (c) Kelly Whitehead, Jesse Langdon 2017                         #
#                                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#!/usr/bin/env python

# Import modules
import os
import sys
import arcpy
from SupportingFunctions import field_is_in_network


def main(fcStreamNetwork, canal, tempDir, is_verbose):
    # Polyline prep
    if is_verbose:
        arcpy.AddMessage("Checking input fields and if canals shapefile exists...")
    listFields = arcpy.ListFields(fcStreamNetwork,"IsMultiCh")
    if len(listFields) is not 1:
        arcpy.AddField_management(fcStreamNetwork, "IsMultiCh", "SHORT", "", "", "", "", "NULLABLE")
    arcpy.CalculateField_management(fcStreamNetwork,"IsMultiCh",0,"PYTHON")

    # Process
    if canal is None:
        findBraidedReaches(fcStreamNetwork, is_verbose)
    else:
        handleCanals(fcStreamNetwork, canal, tempDir, is_verbose)

    use_stream_names(fcStreamNetwork)
    return


def use_stream_names(stream_network):
    if not field_is_in_network(stream_network, "StreamName"):
        return

    with arcpy.da.UpdateCursor(stream_network, ["IsMainCh", "StreamName"]) as cursor:
        for row in cursor:
            if row[0] == 0 and len(row[1]) > 3: # if the stream name isn't empty, make it a main channel
                row[0] = 1
                cursor.updateRow(row)


def handleCanals(stream_network, canal, temp_folder, is_verbose):
    """
    Finds braided sections of the stream network, not counting canals, if canals are available
    :param stream_network:
    :param canal:
    :param temp_folder:
    :param is_verbose:
    :return:
    """
    if is_verbose:
        arcpy.AddMessage("Removing canals...")
    if arcpy.GetInstallInfo()['Version'][0:4] == '10.5':
        stream_network_no_canals = os.path.join(temp_folder, "NoCanals.shp")
    else:
        stream_network_no_canals = os.path.join('in_memory', 'NoCanals')

    arcpy.Erase_analysis(stream_network, canal, stream_network_no_canals)
    findBraidedReaches(stream_network_no_canals, is_verbose)

    with arcpy.da.UpdateCursor(stream_network_no_canals, "IsMultiCh") as cursor: # delete non-braided reaches
        for row in cursor:
            if row[0] == 0:
                cursor.deleteRow()

    arcpy.MakeFeatureLayer_management(stream_network, "lyrBraidedReaches")
    arcpy.MakeFeatureLayer_management(stream_network_no_canals,"lyrNoCanals")

    arcpy.SelectLayerByLocation_management("lyrBraidedReaches","SHARE_A_LINE_SEGMENT_WITH","lyrNoCanals",'',"NEW_SELECTION")

    arcpy.CalculateField_management("lyrBraidedReaches","IsMultiCh",1,"PYTHON")
    arcpy.CalculateField_management("lyrBraidedReaches","IsMainCh",0,"PYTHON")

    arcpy.Delete_management(stream_network_no_canals)


def findBraidedReaches(fcLines, is_verbose):
    if is_verbose:
        arcpy.AddMessage("Finding streams with mutltiple channels...")
    # Clear temporary data
    if arcpy.Exists("in_memory//DonutPolygons"):
        arcpy.Delete_management("in_memory//DonutPolygons")
    if arcpy.Exists("lyrDonuts"):
        arcpy.Delete_management("lyrDonuts")
    if arcpy.Exists("lyrBraidedReaches"):
        arcpy.Delete_management("lyrBraidedReaches")
        
    # Find donut reaches
    arcpy.FeatureToPolygon_management(fcLines,"in_memory/DonutPolygons")
    arcpy.MakeFeatureLayer_management(fcLines,"lyrBraidedReaches")
    arcpy.MakeFeatureLayer_management("in_memory/DonutPolygons","lyrDonuts")
    arcpy.SelectLayerByLocation_management("lyrBraidedReaches","SHARE_A_LINE_SEGMENT_WITH","lyrDonuts",'',"NEW_SELECTION")
    arcpy.CalculateField_management("lyrBraidedReaches","IsMultiCh",1,"PYTHON")
    arcpy.CalculateField_management("lyrBraidedReaches","IsMainCh",0,"PYTHON")

# # Run as Script # # 
if __name__ == "__main__":

    main(sys.argv[1])