'''
MongoDB queries for Experiment level charts

Author: Howard Webb
Date: 6/29/2021
'''

from functions.Mongo_Util import MongoUtil
from pprint import pprint
from datetime import datetime
from functions.GBE_Util import *



# Source directories for data files, not used here

DB = "gbe"
COLLECTION = "2020"

   
def find(query):
    print("Find", query)
    mu = MongoUtil(DB)
    docs = mu.find(DB, COLLECTION, query)
    dump(docs)
        
def get_distinct_query(item, db=DB, col=COLLECTION):
    # get distinct list of items
    print("Distinct", item, db, col)
    mu = MongoUtil(db)
    return mu.distinct(db, col, item)
    
def growth_rate_query(attribute):    
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "subject.attribute.value":{"$ne":0}           
            }}
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
    
    #q = [match]
    q = [match, group, sort]
    
    # run the query
    mu = MongoUtil()
    return mu.aggregate(DB, COLLECTION, q)

def germination_rate_query():
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
    return mu.aggregate(DB, COLLECTION, q)
    
def box_query(attribute, week):
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
    return mu.aggregate(DB, COLLECTION, q)

    
def histogram_query(attribute, title="None", reduce=1):
       
    mu = MongoUtil()
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name":attribute
         }}
    
    q = [match]
    return mu.aggregate(DB, COLLECTION, q)

def two_var_scatter_query(var1, var2):
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
    return mu.aggregate(DB, COLLECTION, q)

def environmental_query(env_var, attr):
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
    return mu.aggregate(DB, COLLECTION, q)

def full_env_query(attr, week):
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
    return mu.aggregate(DB, COLLECTION, q)
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
    #     return pd.DataFrame({TEMP:tmp, HUMIDITY:humidity, attr:attr_val, "GBE_Id":gbe_id, SCHOOL:school, NAME:name, PLOT:plot})         

def score_card_query():
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
    return mu.aggregate(DB, COLLECTION, q)

def health_query():
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
    return mu.aggregate(DB, COLLECTION, q)

def deaths_by_week_query():
    print("Death by Week")
    
    total_plots = plot_count_query()
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
    return mu.aggregate(DB, COLLECTION, q)

def plot_count_query():
    m = {"$group":{"_id":{"School":"$location.farm.name", "plot":"$location.plot"}}}
    c = {"$count":"Count"}
    q = [m, c]
    mu = MongoUtil()
    return mu.aggregate(DB, COLLECTION, q)

def dump(cursor):
    #print("Len", len(cursor))
    print("Print Recs")
    for rec in cursor:
        pprint(rec)

def test():
    print("Test queries")
    docs = get_distinct_query()
    dump(docs)
    print("Done")

if __name__=="__main__":
    test()
