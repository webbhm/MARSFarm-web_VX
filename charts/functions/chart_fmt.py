'''
Formats for defining chart layout and behavior
Author: Howard Webb
Date: 1/7/2023
'''

import sys
#sys.path.append('~/functions')
#print(sys.path)
from functions.MF_Util import *

TITLE='title'
def get_test_fmt(title, group, x_col, y_col):

    fmt = {TITLE:title,
        COLOR: group,
        X_COL:x_col,
        Y_COL:y_col,
        TEMPLATE:"plotly_dark"
        #ERROR:E,
        #ERROR_MINUS:EM,
        #HOVER_DATA:ht
        }
    return fmt

def test():
    print("Test get_test_fmt")
    title = "Test title"
    group = "Trial_Id"
    x_col = "timestamp"
    y_col = "humidity"
    fmt=get_test_fmt(title, group, x_col, y_col)
    print(fmt)
    
if __name__ == '__main__':
    test()