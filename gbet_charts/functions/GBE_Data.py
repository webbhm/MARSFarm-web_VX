'''
Call MongoDB to get data
Format into Pandas DataFrame
Author: Howard Webb
Date"2/3/2020
'''

from pandas import DataFrame
from datetime import datetime

from functions.Mongo_Util import MongoUtil
from functions.GBE_Util import *
from gbet_charts.functions.DewPoint import getDewPoint


DB = "test"
OB_COL = "Observations"
TRIAL_COL = "Trial"

TEMPERATURE = "Temperature"
HUMIDITY = "Humidity"

def get_trial(school, trial):
        '''
        Run Mongo to get data
        This is a single attribute retreival
        Used for Temperature, Humidity or Pressure charting
        The attribute is passed in when the object is created.
        Now that have added multi-attribute reports, this may not be the best architecture.
        '''
        print("Get Trial")
        match = {"$match":{
           "location.school.name":school,
           "activity.id":trial
         }}
        #match = {"$match":{}}
        #print(match)
        
        query = [match]
        
        mu = MongoUtil(DB)    
        recs = mu.aggregate(DB, TRIAL_COL, query)
            
        for doc in recs:
            #print(doc)
            #continue
            if END_DATE not in doc[TIME]:
                doc[TIME][END_DATE] = datetime.now().timestamp() * 1000
                doc[TIME][END_DATE_STR] = datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                doc[TIME][END_DATE] = doc[TIME][END_DATE]
                doc[TIME][END_DATE_STR]  = datetime.fromtimestamp(doc[TIME][END_DATE]/1000).strftime("%Y-%m-%d %H:%M")
            # mongodb uses milsec so must shorten    
            doc[TIME][START_DATE] = doc[TIME][START_DATE]
            # Get date string from timestamp
            doc[TIME][START_DATE_STR] = datetime.fromtimestamp(doc[TIME][START_DATE]/1000).strftime("%Y-%m-%d %H:%M")
            return doc

def env_data(attribute, start_time=0, end_time=datetime.now().timestamp()*1000):
    # Mongo timestamp is unix * 1000
    print("env_data", attribute, start_time, end_time)
    match = {"$match":{
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "$and":[{"time.timestamp":{"$gt":start_time}},
           {"time.timestamp":{"$lt":end_time}}]
            }}
    
    sort = {"$sort":{"time.timestamp":1}}
    query = [match, sort]
    print(query)    
    mu = MongoUtil(DB)    
    recs = mu.aggregate(DB, OB_COL, query)
    #print(recs)
    ts = []
    value = []
    for doc in recs:
        #print(doc)
        #print(start_time, doc[TIME][TIMESTAMP], end_time)
        ts.append(doc["time"][TIME_STR])
        value.append(doc[SUBJECT][ATTRIBUTE][VALUE])    
    data =  DataFrame({TIME:ts, attribute:value})
    #print(data)
    return data


def dew_point_data(start_time, end_time):
    print("Two Variables", start_time, end_time)
    group_name = GBE_ID

    match = {"$match":{
        "status.status_qualifier":SUCCESS,
        "subject.attribute.name":{"$in":[TEMPERATURE, HUMIDITY]},
        "$and":[{"time.timestamp":{"$gt":start_time}},
        {"time.timestamp":{"$lt":end_time}}]
        }}

    # Array data and pivot weeks
    group2 = {"$group":{"_id":{
                    #"school":"$location.school.name",           
                    #"attribute":"$subject.attribute.name",
                    "time":"$time.timestamp_str",
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
    sort = {"$sort":{"_id.time":1}}    
    #q = [match]
    #q = [match, group2]
    q = [match, group2, project, sort]
    
    mu = MongoUtil()
    #print("Run Query")
    recs = mu.aggregate(DB, OB_COL, q)
    #print("DewPoint from Mongo")
    #for doc in recs:
    #    print(doc)
    #return
    att = []
    value = []
    time = []
    for doc in recs:
        if TEMPERATURE in doc["attributes"] and HUMIDITY in doc["attributes"]:
            t = doc["attributes"][TEMPERATURE]
            h = doc["attributes"][HUMIDITY]
            dp = getDewPoint(t, h)
            
            time.append(doc["_id"]["time"])
            att.append(TEMPERATURE)
            value.append(t)

            time.append(doc["_id"]["time"])
            att.append(HUMIDITY)
            value.append(h)
            
            time.append(doc["_id"]["time"])
            att.append("dew-point")
            value.append(dp)
                
            #print(data)
    data = DataFrame({"time":time, "attribute":att, "value":value})
    return data

def data_print(data):
    for doc in data:
        print(doc)
    
if __name__ == "__main__":
    #data = get_trial("OpenAgBloom", "Trial_3")
    #data = env_data(CO2,1643348401000.0, datetime.now().timestamp()*1000 )
    data = dew_point_data(0, datetime.now().timestamp()*1000)
    print(data)
    