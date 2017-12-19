"""
Import tab-delimited file to separate files for Emme processing
Author: Kevin Saavedra
"""
import sys
import pandas as pd
import numpy as np

def main(filename):
    df = pd.read_csv(filename, sep='\t')
    df = df.dropna(axis=0, how='all')
    headings = list(df)

    for num in range(len(headings)):
        df_temp = df[headings[num]]
        blank_row = pd.Series([""], index=df[headings[num]])
        df_final = df_temp.append(blank_row)
        np.savetxt(headings[num]+'.txt', df_temp.values, fmt='%s', newline='\n')

if __name__ == '__main__':
    main(sys.argv[1])