import xml.etree.ElementTree as ET
import csv

# Define namespaces
namespaces = {'ns': 'http://latest/nmc-omc/cmNrm.doc#measCollec'}

# Parse XML file
tree = ET.parse('A20200314.1200+0200-1230+0200_MBTS_06330_VO_BBU0_IERAPETRA_NORTH.xml')
root = tree.getroot()

# Extract file header information
file_header = root.find('ns:fileHeader', namespaces)
file_format_version = file_header.get('fileFormatVersion')
vendor_name = file_header.get('vendorName')
file_sender = file_header.find('ns:fileSender', namespaces).get('elementType')
meas_collec_time = file_header.find('ns:measCollec', namespaces).get('beginTime')

# Prepare CSV output
csv_output = 'measData.csv'
csv_columns = ['measInfoId', 'granPeriod_duration', 'granPeriod_endTime', 'repPeriod_duration', 'measObjLdn',
               'measTypes', 'measResults']

with open(csv_output, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_columns)

    for measData in root.findall('ns:measData', namespaces):
        managed_element = measData.find('ns:managedElement', namespaces).get('userLabel')

        for measInfo in measData.findall('ns:measInfo', namespaces):
            measInfoId = measInfo.get('measInfoId')
            granPeriod_duration = measInfo.find('ns:granPeriod', namespaces).get('duration')
            granPeriod_endTime = measInfo.find('ns:granPeriod', namespaces).get('endTime')
            repPeriod_duration = measInfo.find('ns:repPeriod', namespaces).get('duration')
            measTypes = measInfo.find('ns:measTypes', namespaces).text

            for measValue in measInfo.findall('ns:measValue', namespaces):
                measObjLdn = measValue.get('measObjLdn')
                measResults = measValue.find('ns:measResults', namespaces).text

                # Write to CSV
                writer.writerow(
                    [measInfoId, granPeriod_duration, granPeriod_endTime, repPeriod_duration, measObjLdn, measTypes,
                     measResults])

print(f'Data has been written to {csv_output}')
