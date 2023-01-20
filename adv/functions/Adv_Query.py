# Adv_Query
from functions.Mongo_Util import MongoUtil
def run_query(query):
    # student test query
    mu = MongoUtil()
    return mu.aggregate(DB, COLLECTION, query)

