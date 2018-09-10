import sys
import pandas as pd
import numpy as np
import os.path
from os import path
from decimal import Decimal
from collections import defaultdict

#read txt file
def read_txt(filename):
    file = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) != 0:
                file.append(line)
        df = pd.DataFrame(file)
    return df

#split columns of txt file
def split_column(df):
    df = df[0].str.split('|', expand = True)
    df.columns = ['time', 'stock', 'price']
    return df

#write error message
def write_error(txt, file):
    text_file = open(file, "w")
    text_file.write(txt)
    text_file.close()

#calculate error between actual and predicted price of stocks
def compare_stock(argv):
    if len(argv) != 5:
        print('Number of arguments is incorrect:' + str(len(argv)))
        return

    comparisonFile = argv[4]

    for file in argv[1:4] :
        if not path.exists(file):
            write_error(file + ' does not exist.', comparisonFile)
            return

    windowFile = argv[1]
    actualFile = argv[2]
    predictionFile = argv[3]
    comparisonFile = argv[4]

    #check if no data in files
    df = read_txt(actualFile)
    if len(df) == 0:
        write_error('No data in the actual file.', comparisonFile)
        return
    actual = split_column(df)

    df = read_txt(predictionFile)
    if len(df) == 0:
        write_error('No data in the prediction file.', comparisonFile)
        return
    predicted = split_column(df)

    #check if window size is null, 0 or negative
    df = read_txt(windowFile)
    if len(df) == 0:
        write_error('No window size is specified.', comparisonFile)
        return
    window = int(df[0][0])
    if window <= 0:
        write_error('Window size is negative or defined as 0, no result will be output.', comparisonFile)
        return

    #calculate error between actual and predicted price of matched stocks
    data = pd.merge(actual, predicted, on = ['time','stock'], how = 'inner')
    cols = data.columns.drop('stock')
    data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')
    data['price_error'] = abs(data['price_x'] - data['price_y'])

    #calculated sum and count of errors group by matched stocks
    act_pred = data.groupby(['time'], as_index = False).sum()
    act_pred['count'] = data.groupby(['time'], as_index = False).count()['price_error']

    #check if window size is larger than maximun of matched hours
    max_hour = actual['time'].astype(int).max()
    if window > max_hour:
        write_error('Window size is out of index, no result will be output.', comparisonFile)
        return

    #calculated average error of each time window
    avg_error = defaultdict(list)
    start_index = 0
    for i in range(1, max_hour - window + 2):
        while (start_index < len(act_pred) and act_pred['time'][start_index] < i):
            start_index += 1
        error_sum = 0
        cnt = 0
        for j in range(start_index, start_index + window):
            if j >= len(act_pred):
                break
            if act_pred['time'][j] >= i + window:
                break
            error_sum += act_pred['price_error'][j]
            cnt += act_pred['count'][j]
        if cnt == 0:
            error_avg = 'NA'
        else:
            error_avg = error_sum/cnt
            if error_avg == 0.0:
                error_avg = str(Decimal('0.00'))
            else:
                error_avg = '%.2f' % error_avg
        avg_error[i-1] = [i, i + window - 1, error_sum, cnt, error_avg]

    avg_error = pd.DataFrame.from_dict(avg_error, orient = "index")
    comparison = avg_error[0].astype(str)+'|'+ avg_error[1].astype(str)+'|'+avg_error[4]
    comparison.to_csv(comparisonFile, header = None, index = None)

# call main function
if __name__ == "__main__":
    compare_stock(sys.argv)
