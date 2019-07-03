import sys
import arcpy


def main(ds, ds_out):
    data_name = ds

    # Copy to data store
    input_layer = "https://gpportal.esri.com/server/rest/services/DataStoreCatalogs/bigDataFileShares_pyTest/" \
                  "BigDataCatalogServer/{}".format(data_name)
    output_name = ds + '_gapro'
    ds_data = arcpy.geoanalytics.CopyToDataStore(input_layer, output_name, "RELATIONAL_DATA_STORE")

    # Copy to fgdb
    out_gdb = r"C:\Users\kev10076\Documents\ArcGIS\Projects\REST_migration\REST_migration.gdb"
    out_gdb_name = output_name + '_gdb'
    fgdb_data = arcpy.conversion.FeatureClassToFeatureClass(ds_data, out_gdb, out_gdb_name)

    # Convert time field
    input_time_field = 'instant_datetime'
    input_time_format = "'Not Used'"
    output_time_field = 'date_gapro'
    output_time_type = 'TEXT'
    output_time_format = "yyyy/MM/dd HH:mm:ss"
    time_fgdb_data = arcpy.management.ConvertTimeField(fgdb_data, input_time_field, input_time_format, output_time_field,
                                                       output_time_type, output_time_format)

    # Save to shp
    out_shp = ds_out + '.shp'
    out_folder = r"C:\Users\kev10076\Documents\ArcGIS\Projects\REST_migration\Output"
    arcpy.conversion.FeatureClassToFeatureClass(time_fgdb_data, out_folder, out_shp)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])