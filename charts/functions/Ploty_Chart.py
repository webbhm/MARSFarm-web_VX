'''
Creates charts to display in a web page
Author: Howard Webb
Date: 1/7/2023
'''
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from charts.functions.chart_fmt import get_test_fmt

from charts.functions.test_data import get_test_data
from charts.functions.GBE_Data import env_data
# Global definitions of common terms
from functions.MF_Util import *
import json




time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
EM = [0, 1, 2.5, 3]
TEMPLATE="template"
TITLE="title"

ht = {SCHOOL:True,
    GBE_ID: True,
    NAME:True,
    HEIGHT:True}



def test_chart_fig():
    # create chart fig; for testing or web
    print("Test Line Chart")
    # Dataframe data
    data = get_test_data()
    title="Test Chart (dummy data temp)"
    group = "Trial_Id"
    x_col = "trial_day"
    y_col= "temp"
    #fmt = get_test_fmt(title, group, x_col, y_col)
    # create chart
    fig = px.line(data, x=x_col, y=y_col,
        color=group, title=title,
        #error_y = fmt[ERROR_PLUS], error_y_minus = fmt[ERROR_MINUS],
        #hover_data=fmt[HOVER_DATA],
        template="plotly_dark")
    return fig

def test_chart_json():
    # convert fig to json for web
    fig = test_chart_fig()
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def env_chart_json(attribute, start_date, end_date):
        data = env_data(attribute, start_time=start_date, end_time=end_date )
        x_col = TIME
        y_col = attribute
        title = "Test of Env Charting"
        fig = px.line(data, x=x_col, y=y_col,
        title=title,
        #error_y = fmt[ERROR_PLUS], error_y_minus = fmt[ERROR_MINUS],
        #hover_data=fmt[HOVER_DATA],
        template="plotly_dark")
        jsn = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsn
    
def dew_point_chart(school, start_time, end_time):
    beginning = 6000000000000
    print(" Data", "Start: ", start_time, "End:", end_time)
    data = dew_point_data(start_time, end_time)
    print(data)
    #return data
    title = "Dew Point Chart"
    ht = {
      TIME: True,
      "attribute":True,
      "value": True
      }
    

    fmt = {TITLE:title,
            COLOR: "attribute",
            X_COL:TIME,
            Y_COL:"value",
            HOVER_DATA:ht,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None}
    jsn = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsn 

def show(fig):
    # Test display of chart
    fig.show()
'''    
def save_show(fig, file_name):
    fig.write_html(file_name)  
    fig.show()
  
def get_JSONChart():
    # Convert chart to json for web display
    fig = line_chart(data, fmt)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def get_page_data():
    title = "Test Chart" 
    description = "Temperature sensor data"
    page_data = {"title":title, "description":description,
            "farm":"OpenAgBloom", "trial":"Test_1", "start_date":"12/1/2023", "end_date":"2/12/2023"}
    return page_data   
'''
def test():
    # Test of text function - passes parameters
    title = "Test of Line Chart"
    data = get_test_data()
    print("Data", data)
    title="Test Line Chart"
    group="Trial_Id"
    x_col="trial_day"
    y_col="temp"
    fmt = get_test_fmt(title, group, x_col, y_col)
    print(fmt)
    fig = test_chart_fig(data, fmt)
    show(fig)
    print("Done")
    
if __name__ == '__main__':
    test()
    