'''
Build pandas frames for charts
Strip array of json documents (already pivoted) into data arrays
Then save as pandas frame
Author: Howard Webb
Date: 1/7/2023
'''
from pandas import DataFrame
# dummy data for testing
struct={'group':{'name':'Trial_Id', 'label':'Trial_Id'},
        'x_col':{'name':'trial_day', 'label':'Day'},
        'y_col':{'name':'temp', 'label':'Temperature'}}

data=[{'Trial_Id':123, 'trial_day':1, 'temp':26},
      {'Trial_Id':123, 'trial_day':2, 'temp':21},
      {'Trial_Id':123, 'trial_day':3, 'temp':25},
      {'Trial_Id':456, 'trial_day':1, 'temp':22},
      {'Trial_Id':456, 'trial_day':2, 'temp':27},
      {'Trial_Id':456, 'trial_day':3, 'temp':24},
      ]

def three_column_frame(data_array, structure):
    # Build pandas frame from array of json data and structure def of data (also json)
    # X,Y columns and group
    # Build arrays
    gp = []
    x_col = []
    y_col = []
    for x in range(len(data_array)):
        #print(start_time, doc[TIME][TIMESTAMP], end_time)
        #print(data_array[x][structure['group']['name']])
        gp.append(data_array[x][structure['group']['name']])
        x_col.append(data_array[x][structure['x_col']['name']])
        y_col.append(data_array[x][structure['y_col']['name']])
    # convert to pandas
    return DataFrame({structure['group']['label']:gp,structure['x_col']['label']:x_col, structure['y_col']['label']:y_col})

def test():
    print("Test of data frame creation")
    frm = three_column_frame(data, struct)
    print(frm)

if __name__=='__main__':
    test()