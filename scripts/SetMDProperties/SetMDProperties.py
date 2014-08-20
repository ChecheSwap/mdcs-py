#------------------------------------------------------------------------------
# Copyright 2013 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#------------------------------------------------------------------------------
# Name: SetMDProperties.py
# Description: To set mosaic dataset properties
# Version: 20140417
# Requirements: ArcGIS 10.1 SP1
# Author: Esri Imagery Workflows team
#------------------------------------------------------------------------------
#!/usr/bin/env python


import arcpy,os,sys
from xml.dom import minidom
import Base

class SetMDProperties(Base.Base):

    dic_properties_lst = {}
    dicMDs = {}

    def __init__(self, base):
        self.setLog(base.m_log)

        self.m_base = base


    def is101SP1(self): # if python version is >= 3, it's asssumed we're being run from ArcGIS Pro
        return self.CheckMDCSVersion([10, 1, 0, 0] if (sys.version_info[0] < 3) else [1, 0, 0, 0], [0, 0, 0, 0])       # ver [major, minor, revision, build]


    def getInternalPropValue(self, md, key):
        if (key in self.dic_properties_lst.keys()):
            return self.dic_properties_lst[key]
        else:
            return ''

    # Step (12) - Configure MD properties.
    def setMDProperties(self, mdPath):

        mdName = os.path.basename(mdPath).upper()
        noRasterPerMosaic = self.getInternalPropValue(mdName, 'max_num_per_mosaic')    #"50"
        maxRequestSizex = self.getInternalPropValue(mdName, 'rows_maximum_imagesize')  #"4000"
        maxRequestSizey = self.getInternalPropValue(mdName, 'columns_maximum_imagesize')  #"4000"
        allowedCompression = self.getInternalPropValue(mdName, 'allowed_compressions')    #"LZ77;NONE;JPEG;LERC"
        defaultCompression = self.getInternalPropValue(mdName,'default_compression_type') #"None"
        compressionQuality = self.getInternalPropValue(mdName,'JPEG_quality') #"75"
        clipToFootprint = self.getInternalPropValue(mdName,'clip_to_footprints')   #"NOT_CLIP"
        allowedFields = self.getInternalPropValue(mdName,'transmission_fields')   #"Name;MinPS;MaxPS;LowPS;HighPS;ProductName;BEST;Source;LE90;CE90;Date_Start;Date_End;Source_URL;DEM_Type;Dataset_ID;VerticalDatum"
        LERC_Tolerance = self.getInternalPropValue(mdName,'LERC_Tolerance')#"0.01"
        resampling_type = self.getInternalPropValue(mdName,'resampling_type')
        clip_to_boundary = self.getInternalPropValue(mdName,'clip_to_boundary')
        color_correction = self.getInternalPropValue(mdName,'color_correction')
        footprints_may_contain_nodata = self.getInternalPropValue(mdName,'footprints_may_contain_nodata')
        allowed_mensuration_capabilities = self.getInternalPropValue(mdName,'allowed_mensuration_capabilities')
        default_mensuration_capabilities = self.getInternalPropValue(mdName,'default_mensuration_capabilities')
        allowed_mosaic_methods = self.getInternalPropValue(mdName,'allowed_mosaic_methods')
        defaultMosaicMethod = self.getInternalPropValue(mdName, 'default_mosaic_method')
        orderField = self.getInternalPropValue(mdName, 'Order_field')
        order_base = self.getInternalPropValue(mdName,'order_base')
        sorting_order = self.getInternalPropValue(mdName,'sorting_order')
        mosaic_operator = self.getInternalPropValue(mdName,'mosaic_operator')
        blend_width = self.getInternalPropValue(mdName, 'blend_width')
        view_point_x = self.getInternalPropValue(mdName, 'view_point_x')
        view_point_y = self.getInternalPropValue(mdName,'view_point_y')
        cell_size_tolerance = self.getInternalPropValue(mdName,'cell_size_tolerance')
        cell_size = self.getInternalPropValue(mdName, 'cell_size')
        metadata_level = self.getInternalPropValue(mdName, 'metadata_level')
        use_time = self.getInternalPropValue(mdName,'use_time')
        start_time_field = self.getInternalPropValue(mdName,'start_time_field')
        end_time_field = self.getInternalPropValue(mdName,'end_time_field')
        time_format = self.getInternalPropValue(mdName, 'time_format')
        geographic_transform = self.getInternalPropValue(mdName,'geographic_transform')
        max_num_of_download_items = self.getInternalPropValue(mdName, 'max_num_of_download_items')
        max_num_of_records_returned = self.getInternalPropValue(mdName,'max_num_of_records_returned')


        if (self.is101SP1() == False):  #OrderField set to 'BEST' would fail in 10.1 without SP1
            orderField = 'MinPS'

        try:
            self.log("\t\tSetting MD Properties", self.const_general_text)
            arcpy.SetMosaicDatasetProperties_management(
            mdPath,
            maxRequestSizex,
            maxRequestSizey,
            allowedCompression,
            defaultCompression,
            compressionQuality,
            LERC_Tolerance,
            resampling_type,
            clipToFootprint,
            footprints_may_contain_nodata,
            clip_to_boundary,
            color_correction,
            allowed_mensuration_capabilities,
            default_mensuration_capabilities,
            allowed_mosaic_methods,
            defaultMosaicMethod,
            orderField,
            order_base,
            sorting_order,
            mosaic_operator,
            blend_width,
            view_point_x,
            view_point_y,
            noRasterPerMosaic,
            cell_size_tolerance,
            cell_size,
            metadata_level,
            allowedFields,
            use_time,
            start_time_field,
            end_time_field,
            time_format,
            geographic_transform,
            max_num_of_download_items,
            max_num_of_records_returned
            )
            self.log("\t\tDone setting mosaic dataset properties for : " + mdName, self.const_general_text)
            return True

        except:
            self.log("Failed to set mosaic dataset properties.", self.const_critical_text)
            self.log(arcpy.GetMessages(), self.const_critical_text)

        return False


    def init(self, config):

        Nodelist = self.m_base.m_doc.getElementsByTagName("MosaicDataset")
        if (Nodelist.length == 0):
            self.log("Error: MosaicDataset node not found! Invalid schema.", self.const_critical_text)
            return False

        try:
            for node in Nodelist[0].childNodes:
                  node =  node.nextSibling
                  if (node != None and node.nodeType == minidom.Node.ELEMENT_NODE):
                        if (node.nodeName == 'DefaultProperties'):
                            for node in node.childNodes:
                                if (node.nodeType == minidom.Node.ELEMENT_NODE):
                                    self.dic_properties_lst[node.nodeName] = node.firstChild.nodeValue

        except:
            Error = True

        return True