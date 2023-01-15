'''
Get completed data as Dataframe for charts
Calls to MongoDB for data
Test data is a separate module
'''
from datetime import datetime
session = {'defaults':{'trial':{"id":123, 'start_date':datetime.now().timestamp-(30*24*60*60)}}}

from test_data import get_test_data
from chart_frame import three_column_frame

test_struct={'group':{'name':'Trial_Id', 'label':'Trial_Id'},
        'x_col':{'name':'trial_day', 'label':'Day'},
        'y_col':{'name':'temp', 'label':'Temperature'}}


def test_chart_data():
    # generate data frame for test_chart
    json = get_test_data()
    data = three_column_frame(json, test_struct)
    return data

def env_data(trial_id, attribute):
    # environmental data for an individual trial
    start_date = session["defaults"]['trial']["start_date"]
    end_date = datetime.now().timestamp()
    print("env_data", attribute, start_time, end_time)
    match = {"$match":{
           "trial.id":trial_id,
           "status.status_qualifier":SUCCESS,
           "subject.attribute.name": attribute,
           "$and":[{"time.timestamp":{"$gt":start_time}},
           {"time.timestamp":{"$lt":end_time}}]
            }}
    
    sort = {"$sort":{"time.timestamp":1}}
    query = [match, sort]
        
    mu = MongoUtil(DB)    
    recs = mu.aggregate(DB, OB_COL, query)
    
    test_struct={'group':{'name':'Trial_Id', 'label':'Trial_Id'},
        'x_col':{'name':'trial_day', 'label':'Day'},
        'y_col':{'name':attribute, 'label':'Temperature'}}

    return three_column_frame(recs, test_struct)

    ts = []
    value = []
    for doc in recs:
        #print(start_time, doc[TIME][TIMESTAMP], end_time)
        ts.append(doc["time"][TIME_STR])
        value.append(doc[SUBJECT][ATTRIBUTE][VALUE])    
    return DataFrame({TIME:ts, attribute:value})    

def test():
    print("Test of test chart data")
    f = test_chart_data()
    print(f)    

if __name__ == '__main__':
    test()

