from pymongo import MongoClient

# logon string to get into the database
URL = 'mongodb+srv://webbhm:sHzHKD9_vZUGCZ4@gbe-d.cc79x.mongodb.net/'

class MongoUtil(object):
    
    def __init__(self, db="gbe"):
        # Create a database client
        url = URL + db
        #url = 'mongodb+srv://webbhm:sHzHKD9_vZUGCZ4@gbe-d.cc79x.mongodb.net/gbe'
        print("Init", url)
        self._client = MongoClient(url)
        print("Initialized")
        
    # save activity records
    def save_many(self, db_nm, col_nm, rec_set):
        # save array of records to database (db) and collection (col)
        db = self._client[db_nm]
        col = db[col_nm]
        print("DB", db_nm, col_nm)
        ret = col.insert_many(rec_set)
        print(ret.inserted_ids)
        return ret
        
    def find(self, db, col, query):
        return self._client[db][col].find(query)
    
    def find_one(self, db, col, query):
        return self._client[db][col].find_one(query)    
    
    # Main function used to access observtion data
    def aggregate(self, db, col, query):
        #print("Aggregate", col)
        return self._client[db][col].aggregate(query)
    
    def count(self, db, col, query):
        return self._client[db][col].count(query)
    
    def distinct(self, db, col, item):
        return self._client[db][col].distinct(item)
    
if __name__ == "__main__":
    mu = MongoUtil("gbe")
    mu.find("gbe", "2020", {"subject.attribute.name":"temp"})
