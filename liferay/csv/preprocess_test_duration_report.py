# Script to create test fix ticket based on a given case result
#
# Run with python3 preprecess.py {test-duration-metrics.txt} {test-duration-report.csv}

import pandas as pd
import sys

source = pd.read_csv(sys.argv[1], sep='\t', header=None)
source.columns = ['Test Name', 'Batch Name', 'Time (mins)', 'Result']

df = pd.DataFrame(source, columns=['Test Name', 'Time (mins)', 'Result'])

df1 = df[df['Test Name'].str.strip().str.startswith('LocalFile')].reset_index(drop=True)

df1['Test Name'] = df1['Test Name'].str.replace('LocalFile.','', regex=True)

df1['Time (mins)'] = df1['Time (mins)'].div(60000).round(1)

df1.to_csv(sys.argv[2], index=False)