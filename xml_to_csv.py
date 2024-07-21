import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_csv(xml_file, output_csv):
    namespaces = {'ns': 'http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec'}
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extracting file header information
    file_header = root.find('ns:fileHeader', namespaces)
    if file_header is not None:
        file_format_version = file_header.get('fileFormatVersion', '')
        vendor_name = file_header.get('vendorName', '')
    else:
        file_format_version = ''
        vendor_name = ''

    file_sender_elem = root.find('ns:fileSender', namespaces)
    file_sender = file_sender_elem.get('elementType', '') if file_sender_elem is not None else ''

    meas_collec_elem = root.find('ns:measCollec', namespaces)
    if meas_collec_elem is not None:
        begin_time = meas_collec_elem.get('beginTime', '')
        end_time = meas_collec_elem.get('endTime', '')
    else:
        begin_time = ''
        end_time = ''

    rows = []

    for meas_data in root.findall('ns:measData', namespaces):
        user_label_elem = meas_data.find('ns:managedElement', namespaces)
        user_label = user_label_elem.get('userLabel', '') if user_label_elem is not None else ''

        for meas_info in meas_data.findall('ns:measInfo', namespaces):
            meas_info_id = meas_info.get('measInfoId', '')

            gran_period = meas_info.find('ns:granPeriod', namespaces)
            if gran_period is not None:
                duration = gran_period.get('duration', '')
                end_time = gran_period.get('endTime', '')
            else:
                duration = ''
                end_time = ''

            meas_types_elem = meas_info.find('ns:measTypes', namespaces)
            meas_types = meas_types_elem.text.split() if meas_types_elem is not None else []

            for meas_value in meas_info.findall('ns:measValue', namespaces):
                meas_obj_ldn = meas_value.get('measObjLdn', '')
                meas_results = [r.text for r in meas_value.findall('ns:r', namespaces)]

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
    print(f"Data has been written to {output_csv}")

# Usage
xml_file = "/mnt/data/A20200314.1200+0200-1230+0200_MBTS_06330_VO_BBU0_IERAPETRA_NORTH.xml"
output_csv = "/mnt/data/parsed_flattened.csv"
xml_to_csv(xml_file, output_csv)
