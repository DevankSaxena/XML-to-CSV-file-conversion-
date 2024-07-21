import csv
import os

input_csv = 'measData.csv'
output_dir = 'output_csvs'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the input CSV file
with open(input_csv, mode='r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    header = reader.fieldnames

# Group rows by measInfoId
grouped_rows = {}
for row in rows:
    meas_info_id = row['measInfoId']
    if meas_info_id not in grouped_rows:
        grouped_rows[meas_info_id] = []
    grouped_rows[meas_info_id].append(row)

# Write each group to a separate CSV file
for meas_info_id, group in grouped_rows.items():
    output_csv = os.path.join(output_dir, f'measData_{meas_info_id}.csv')
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(group)
    print(f'Data has been written to {output_csv}')

print('All files have been split and saved.')
