import pandas as pd
import os

def split_csv_by_measinfoid(input_csv, output_dir):
    df = pd.read_csv(input_csv)
    measinfoids = df['measInfoId'].unique()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for measinfoid in measinfoids:
        subset_df = df[df['measInfoId'] == measinfoid]
        subset_df.to_csv(f"{output_dir}/measinfoid_{measinfoid}.csv", index=False)

# Usage
input_csv = "/mnt/data/parsed_flattened.csv"
output_dir = "/mnt/data/split_csv_files"
split_csv_by_measinfoid(input_csv, output_dir)
