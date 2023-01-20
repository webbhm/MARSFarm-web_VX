'''
Demo of Ploty reports

Author: Howard Webb
Date: 6/29/2021
'''


from pprint import pprint
import json
from datetime import datetime

#from Plot import Plot
import pandas as pd
from functions.GBE_Util import *
from functions.Mongo_Util import MongoUtil
from functions.Ploty_Charts import *



# Source directories for data files, not used here

DB = "gbe"
COLLECTION = "2020"

   
def find(query):
    print("Find", query)
    mu = MongoUtil(DB)
    docs = mu.find(DB, COLLECTION, query)
    dump(docs)
        
def get_distinct(item, db=DB, col=COLLECTION):
    # get distinct list of items
    print("Distinct", item, db, col)
    mu = MongoUtil(db)
    docs = mu.distinct(db, col, item)
    #print("Doc", type(docs), docs)
    data = []
    for doc in docs:
    #    print(doc)
        data.append(doc)
    #print(data)    
    print("Done")
    
def growth_rate_chart(title, attribute):
    #Bar chart of weekly growth (height) by gbe_id
    print("By Week Growth Chart")
    group_name = "GBE_Id"
    x_axis_name = "week"
    y_axis_name = attribute
    title = "Change by Week: " + attribute
    data = growth_rate_data(attribute)
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
    
def growth_rate_data(attribute):    
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "subject.attribute.value":{"$ne":0}           
            }}
    gbe_flag = True
    #print(attribute, TEMPERATURE, HUMIDITY, attribute in [TEMPERATURE, HUMIDITY])
    if attribute in [TEMPERATURE, HUMIDITY]:
        # Environmental observations don't have gbe_id
        gbe_flag = False
    #print("GBE Flag", gbe_flag)
    if gbe_flag:
        #Group by GBE_Id and week, get avg, min, max
        group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                       "name":"$subject.type",
                       "week":{"$toString":"$time.week"}},
                        #"name":{"$first":"$subject.type"},   
                        "avg":{"$avg":"$subject.attribute.value"},
                        "min":{"$min":"$subject.attribute.value"},
                        "max":{"$max":"$subject.attribute.value"}
                           }
                       }
        sort = {"$sort":{"_id.GBE_Id":1, "_id.week":1}}
    else:
        group = {"$group":{"_id":{WEEK:{"$toString":"$time.week"}},
                        #"name":{"$first":"$subject.type"},   
                        "avg":{"$avg":"$subject.attribute.value"},
                        "min":{"$min":"$subject.attribute.value"},
                        "max":{"$max":"$subject.attribute.value"}
                           }
                       }
        sort = {"$sort":{"_id.week":1}}
    
    #q = [match]
    q = [match, group, sort]
    
    # run the query
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return
    # extract data for plotting as dataframe
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
        if gbe_flag:
            print("Flag", gbe_flag)
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
    if gbe_flag:
        data = pd.DataFrame({GBE_ID:gbe_id, NAME:name, WEEK:wk, attribute:val, MIN:v_min, MAX:v_max, ERROR_PLUS:v_e, ERROR_MINUS:v_em})    
    else:
        data = pd.DataFrame({WEEK:wk, attribute:val, MIN:v_min, MAX:v_max, ERROR_PLUS:v_e, ERROR_MINUS:v_em})
    return data
    #print(data)

def school_by_week(attribute, school):
    #Bar chart of weekly growth (height) for specific school
    # Optionally run for individual school
    # Only one value per week, so don't need error or min/max
    
    #school = 'Academir Charter School West'
    #print("By Week Growth Chart for School", school)
    title = "Heigh Change By Week - " + school
    #print("Var", school, attribute)
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "location.farm.name":school,
           "subject.attribute.value":{"$ne":0}
            }}
    
    #Group by GBE_Id and week, get avg, min, max
    # Name is not unique, so cannot put in id
    group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id", "name":"$subject.type",
                    "school":"$location.farm.name",
                    "plot":"$location.plot",
                   #"name":"$subject.type",
                   "week":{"$toString":"$time.week"}},
                   "avg":{"$avg":"$subject.attribute.value"},
                   "min":{"$min":"$subject.attribute.value"},
                   "max":{"$max":"$subject.attribute.value"}
                       }
                   }
    
    sort = {"$sort":{"_id.plot":1, "_id.week":1}}
    
    #q = [match]
    q = [match, group, sort]
    
    # run the query
    mu = MongoUtil(DB)
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return
    # extract data for plotting as dataframe
    gbe_id = []
    name = []
    plot = []
    wk = []
    val = []
    v_min = []
    v_max = []
    v_e = []
    v_em = []

    for doc in recs:
        #print(doc)
        #return
        #gbe_id.append("G"+str(doc["_id"]["GBE_Id"]))
        gbe_id.append(doc["_id"]["GBE_Id"])
        name.append(doc["_id"]["name"])
        plot.append(doc["_id"]["plot"])
        wk.append(doc["_id"]["week"])
        val.append(doc["avg"])
        v_max.append(doc["min"])
        v_min.append(doc["max"])
        v_e.append(doc["avg"]-doc["min"])
        v_em.append(doc["max"]-doc["avg"])

    data = pd.DataFrame({GBE_ID:gbe_id, NAME:name, WEEK:wk, PLOT:plot, attribute:val, MIN:v_min, MAX:v_max})    
    #print(data)
    ht = {
      GBE_ID: True,
      NAME:True,
      PLOT:True,
      attribute:True,
      #MIN:True,
      #MAX:True
      }
    fmt = {TITLE:title,
            COLOR: WEEK,
            X_COL:PLOT,
            Y_COL:attribute,
            HOVER_DATA:ht,
            ERROR_PLUS:None,
            ERROR_MINUS:None}        
    #return None
    return three_bar_error(data, fmt)
    
def germination_rate():
    # time between planting and germination, with number germinated as bubble
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name":{"$in":[GERMINATION, PLANTING]}
           }}
           
    group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    #"school":"$location.farm.name",
                    #"plot":"$location.plot",
                    "attribute":"$subject.attribute.name"}, #should only be one value
                    "timestamp":{"$max":"$time.timestamp"},
                    "max":{"$max":"$subject.attribute.value"},
                    "avg":{"$avg":"$subject.attribute.value"},
                    "min":{"$min":"$subject.attribute.value"}   
             }}
    
    # Array data and pivot on GBE_ID
    group2 = {"$group":{"_id":{"GBE_Id":"$_id.GBE_Id",
                    "name":"$_id.name",
                    "school":"$_id.school",           
                    "plot":"$_id.plot",
                    "attribute":"$subject.attribute.name"},
                   "items":{"$addToSet":{
                   "attribute":"$_id.attribute",
                   "value":{"max":"$max",
                            "avg":"$avg",
                            "min":"$min",
                            "timestamp":"$timestamp"}
                   }}}}
    
    # Pivot the weeks together
    project = {"$project":
        {"data":{"$arrayToObject":{
            "$zip":{"inputs":["$items.attribute", "$items.value"]}
            }}}}
    
    sort = {"$sort":{"_id.GBE_Id":1}}
    
    
    #q = [match]
    #q = [match, group]
    #q = [match, group, group3]
    q = [match, group, group2, project, sort]
    #q = [match, group4]
    #q = [match, group4, project]
    #q = [match, project2]
    
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return

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
    #data = pd.DataFrame({GBE_ID:gbe_id, "name":name, "days_to_germination":days_to_germination, "germ_avg":germ_avg, MIN:germ_min, MAX:germ_max})
    title = "Days to Germination"
    data = pd.DataFrame({GBE_ID:gbe_id, NAME:name, "days":days_to_germination, "avg":germ_avg, MIN:germ_min, MAX:germ_max, ERROR_PLUS:germ_e, ERROR_MINUS:germ_em})    
    #print(data)
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
    print(fmt)
    return scatter_chart_error(data, fmt)
    #return
    #return express_box(data, title, GBE_ID, "days_to_germination")
    
def box_test(attribute, week):
    # test of box chart

    group_name = "GBE_Id"
    if week not in [2, 3, 4]:
        week = 2
    x_axis_name = "week"
    y_axis_name = attribute
    title = "Attribute by GBE_Id: " + attribute + " week: " + str(week)
    print("Box Test", title)
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "subject.attribute.value":{"$ne":0}           
            }}
    
    q = [match]
    
    # run the query
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #dump(recs)
    #return
    # extract data for plotting as dataframe
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
    #return
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
       
    mu = MongoUtil()
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name":attribute
         }}
    
    q = [match]
    recs = mu.aggregate(DB, COLLECTION, q)
        #RANGE = {TEMPERATURE:100, HUMIDITY:100, AMBIENT_TEMP:100}
    #range = RANGE[attribute]
    max = 100
    count = [0] * (max + 1)
#     rng = range(0, max + 1)
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
    #print(data)
    #return
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

    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "subject.attribute.name":{"$in":[var1, var2]}
        }}    
    if var2 == "edible_mass":
        match = {"$match":{
            "status.status_qualifier":SUCCESS,
            "time.week":4,
            "subject.attribute.name":{"$in":[var1, var2]}
        }}

   
    # Array data and pivot weeks
    
    group2 = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    "school":"$location.farm.name",           
                    "plot":"$location.plot",
                    "week":"$time.week",
                    #"attribute":"$subject.attribute.name"
                    },
                   "items":{"$addToSet":{
                   "attribute":"$subject.attribute.name",
                   "value":"$subject.attribute.value"}
                   }}}        

    
    # Pivot the weeks together
    project = {"$project":
        {"attributes":{"$arrayToObject":{
            "$zip":{"inputs":["$items.attribute", "$items.value"]}
            }}}}
    
    #q = [match]
    #q = [match, group2]
    q = [match, group2, project]    
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    gbe_id = []
    val1 = []
    val2 = []
    school = []
    name = []
    plot = []
    for doc in recs:
    #    pprint(doc)
    #    continue


        if var1 in doc["attributes"] and var2 in doc["attributes"]:
            gbe_id.append(doc["_id"]["GBE_Id"])
            val1.append(doc["attributes"][var1])
            val2.append(doc["attributes"][var2])
            school.append(doc["_id"]["school"])
            name.append(doc["_id"]["name"])
            plot.append(doc["_id"]["plot"])
            #print(data)
    data = pd.DataFrame({var1:val1, var2:val2, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot})         
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

def environmental(env_var, attr, title):
    print("Environmental", env_var, attr)
    group_name = GBE_ID

    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "subject.attribute.name":attr
        }}    
    if attr == "edible_mass":
        match = {"$match":{
            "status.status_qualifier":SUCCESS,
            "time.week":4,
            "subject.attribute.name":attr
        }}

    #join to get environmental data
    join = {
      "$lookup": {
         "from": "2020",
         "let": { "school":"$location.farm.name",
                "week": "$time.week" },
         "pipeline": [ {
            "$match": {
               "$expr": {
                  "$and": [
                     { "$eq": [ "$$school", "$location.farm.name" ] },
                     { "$eq": [ "$$week", "$time.week" ] },
                     # Irrigation is Agronomic, not Environment, so remove this check
                     #{ "$eq": [ "$activity_type","Environment_Observation"]},
                     { "$eq": [ "$subject.attribute.name",env_var]}
                  ]
               }
            }
         } ],
         "as": "env"
      }}
    
    
        
    # Array data and pivot weeks
    
    group2 = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    "school":"$location.farm",           
                    "plot":"$location.plot",
                    "week":"$time.week",
                    #"attribute":"$subject.attribute.name"
                    },
                   "items":{"$addToSet":{
                   "attribute":"$subject.attribute.name",
                   "value":"$subject.attribute.value"}
                   }}}        

    
    # Pivot the weeks together
    project = {"$project":
        {"attributes":{"$arrayToObject":{
            "$zip":{"inputs":["$items.attribute", "$items.value"]}
            }}}}
    
    #q = [match]
    q = [match, join]
    #q = [match, join, group2, project]    
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #for doc in recs:
    #    print(doc)
    #return
    gbe_id = []
    env_val = []
    attr_val = []
    school = []
    name = []
    plot = []
       
    for doc in recs:
        #pprint(doc)
        #continue


        #if var1 in doc["attributes"] and var2 in doc["attributes"]:
        gbe_id.append(doc["subject"]["GBE_Id"])
        school.append(doc["location"]["farm"]["name"])
        attr_val.append(doc["subject"]["attribute"]["value"])
        env_val.append(doc["env"][0]["subject"]["attribute"]["value"])
        name.append(doc["subject"]["type"])
        plot.append(doc["location"]["plot"])
            #print(data)
    #print(data)
    data = {env_var:env_val, attr:attr_val, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot}         
    ht = {SCHOOL:True,
      GBE_ID: True,
      NAME:True,
      SCHOOL:True,
      PLOT:True,
      env_var:True,
      attr:True}
    fmt = {TITLE:title,
            COLOR: GBE_ID,
            X_COL:env_var,
            Y_COL:attr,
            ERROR_PLUS:None,
            ERROR_MINUS:None,
            HOVER_DATA:ht,
            TEMPLATE:None}
    #print(fmt)
    '''
    fig = bar_chart_error(SCATTER_DATA, fmt)
    fmt = {TITLE:title,
            COLOR: GBE_ID,
            X_COL:env_var,
            Y_COL:attr,
            HOVER_DATA:ht}        
    #return None
    '''
    return scatter_chart(data, fmt)

def full_env(attr, week, title):
    # Get temp and humidity plus variable
    # Use to test scatter bubble and map
    print("Full Env", attr, week)

    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "time.week":week,
        "subject.attribute.name":attr
        }}  
    
    #join to get environmental data
    join = {
      "$lookup": {
         "from": "2020",
         "let": { "school":"$location.farm.name",
                "week": "$time.week" },
         "pipeline": [ {
            "$match": {
               "$expr": {
                  "$and": [
                     { "$eq": [ "$$school", "$location.farm.name" ] },
                     { "$eq": [ "$$week", "$time.week" ] },
                     # Irrigation is Agronomic, not Environment, so remove this checkeq": [ "$activity_type","Environment_Observation"]},
                     { "$in": [ "$subject.attribute.name",["humidity", "temp"]]}
                  ]
               }
            }
         } ],
         "as": "env"
      }}
    
    #q = [match]
    #q = [match, group2]
    q = [match, join]
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #for doc in recs:
    #    print(doc)
    #return
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
        

            #print(data)
    #print(data)
    data = pd.DataFrame({TEMP:tmp, HUMIDITY:humidity, attr:attr_val, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot})         
    #print(data)
    #return
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
    #print(fmt)
    return scatter_bubble(data, fmt)


def score_cards():
    # Scorecard of data quality by school
    print("Score Card")
    
    match = {"$match":{
           "status.status_qualifier_reason":{"$in":["Invalid Data", "Missing Data"]}
           #"status.status_qualifier_reason":{"$in":["Invalid_Data","Missing_Data"]}
            }}
    
    group = {"$group":{"_id":{
                    "school":"$location.farm.name",           
                    "reason":"$status.status_qualifier_reason"
                    },
                   #"items":{"$addToSet":{
                   #"reason":"$status.status_qualifier_reason",    
                   "nbr":{"$sum":1},
                   }}
    
    sort = {"$sort":{"_id.school":1, "_id.reason":1}}
    
    
    
    #q = [match]
    q= [match, group, sort]

    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #print("dump", recs)
    #for doc in recs:
    #    print(doc)
    #return
    
    sch = []
    rsn = []
    val = []
    
    for doc in recs:
        #print(doc)
        sch.append(doc["_id"]["school"])
        rsn.append(doc["_id"]["reason"])
        val.append(doc["nbr"])
        '''
        if "Missing Data" in doc["attributes"]:
            m_d.append(int(doc["attributes"]["Missing Data"]))
        else:
            m_d.append(0)
        if "Invalid Data" in doc["attributes"]:
            i_d.append(int(doc["attributes"]["Invalid Data"]))
        else:
            i_d.append(0)
    '''        
    data = pd.DataFrame({SCHOOL:sch, "reason":rsn, "count":val})         
    #print(data)
    #return
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

    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "subject.attribute.name":"health"
        }}
   
    # Array data and pivot weeks
    
    group = {"$group":{"_id":{"GBE_Id":"$subject.GBE_Id",
                    "name":"$subject.type",
                    "school":"$location.farm.name",           
                    "plot":"$location.plot",
                    #"week":"$time.week",
                    #"attribute":"$subject.attribute.name"
                    },
                   "max":{"$max":"$subject.attribute.encode"},
                   "avg":{"$avg":"$subject.attribute.encode"},       
                   "min":{"$min":"$subject.attribute.encode"},       
                 }}
    
    sort = {"$sort":{"_id.school":1, "_id.plot":1}}
    
    #q = [match]
    q = [match, group, sort]
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
    #for doc in recs:
    #    print(doc)
    #return
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
    #print(data)
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
    print("Death by Week")
    
    total_plots = plot_count()
    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "subject.attribute.value":"dead"
        }}    
    group = {"$group":{"_id":{       
                    "week":"$time.week",
                    },
                   #"count":{"$count":"$subject.attribute.encode"}
                   "count":{"$sum":1}
                 }}
    
    sort = {"$sort":{"_id.week":1}}
    
    #q = [match]
    #q = [match, group]
    q = [match, group, sort]
    
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
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

def plot_count():
    m = {"$group":{"_id":{"School":"$location.farm.name", "plot":"$location.plot"}}}
    c = {"$count":"Count"}
    q = [m, c]
    mu = MongoUtil()
    recs = mu.aggregate(DB, COLLECTION, q)
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

def run_query(query):
    # student test query
    mu = MongoUtil()
    return mu.aggregate(DB, COLLECTION, query)


        
def query_data(query):
    print("Query Data", query)
    q = [query]
    mu = MongoUtil()
    return mu.aggregate(DB, COLLECTION, q)    

def dump(cursor):
    #print("Len", len(cursor))
    print("Print Recs")
    for rec in cursor:
        pprint(rec)
    

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