# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Name: Supporting Functions
# Purpose: A series of useful functions, placed in one spot so they're easier to bug fix
#
# Author: Braden Anderson
# Created on: 7 September 2018
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import os
import arcpy
import uuid


def field_is_in_network(stream_network, field_name):
    fields = [field.name for field in arcpy.ListFields(stream_network)]
    return field_name in fields


def find_folder(folder_location, folder_name):
    """
    If the folder exists, returns it. Otherwise, raises an error
    :param folder_location: Where to look
    :param folder_name: The folder to look for
    :return: Path to folder
    """
    folders = os.listdir(folder_location)
    for folder in folders:
        if folder.endswith(folder_name):
            return os.path.join(folder_location, folder)
    return None


def make_folder(path_to_location, new_folder_name):
    """
    Makes a folder and returns the path to it
    :param path_to_location: Where we want to put the folder
    :param new_folder_name: What the folder will be called
    :return: String
    """
    newFolder = os.path.join(path_to_location, new_folder_name)
    if not os.path.exists(newFolder):
        os.mkdir(newFolder)
    return newFolder


def find_available_num_prefix(folder_root):
    """
    Tells us the next number for a folder in the directory given
    :param folder_root: Where we want to look for a number
    :return: A string, containing a number
    """
    taken_nums = [fileName[0:2] for fileName in os.listdir(folder_root)]
    POSSIBLENUMS = range(1, 100)
    for i in POSSIBLENUMS:
        string_version = str(i)
        if i < 10:
            string_version = '0' + string_version
        if string_version not in taken_nums:
            return string_version
    arcpy.AddWarning("There were too many files at " + folder_root + " to have another folder that fits our naming convention")
    return "100"


def find_available_num_suffix(folder_root):
    """
    Tells us the next number for a folder in the directory given
    :param folder_root: Where we want to look for a number
    :return: A string, containing a number
    """
    taken_nums = [fileName[-2:] for fileName in os.listdir(folder_root)]
    POSSIBLENUMS = range(1, 100)
    for i in POSSIBLENUMS:
        string_version = str(i)
        if i < 10:
            string_version = '0' + string_version
        if string_version not in taken_nums:
            return string_version
    arcpy.AddWarning("There were too many files at " + folder_root + " to have another folder that fits our naming convention")
    return "100"


def make_layer(output_folder, layer_base, new_layer_name, symbology_layer=None, is_raster=False, description="Made Up Description", file_name=None, symbology_field=None):
    """
    Creates a layer and applies a symbology to it
    :param output_folder: Where we want to put the layer
    :param layer_base: What we should base the layer off of
    :param new_layer_name: What the layer should be called
    :param symbology_layer: The symbology that we will import
    :param is_raster: Tells us if it's a raster or not
    :param description: The discription to give to the layer file
    :return: The path to the new layer
    """
    new_layer = new_layer_name
    if file_name is None:
        file_name = new_layer_name.replace(' ', '')
    new_layer_save = os.path.join(output_folder, file_name)
    if not new_layer_save.endswith(".lyr"):
        new_layer_save += ".lyr"

    if is_raster:
        try:
            arcpy.MakeRasterLayer_management(layer_base, new_layer)
        except arcpy.ExecuteError as err:
            if get_execute_error_code(err) == "000873":
                arcpy.AddError(err)
                arcpy.AddMessage("The error above can often be fixed by removing layers or layer packages from the Table of Contents in ArcGIS.")
                raise Exception
            else:
                raise arcpy.ExecuteError(err)

    else:
        arcpy.MakeFeatureLayer_management(layer_base, new_layer)

    if symbology_layer:
        arcpy.ApplySymbologyFromLayer_management(new_layer, symbology_layer)

    if not os.path.exists(new_layer_save):
        arcpy.SaveToLayerFile_management(new_layer, new_layer_save, "RELATIVE")
        new_layer_instance = arcpy.mapping.Layer(new_layer_save)
        new_layer_instance.description = description
        new_layer_instance.save()
    return new_layer_save


def getUUID():
    return str(uuid.uuid4()).upper()


def find_relative_path(path, project_root):
    """
    Looks for the relative path from the project root to the item in the path
    :param path:
    :param project_root:
    :return:
    """
    relative_path = ''
    while path != os.path.dirname(path): # While there are still
        if path == project_root:
            return relative_path
        path, basename = os.path.split(path)

        relative_path = os.path.join(basename, relative_path)
    raise Exception("Could not find relative path")


def get_execute_error_code(err):
    """
    Returns the error code of the given arcpy.ExecuteError error, by looking at the string of the error
    :param err:
    :return:
    """
    return err[0][6:12]


def write_xml_element_with_path(xml_file, base_element, xml_element_name, item_name, path, project_root, xml_id=None):
    """

    :param xml_file:
    :param base_element:
    :param xml_element_name:
    :param xml_id:
    :param item_name:
    :param path:
    :param project_root:
    :return:
    """
    if xml_id is None:
        new_element = xml_file.add_sub_element(base_element, xml_element_name, tags=[("guid", getUUID())])
    else:
        new_element = xml_file.add_sub_element(base_element, xml_element_name, tags=[("guid", getUUID()), ("id", xml_id)])

    xml_file.add_sub_element(new_element, "Name", item_name)
    relative_path = find_relative_path(path, project_root)
    xml_file.add_sub_element(new_element, "Path", relative_path)
