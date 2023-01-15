import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from test_data import get_data
import sys
sys.path.append('../../functions')
from MF_Util import *


title = "Test of Line Chart"

time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
EM = [0, 1, 2.5, 3]
TEMPLATE="template"

ht = {SCHOOL:True,
    GBE_ID: True,
    NAME:True,
    HEIGHT:True}

fmt = {TITLE:title,
    COLOR: 'mf_id',
    X_COL:'day',
    Y_COL:'temp',
    TEMPLATE:"plotly_dark"
    #ERROR:E,
    #ERROR_MINUS:EM,
    #HOVER_DATA:ht
    }

def line_chart(data, fmt):
    print("Line Box")
    print(fmt[TITLE], fmt[X_COL], fmt[Y_COL])
    #df = px.data.tips()
    fig = px.line(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE],
        #error_y = fmt[ERROR_PLUS], error_y_minus = fmt[ERROR_MINUS],
        #hover_data=fmt[HOVER_DATA],
        template=fmt[TEMPLATE])
    return fig


def show(fig):
    fig.show()
    
def save_show(fig, file_name):
    fig.write_html(file_name)  
    fig.show()
        

def test():
    # Test of text function - passes parameters
    title = "Test of Line Chart"
    data = get_data(time, TEMPERATURE)
    print("Data", data)
    print(fmt)
    fig = line_chart(data, fmt)
    show(fig)
    print("Done")
    
if __name__ == '__main__':
    test()
    