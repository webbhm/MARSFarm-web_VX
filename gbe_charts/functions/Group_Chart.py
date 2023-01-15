'''
Experiment Level Charting
This file does the following:
Calls the data query
Data to Pandas Frame
Chart parameters and creation
Does not convert the chart to JSON

Author: Howard Webb
Date: 6/29/2021
'''

from pprint import pprint
import json
from datetime import datetime
import pandas as pd
from functions.GBE_Util import *
from gbe_charts.functions.Group_Query import *
from functions.Ploty_Charts import *



# ------------ GBE Group Charts --------------------

def growth_rate_chart(title, attribute):
    #Bar chart of weekly growth (height) by gbe_id
    print("By Week Growth Chart")
    # Get data
    recs = growth_rate_query(attribute)
    
    # Build data frame
    gbe_id = []
    name = []
    wk = []
    val = []
    v_max = []
    v_min = []
    v_e = []
    v_em = []
    # may not have GBE_Id 
    for doc in recs:
        #print(doc)
        #return
        gbe_id.append(doc["_id"]["GBE_Id"])
        name.append(doc["_id"]["name"])
        wk.append(doc["_id"]["week"])
        avg = doc["avg"]
        mn = doc["min"]
        mx = doc["max"]
        val.append(avg)
        v_max.append(mx)
        v_min.append(mn)
        v_e.append(mx - avg)
        v_em.append(avg - mn)
        data = pd.DataFrame({GBE_ID:gbe_id, NAME:name, WEEK:wk, attribute:val, MIN:v_min, MAX:v_max, ERROR_PLUS:v_e, ERROR_MINUS:v_em})    
    
    group_name = "GBE_Id"
    x_axis_name = "week"
    y_axis_name = attribute
    title = "Change by Week: " + attribute
    ht = {
      GBE_ID: True,
      NAME:True,
      #PLOT:True,
      attribute:True,
      MIN:True,
      MAX:True}
    fmt = {TITLE:title,
            COLOR: WEEK,
            X_COL:GBE_ID,
            Y_COL:attribute,
            HOVER_DATA:ht,
            ERROR_PLUS:ERROR_PLUS,
            ERROR_MINUS:ERROR_MINUS}        
    #return None
    return three_bar_error(data, fmt)
    
def germination_rate_chart():
    # time between planting and germination, with number germinated as bubble

    # get query data
    recs = germination_rate_query()
    
    # build data frame
    gbe_id = []
    name = []
    plot = []
    days_to_germination = []
    germ_avg = []
    germ_max = []
    germ_min = []
    germ_e = []
    germ_em = []
    for rec in recs:
        gbe_id.append(rec["_id"]["GBE_Id"])
        name.append(rec["_id"]["name"])
        #plot.append(rec["_id"]["plot"])
        # days between planting and germination - stored as seconds, divide by 8640 for days
        days = (rec["data"]["Germination"]["timestamp"]-rec["data"]["Planting"]["timestamp"])/86400
        #print("Days", days, round(days, 0))
        days_to_germination.append(round(days, 0))
        germ_avg.append(rec["data"]["Germination"]["avg"])
        germ_e.append(rec["data"]["Germination"]["max"]-rec["data"]["Germination"]["avg"])
        germ_em.append(rec["data"]["Germination"]["avg"]-rec["data"]["Germination"]["min"])
        germ_max.append(rec["data"]["Germination"]["max"])
        germ_min.append(rec["data"]["Germination"]["avg"] - rec["data"]["Germination"]["min"])

    data = pd.DataFrame({GBE_ID:gbe_id, NAME:name, "days":days_to_germination, "avg":germ_avg, MIN:germ_min, MAX:germ_max, ERROR_PLUS:germ_e, ERROR_MINUS:germ_em})    

    # Build Chart
    title = "Days to Germination"
    ht = {
      GBE_ID: True,
      NAME:True,
      #PLOT:True,
      "days":True,
      "avg":True,
      MAX:True,
      MIN:True}
    fmt = {TITLE:title,
            COLOR: GBE_ID,
            X_COL:GBE_ID,
            Y_COL:"days",
            ERROR_PLUS:ERROR_PLUS,
            ERROR_MINUS:ERROR_MINUS,
            HOVER_DATA:ht}
    #print(fmt)
    return scatter_chart_error(data, fmt)
    #return
    #return express_box(data, title, GBE_ID, "days_to_germination")

def score_card_chart():
    # Scorecard of data quality by school
    print("Score Card")
    
    # get query data
    recs = score_card_query()
    
    # build data frame    
    sch = []
    rsn = []
    val = []
    
    for doc in recs:
        #print(doc)
        sch.append(doc["_id"]["school"])
        rsn.append(doc["_id"]["reason"])
        val.append(doc["nbr"])
    data = pd.DataFrame({SCHOOL:sch, "reason":rsn, "count":val})         

    #build chart
    title = "Score Card of All Schools"
    ht = {
      SCHOOL:True,
      "count":True,
      }
    fmt = {TITLE:title,
            COLOR: "reason",
            X_COL:SCHOOL,
            Y_COL:"count",
            Z_COL:None,
            HOVER_DATA:ht,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None,
            "mode":"group"
           }
    #print(fmt)
    return bar_chart(data, fmt)

def health_chart():
    print("Health Chart")
    score = {"good":10, "fair":7, "poor":4, "dead":1}
    group_name = GBE_ID
    
    # get query data
    recs = health_query()

    # build data frame
    gbe_id = []
    name = []
    school = []
    plot = []
    mx = []
    mn = []
    av = []
    
    for doc in recs:
    #    pprint(doc)
    #    continue
        gbe_id.append(doc["_id"]["GBE_Id"])
        min = doc["min"]
        avg = doc["avg"]
        if min == 0:
            avg = 0
        
        mn.append(min)
        mx.append(doc["max"])
        av.append(avg)
        school.append(doc["_id"]["school"])
        name.append(doc["_id"]["name"])
        plot.append(doc["_id"]["plot"])
        #print(data)
    data = pd.DataFrame({"avg":av, "max":mx, "min":mn, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot})         


    #build chart
    title = "Health by School and Plot"
    ht = {SCHOOL:True,
      GBE_ID: True,
      NAME:True,
      PLOT:True,
      "min":True,
      "max":True,
      "avg":True}
    fmt = {TITLE:title,
            COLOR: PLOT,
            X_COL:SCHOOL,
            Y_COL:"avg",
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            HOVER_DATA:ht,
            TEMPLATE:None}        
    #return None
    return bar_chart(data, fmt)

def deaths_by_week():
    # builds data to pass into page
    # this is not a chart
    print("Death by Week")
    
    # get query data
    recs = deaths_by_week_query()
    
    # build data frame
    total_plots = plot_count()
    total_dead = 0
    dead = [0] * 4
    for doc in recs:
        #print(doc)
        week = int(doc["_id"]["week"])
        dead[week-2] = int(doc["count"])
        total_dead += int(doc["count"])
        
    #print("Total Dead", total_dead)
    percent_dead = round(total_plots/total_plots, 2)
    title = "Deaths per Week"    
    data = {"title":title, "total_plots":total_plots, "total_dead":total_dead,
            "percent_dead":percent_dead,
            "week_2":dead[0], "week_3":dead[1], "week_4":dead[2]}
    print(data)
    return data

#--------------------- Charting Style Options -----------------

def box_test_chart(attribute, week):
    # test of box chart

    group_name = "GBE_Id"
    if week not in [2, 3, 4]:
        week = 2
    
    # get query data
    #print("Get box data")
    recs = box_query(attribute, week)
    #print("Got data, build DataFrame")
    # build data frame
    gbe_id = []
    name = []
    value = []
    for doc in recs:
        #print(doc)
        #return
        gbe_id.append("GBE"+str(doc["subject"]["GBE_Id"]))
        name.append(doc["subject"]["type"])
        value.append(doc["subject"]["attribute"]["value"])
    data = pd.DataFrame({GBE_ID:gbe_id, "name":name, attribute:value})
    #print("Got Frame, build chart")
    x_axis_name = "week"
    y_axis_name = attribute

    title = "Attribute by GBE_Id: " + attribute + " week: " + str(week)
    ht = {#SCHOOL:True,
      GBE_ID: True,
      NAME:True,
      #PLOT:True,
      attribute:True}
    fmt = {TITLE:title,
            COLOR: GBE_ID,
            X_COL:GBE_ID,
            Y_COL:attribute,
            HOVER_DATA:ht}     
    print("Return chart", title)
    return box_chart(data, fmt)
   
    

def grouped_bar_test():
    # value change over week
    y_title = "height"
    x_title = "week"
    color = "week"
    name = "name"
    plant = "plant"
        # extract data for plotting as dataframe
    i = [] # identifier
    v = [] # value
    y = [] # y axis
    data = {"plant":["G1", "G1", "G1", "G2", "G2", "G2"], y_title:[10, 15, 20, 15, 20, 25], x_title:[1,2,3, 1, 2, 3], name:["Crispy","Crispy","Crispy","Red","Red","Red"] }
    #for rec in recs:
    #    print(rec)
    #    i.append(rec["_id"]["farm"])
    #    v.append(rec["_id"][x_name])
    #    y.append(rec["attributes"]["Irrigation"])
        
    data = pd.DataFrame.from_dict(data)
    #print(data) 
    p = Plot()
               #data, title, x_title, y_title, color, hover     
    p.group_bar(data, "Height over Week", plant, y_title, color, name)
    
def histogram_chart(attribute, title="None", reduce=1):
       
    # get query data
    recs = histogram_query(attribute)
    
    # build data frame
    max = 100
    count = [0] * (max + 1)
    # rng = range(0, max + 1)
    # array of range values
    rng = range(max + 1)
    r = [n for n in rng]
    #print(count)
    school = []
    for doc in recs:
        #pprint(doc)
        # get bucket value
        val = doc[SUBJECT][ATTRIBUTE][VALUE]
        val = int(round((val/reduce), 0))
        #print("Val", val)
        count[val] += 1
        # Identifiers
        school.append(doc[LOCATION][FARM][NAME])              
    data = pd.DataFrame({COUNT:count, attribute:r})
    
    # build chart
    ht = {attribute:True,
          COUNT:True}
    fmt = {TITLE:title,
            COLOR: None,
            X_COL:attribute,
            Y_COL:COUNT,
            Z_COL:None,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            HOVER_DATA:ht,
            TEMPLATE:None}
    #print(fmt)
    return bar_chart(data, fmt)

def two_var_scatter_chart(var1, var2, title):
    print("Two test", var1, var2)
    group_name = GBE_ID
    
    # get query data
    recs = two_var_scatter_query(var1, var2)
    
    # build data frame
    gbe_id = []
    val1 = []
    val2 = []
    school = []
    name = []
    plot = []
    for doc in recs:
        if var1 in doc["attributes"] and var2 in doc["attributes"]:
            gbe_id.append(doc["_id"]["GBE_Id"])
            val1.append(doc["attributes"][var1])
            val2.append(doc["attributes"][var2])
            school.append(doc["_id"]["school"])
            name.append(doc["_id"]["name"])
            plot.append(doc["_id"]["plot"])
            #print(data)
    data = pd.DataFrame({var1:val1, var2:val2, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot})         

    # build chart
    ht = {SCHOOL:True,
      GBE_ID: True,
      NAME:True,
      PLOT:True,
      var1:True,
      var2:True}
    fmt = {TITLE:title,
            COLOR: GBE_ID,
            X_COL:var1,
            Y_COL:var2,   
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None,           
            HOVER_DATA:ht}        
    #return None
    return scatter_chart(data, fmt)

def environmental_chart(env_var, attr, title):
    print("Environmental", env_var, attr)
    group_name = GBE_ID

    # get query data
    recs = environmental_query(env_var, attr)
    
    # build data frame
    gbe_id = []
    env_val = []
    attr_val = []
    school = []
    name = []
    plot = []
       
    for doc in recs:
        #if var1 in doc["attributes"] and var2 in doc["attributes"]:
        gbe_id.append(doc["subject"]["GBE_Id"])
        school.append(doc["location"]["farm"]["name"])
        attr_val.append(doc["subject"]["attribute"]["value"])
        env_val.append(doc["env"][0]["subject"]["attribute"]["value"])
        name.append(doc["subject"]["type"])
        plot.append(doc["location"]["plot"])
    data = {env_var:env_val, attr:attr_val, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot}         

    # build chart
    ht = {SCHOOL:True,
      GBE_ID: True,
      NAME:True,
      SCHOOL:True,
      PLOT:True,
      env_var:True,
      attr:True}
    fmt = {TITLE:title,
            COLOR: SCHOOL,
            X_COL:env_var,
            Y_COL:attr,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            HOVER_DATA:ht,
            TEMPLATE:None}
    return line_chart(data, fmt)

def full_env_chart(attr, week, title):
    # Get temp and humidity plus variable
    # Use to test scatter bubble and map
    print("Full Env", attr, week)

    # get query data
    recs = group_attribute_query(attr, week)
    print("Got data, build frame")
    # build data frame
    gbe_id = []
    name = []
    school = []
    plot = []
    tmp = []
    humidity = []
    attr_val = []   
    for doc in recs:
        #pprint(doc)
        #print(doc["subject"])
        #continue
        if len(doc["env"]) < 2:
            print(doc)
        else:    
            school.append(doc["location"]["farm"]["name"])
            gbe_id.append(doc["subject"][GBE_ID])
            name.append(doc["subject"]["type"])
            plot.append(doc["location"]["plot"])        
            attr_val.append(doc["subject"]["attribute"]["value"])
            #print("0", doc["env"][0]["subject"]["attribute"]["name"])
            #print("1", doc["env"][1]["subject"]["attribute"]["name"])
            if doc["env"][0]["subject"]["attribute"]["name"] == HUMIDITY:
                humidity.append(doc["env"][0]["subject"]["attribute"]["value"])
                tmp.append(doc["env"][1]["subject"]["attribute"]["value"])
            else:
                humidity.append(doc["env"][1]["subject"]["attribute"]["value"])
                tmp.append(doc["env"][0]["subject"]["attribute"]["value"])
    print("Build env DataFrame")
    data = pd.DataFrame({TEMP:tmp, HUMIDITY:humidity, attr:attr_val, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot})         

    # build chart
    ht = {
      GBE_ID: True,
      NAME:True,
      SCHOOL:True,
      PLOT:True,
      attr:True,
      TEMP:True,
      HUMIDITY:True}
    fmt = {TITLE:title,
            COLOR: GBE_ID,
            X_COL:TEMP,
            Y_COL:HUMIDITY,
            Z_COL:attr,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            TEMPLATE:None,           
            HOVER_DATA:ht}
    print("build Bubble")
    return scatter_bubble(data, fmt)







def plot_count():
    #
    
    # get query data
    recs = plot_count_query()
    
    # build data
    for doc in recs:
        #print( doc)
        pass
    return doc["Count"]

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
    
def design_chart_test():
    title = "Custom Chart"
    #school = "Academir Charter School West"
    attribute = HUMIDITY
    chart_type = "line"
    x_axis = WEEK
    y_axis = attribute
    group = "week"
    error_plus = ERROR_PLUS
    error_minus = ERROR_MINUS
    template = "plotly_dark"
    fig = design_chart_data(title, attribute, chart_type, x_axis, y_axis, group, error_plus, error_minus, template)    
    return fig

if __name__=="__main__":
    #grouped_bar_test()
    #fig = growth_rate_chart("Height Change", HEIGHT)
    #fig = histogram_chart(TEMPERATURE, "Histogram of Temperature")
    #fig = school_by_week(HEIGHT, 'Our Lady of Lourdes Academy')
    #school_by_week(HEIGHT, 'Academir Charter School West').show()
    #fig = school_by_week(HEIGHT, 'Florida Christian School MS')
    #fig = germination_rate()
    #fig = box_test(HEIGHT, 2)
    #fig = box_test(EDIBLE_MASS, 4)
    #get_distinct("location.farm.name")
    
    #get_distinct("activity.id", "test", "Trial")
    #get_distinct("subject.type", DB, COLLECTION)
    #get_distinct({"location.school.name", "location.plot"})
    #find({"subject.GBE_Id":'152'})
    #find({"subject.attribute.name":"Irrigation"})
    #find({"status.status_qualifier":'Success', "subject.attribute.value":0})    
    #find({"status.status_qualifier_reason":"Invalid Data", "subject.attribute.value":{"$not":{"$eq":""}}})
    #find({"status.status_qualifier_reason":"Invalid Data"})
    #find({"subject.attribute.name":"Irrigation"})
    #find({"subject.attribute.name":"Humidity"})    
    #fig = two_var_scatter_chart("height", "edible_mass", "Relation height to mass")
    #fig = two_var_scatter_chart("Irrigation", "edible_mass", "Relation height to mass")
    #environmental("Irrigation", "edible_mass", "Environmental Variable and attribute").show()
    #fig = full_env(HEIGHT, 2, "Height")
    #fig = score_cards()
    #fig = health_chart()
    #fig = deaths_by_week()
    fig = design_chart_test()
    #fig.show()
    #print("Plot Count", plot_count())
    
    print("Finished")