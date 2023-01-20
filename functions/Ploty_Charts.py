import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from functions.GBE_Util import *

import random
from numpy import *

# Test data
BAR_DATA = {GBE_ID:["A", "A", "A", "B", "B", "B", "C", "C", "C"], HEIGHT:[10, 15, 20, 15, 20, 25, 20, 25, 30], WEEK:[1, 2, 3, 1, 2, 3, 1, 2, 3], NAME:["Aa", "Ab", "Ac", "Ba", "Bb", "Bc", "Ca", "Cb", "Cc"]}
G = ["151", "152", "155", "157"]
H =[1, 2, 3, 4]
M = [1, 2, 3, 4]
EM = [0, 1, 2.5, 3]
E = [2, 4, 3.5, 6]
N = ["Alpha", "Beta", "Gama", "Delta"]
V = ["Outrageous", "Butter Crunch", "Crispy Red", "Leafy Green"]
S = ["Little Red", "Kinder", "High", "Pattern"]
SCATTER_DATA = {GBE_ID:G, HEIGHT: H, ERROR:E, ERROR_MINUS:EM, EDIBLE_MASS: M, NAME: N, SCHOOL:S}

Y = BAR_DATA[HEIGHT]
X = BAR_DATA[GBE_ID]
H= BAR_DATA[NAME]
C = X
DIR = "C:\\Users\\WebbH\\Documents\\GBE\\" 

def group_bar_test():
    # minimum grouped bar graph - average
    print("Minimum Group  Bar Test")
    title = "Group Bar Test"
    i_title = "GBE_Id"
    x_title = "week"
    y_title = "height"
    color = x_title
    hover = "hover"
    
    print(len(data[i_title]), len(data[x_title]), len(data[y_title]))
    #df = pd.DataFrame.from_dict(BAR_DATA)
    print("Title:", title)
    print("Hover:", hover)
    print("Color:", color)
    print("X_Title:", x_title)
    print("Y_Title:", y_title)

    fig = px.histogram(BAR_DATA, x=i_title, y=y_title,
        color=color, barmode='group', title=title,
        histfunc="avg")
    
    fig.show()
    print("Done")
    
def bar_text():
    # Example bar with custom text
    print("Custom Text Bar")
    x = ['Product A', 'Product B', 'Product C']
    y = [20, 14, 23]
    h = ['27% market share', '24% market share', '19% market share']

    # Use the hovertext kw argument for hover text
    fig = go.Figure(data=[go.Bar(x=x, y=y,
            hovertext=h)])
    # Customize aspect
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='January 2013 Sales Report')
    fig.show()
    
def bar_text2():
    # Example bar with custom text
    # Following says hover_name does not work
    #https://towardsdatascience.com/histograms-with-plotly-express-complete-guide-d483656c5ad7#d978
    
    print("Custom Text Bar 2")
    title="Bar Test Two"

    fig = px.histogram(BAR_DATA, x=GBE_ID, y=HEIGHT,
                       color=WEEK, barmode="group",
                       title=title,
                       histfunc='avg',
                       labels={NAME:NAME})
    fig.show()
       
    print("Done")
    
def bar_text3():
    # Example bar with custom text
    print("Custom Text Bar Three")
    y = BAR_DATA[HEIGHT]
    x = BAR_DATA[GBE_ID]
    h = BAR_DATA[NAME]

    # Use the hovertext kw argument for hover text
    fig = go.Figure(data=[go.Histogram(x=x, y=y,
            hovertext=h)])
    # Customize aspect
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='Bar Custom Text')
    fig.show()

def bar_confidence():
    #print("Avg Growth Rate with Min/Max")
    gbe_id = ["A", "B", "C"]
    w1 = [10, 15, 20]
    w1e = [1, 0.5, 1.5]
    w2 = [15, 20, 25]
    w2e = [0.7, 0.3, 1.2]
    w3 = [20, 25, 30]
    w3e = [2.4, 0.9, 1.3]
    ht = ["Outrageous", "Butter Crunch", "Crispy Red", "Leafy Green"]
    title = "Avg Growth Rate with Min/Max"
    trace_1_name = "Week 1"
    trace_2_name = "Week 2"
    trace_3_name = "Week 3"
    x_title = "GBE_Id"
    y_title = "Height"
    #template = '%{hovertext}</br></br>Plant:%{x}</br>Height: %{y}'
    template = '%{hovertext}<br>Plant: %{x}<br>Height: %{y}<extra></extra>'
    file_name = DIR + "bar_conf.html" 
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=trace_1_name,
        x=gbe_id, y=w1,
        error_y=dict(type='data', array=w1e),
    ))
    fig.add_trace(go.Bar(
        name=trace_2_name,
        x=gbe_id, y=w2,
        error_y=dict(type='data', array=w2e)
    ))
    fig.add_trace(go.Bar(
        name=trace_3_name,
        x=gbe_id, y=w3,
        error_y=dict(type='data', array=w3e)
    ))
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)

    fig.update_traces(hoverinfo="text", hovertext=HT,
        hovertemplate=template)
    fig.update_layout(barmode='group',
        title=title)
        #lables=dict(x="GBE_Id", y="Height"))
    #print(fig)
    return fig
    fig.show()
    fig.write_html(file_name)    
    print("Done")
    
def bar_confidence2(title, gbe_id, ht, wk1, wk1e, wk2, wk2e, wk3, wk3e):
    print("Avg Growth Rate with Min/Max")
    ht = ["Outrageous", "Butter Crunch", "Crispy Red", "Leafy Green"]
    #title = "Avg Growth Rate with Min/Max"
    trace_1_name = "Week 2"
    trace_2_name = "Week 3"
    trace_3_name = "Week 4"
    x_title = "GBE_Id"
    y_title = "Height"
    #template = '%{hovertext}</br></br>Plant:%{x}</br>Height: %{y}'
    template = '%{hovertext}<br>Plant: %{x}<br>Height: %{y}<extra></extra>'
    file_name = DIR + "bar_" + title + ".html" 
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=trace_1_name,
        x=gbe_id, y=wk1,
        error_y=dict(type='data', array=wk1e),
    ))
    fig.add_trace(go.Bar(
        name=trace_2_name,
        x=gbe_id, y=wk2,
        error_y=dict(type='data', array=wk2e)
    ))
    fig.add_trace(go.Bar(
        name=trace_3_name,
        x=gbe_id, y=wk3,
        error_y=dict(type='data', array=wk3e)
    ))
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)

    fig.update_traces(hoverinfo="text", hovertext=ht,
        hovertemplate=template)
    fig.update_layout(barmode='group',
        title=title)
        #lables=dict(x="GBE_Id", y="Height"))
    #print(fig)
    return fig
    fig.show()
    fig.write_html(file_name)    
    print("Done")
    

def two_variable_scatter(data, var1, var2, color, hover, title):
    # minimum scatter plot test
    print("Minimum Scatter Plot Test")
    #HEIGHT = "height"
    #MASS = "mass"
    template = hover + ':%{hovertext}<br>' + var1 + ': %{y}<br>' + var2 + ': %{x}<extra></extra>'
    #template = 'GBE_Id=D<br>mass=%{x}<br>height=%{y}<extra></extra>'    
    #df = pd.DataFrame.from_dict(data)
    
    fig = px.scatter(data, x=var1, y=var2, color=color)
    
    fig.update_traces(hoverinfo="text", hovertext=data[hover],
        hovertemplate=template)
    return fig
    fig.show()
    print(fig)
    print("Done")
    
def hist_text():
    print("Histogram Text Copy")
    title="Bar Test Two"
    y = BAR_DATA[HEIGHT]
    x = BAR_DATA[GBE_ID]
    h = BAR_DATA[NAME]
    
    df = px.data.tips()
    fig = px.histogram(BAR_DATA, x=GBE_ID, y=HEIGHT,
                   color=WEEK, barmode="group",                       
                   title='Hist Text Test',
                   #labels={GBE_ID:NAME}, # can specify one label per df column
                   
                   hover_data={NAME:True,
                               GBE_ID: True}  #opacity=0.8,
                   #log_y=True, # represent bars with log scale
                   #color_discrete_sequence=['indianred'], # color of histogram bars
                   )
    fig.show()    
    print("Done")
    
def pie_text():
    # Modified example with custom hovertext
    print("Pie with custom text")
    fig = go.Figure(go.Pie(
    name = "",
    values = [2, 5, 3, 2.5],
    labels = ["R", "Python", "Java Script", "Matlab"],
    text = ["Alpha", "Beta", "Gama", "Delta"],
    #name = ["Alpha", "Beta", "Gama", "Delta"],
    textinfo = "label",    
    hoverinfo = "text",
    hovertemplate = "%{text}: </br> </br>Value: %{value}",
    title = "Crazy Testing"
))
  
    fig.show()
    print("Done")
    
def express_box(data, title, x_name, y_name):
    print("Express Box")
    print(title, x_name, y_name)
    #df = px.data.tips()
    fig = px.box(data, x=x_name, y=y_name)
    
    #fig.update_traces(hoverinfo="name", hovertext="name", title=title, color="GBE_Id")    
    fig.update_layout(title_text=title)
    #print(df)
    return fig
    file_name = DIR + "box_" + y_name + ".html"    
    fig.write_html(file_name)          
        
def show(fig):
    fig.show()
    
def save_show(fig, file_name):
    fig.write_html(file_name)  
    fig.show()
        
def bar_chart(data, fmt):
    # Example bar with custom text
    print("Custom Text Bar")
    if "bar_type" in fmt:
        mode = fmt["mode"]
    else:
        mode = None
         
    fig = px.bar(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE], barmode=mode, hover_data=fmt[HOVER_DATA])
    return fig

def three_bar_error(data, fmt):
    # Example bar with custom text
    # Likely will become the standard bar chart routine
    # Used by: Growth_Rate, School by Week (no error data)
    print("Three Bar Error")
    #print(fmt[ERROR])
    
    fig = px.bar(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE],  hover_data=fmt[HOVER_DATA],    
        error_y=fmt[ERROR_PLUS], error_y_minus=fmt[ERROR_MINUS],
        barmode = 'group', template="seaborn")
    #print(wk_3)
    return fig


def scatter_chart_error(data, fmt):
    # Example bar with custom text
    print("Custom Text Bar")
    print(fmt[ERROR_PLUS], fmt[ERROR_MINUS])
    
    fig = px.scatter(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE], hover_data=fmt[HOVER_DATA],    
        error_y=fmt[ERROR_PLUS], error_y_minus=fmt[ERROR_MINUS])

    return fig


def scatter_bubble(data, fmt):
    fig = px.scatter(data, x=fmt[X_COL], y=fmt[Y_COL],
             size=fmt[Z_COL], color=fmt[COLOR],
                 hover_data=fmt[HOVER_DATA])
    return fig

def box_chart(data, fmt):
    print("Express Box")
    print(fmt[TITLE], fmt[X_COL], fmt[Y_COL])
    #df = px.data.tips()
    fig = px.box(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE],
        hover_data=fmt[HOVER_DATA], template="plotly_dark")
    return fig

def line_chart(data, fmt):
    print("Line Box")
    print(fmt[TITLE], fmt[X_COL], fmt[Y_COL])
    #df = px.data.tips()
    fig = px.line(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE],
        error_y = fmt[ERROR_PLUS], error_y_minus = fmt[ERROR_MINUS],
        hover_data=fmt[HOVER_DATA], template=fmt[TEMPLATE])
    return fig

def bar_chart(data, fmt):
    # Example bar with custom text
    print("Bar Chart")
   
    fig = px.bar(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE],  hover_data=fmt[HOVER_DATA],    
        error_y=fmt[ERROR_PLUS], error_y_minus=fmt[ERROR_MINUS], barmode = 'group', template=fmt[TEMPLATE])
    #print(wk_3)
    return fig

def scatter_chart(data, fmt):
    # Example bar with custom text
    print("Scatter Chart")
    
    fig = px.scatter(data, x=fmt[X_COL], y=fmt[Y_COL],
        color=fmt[COLOR], title=fmt[TITLE], hover_data=fmt[HOVER_DATA],    
        error_y=fmt[ERROR_PLUS], error_y_minus=fmt[ERROR_MINUS],
        template=fmt[TEMPLATE])

    return fig

def design_chart_data(title, attribute, chart_type, x_axis, y_axis, group, error_plus, error_minus, template):
    # Design your own chart using school/attibute data
    data = growth_rate_data(attribute)
    #print(data)
    if attribute in [TEMPERATURE, HUMIDITY]:
        ht = {WEEK:True,
          attribute:True,
          MIN:True,
          MAX:True}
    else:
        ht = {
          GBE_ID:True,
          NAME:True,
          WEEK:True,
          attribute:True,
          MIN:True,
          MAX:True}
        
    fmt = {TITLE:title,
            COLOR: group,
            X_COL:x_axis,
            Y_COL:y_axis,
            HOVER_DATA:ht,
            ERROR_PLUS:error_plus,
            ERROR_MINUS:error_minus,
            TEMPLATE:template}
    if chart_type == "line":
        return line_chart(data, fmt)
    elif chart_type == "bar":
        return bar_chart(data, fmt)
    elif chart_type == "scatter":
        return scatter_chart(data, fmt)
    #return None


def test_test():
    # Test of text function - passes parameters
    title = "Test of Test Bar"
    ht = {SCHOOL:True,
      GBE_ID: True,
      NAME:True,
      HEIGHT:True}
    fmt = {TITLE:title,
            COLOR: GBE_ID,
            X_COL:GBE_ID,
            Y_COL:HEIGHT,
            ERROR:E,
            ERROR_MINUS:EM,
            HOVER_DATA:ht}
    #print(fmt)
    fig = bar_chart(SCATTER_DATA, None, None, fmt)
    show(fig)
    print("Done")
    
if __name__ == '__main__':
    #scatter_test()
    #group_bar_test()
    #bar_text()
    #pie_text()
    #bar_text2()
    #hist_text()
    #bar_confidence()
    #fig = box_chart()
    #fig = two_variable_scatter(SCATTER_DATA, 'height', 'mass', "GBE_Id", "name", "title")
    test_test()
    #show(fig)
    