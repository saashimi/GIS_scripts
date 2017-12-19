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
    df0 = df[headings[0]]
    print df0.values

    """
    with open(headings[0], 'a') as write_file:
        np.savetxt(headings[0], df0.values, newline='\n')
    write_file.close()
    """
    """
    #for heading in headings: #TODO LOOP OVER EVERY HEADING
    
    #with open(headings[0], 'a') as write_file:
        #iterate over rows:
    for row in df.iterrows():
        #write_file.write(row[df[headings[0]]])
        print row[df[headings[0]]]

    #write_file.close()

        #Extract the column heading as the text file name
        #For every row in column:
        	# write to new line in text file.
    """

if __name__ == '__main__':
    main(sys.argv[1])