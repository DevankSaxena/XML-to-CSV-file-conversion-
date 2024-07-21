import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_csv(xml_file, output_csv):
    namespaces = {'ns': 'http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec'}
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extracting file header information
    file_header = root.find('ns:fileHeader', namespaces)
    file_format_version = file_header.get('fileFormatVersion')
    vendor_name = file_header.get('vendorName')
    file_sender = root.find('ns:fileSender', namespaces).get('elementType')
    meas_collec = root.find('ns:measCollec', namespaces)
    begin_time = meas_collec.get('beginTime')
    end_time = meas_collec.get('endTime')

    rows = []

    for meas_data in root.findall('ns:measData', namespaces):
        user_label = meas_data.find('ns:managedElement', namespaces).get('userLabel')
        for meas_info in meas_data.findall('ns:measInfo', namespaces):
            meas_info_id = meas_info.get('measInfoId')
            gran_period = meas_info.find('ns:granPeriod', namespaces)
            duration = gran_period.get('duration')
            end_time = gran_period.get('endTime')
            meas_types = meas_info.find('ns:measTypes', namespaces).text.split()
            for meas_value in meas_info.findall('ns:measValue', namespaces):
                meas_obj_ldn = meas_value.get('measObjLdn')
                meas_results = meas_value.find('ns:measResults', namespaces).text.split()
                row = [
                    vendor_name,
                    file_format_version,
                    xml_file,
                    file_sender,
                    begin_time,
                    end_time,
                    duration,
                    user_label,
                    meas_info_id,
                    meas_obj_ldn,
                    ','.join(meas_types),
                    ','.join(meas_results)
                ]
                rows.append(row)

    columns = [
        'vendorName', 'fileFormatVersion', 'input_filename', 'elementType', 
        'beginTime', 'endTime', 'duration', 'userLabel', 'measInfoId', 
        'measObjLdn', 'measTypes', 'measResults'
    ]
    
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(output_csv, index=False)

# Usage
xml_file = "A20200314.1200+0200-1230+0200_MBTS_06330_VO_BBU0_IERAPETRA_NORTH.xml"
output_csv = "parsed_flattened.csv"
xml_to_csv(xml_file, output_csv)
