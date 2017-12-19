"""
Import tab-delimited file to separate files for Emme processing
Author: Kevin Saavedra
"""
import sys
import pandas as pd
import numpy as np

def main(filename):
    df = pd.read_csv(filename, sep='\t')
    df = df.fillna('')
    headings = list(df)
    
    for num in range(len(headings)):
        df_temp = df[headings[num]]
        np.savetxt(headings[num]+'.txt', df_temp.values, fmt='%s', newline='\n')

if __name__ == '__main__':
    main(sys.argv[1])