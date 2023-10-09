import pandas as pd
import scipy as sp
import os


def execute_analize():
    headers = ['year', 'day', 'hour', 'B_scalar','Bz_GSM','Bz_GSE','SW_temperature', 'SW_proton_density','Plasma_Speed','Flow_pressure']
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute file path
    doc = os.path.join(current_directory, 'data1.txt')
    df = pd.read_csv(doc , delim_whitespace=' ',names=headers)
    #Found max values for each column
    df.max()
    #Create list with max values of each column
    max_values = [9999, 999, 99, 99, 99, 99, 9999999.00, 999.90, 9999.00, 99.99]
    # Remove rows with missing values
    df_raw = df[(df != max_values).all(axis=1)]

    # reset index
    df_raw = df_raw.reset_index(drop=True)

    data_to_find = df_raw['Bz_GSM']

    peaks = sp.signal.find_peaks(data_to_find, height=3.88, distance=20)
    print(len(peaks[0]))

    return {"time":peaks[0].tolist(), 'DataFrame':data_to_find.to_dict()}

execute_analize()