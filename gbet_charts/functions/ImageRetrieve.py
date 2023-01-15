'''
Get jpg and gif from MongoDB (stored as binary)
Author: Howard Webb
Date: 2022-08-29
'''

from functions.Mongo_Util import MongoUtil
from bson.binary import Binary
import io
# image processing
from PIL import Image
# used for image display
import matplotlib.pyplot as plt
#from bson.objectid import ObjectId
import base64

database = "images"
collection = "latest"

def get_doc(farm, field):
    #match = {"_id":ObjectId("630a37cfde603972af7b32a8")}
    match = {"location":{"farm":farm, "field":field}}

    # get image document from database
    query = [match]
    mu = MongoUtil()
    return mu.find_one(database, collection, match)


def get_gif(farm, field):
    doc = get_doc(farm, field)
    file_name = doc['gif']['name']
    pil_img = Image.open(io.BytesIO(doc['gif']['image']))
    data = io.BytesIO()
    #First save image as in-memory.
    pil_img.save(data, "GIF", save_all=True)
    #pil_img.save("/home/pi/Desktop/test.gif", "GIF", save_all=True)
    
    #Then encode the saved image file.
    encoded_img_data = base64.b64encode(data.getvalue()).decode('utf-8')
    # display for testing
    #pil_img.show()
    return doc['gif']['start_date'], doc['gif']['end_date'], doc['gif']['name'], encoded_img_data
    #return doc['gif']['start_date'], doc['gif']['end_date'], doc['gif']['name'], data

def get_jpg(farm, field):
    doc = get_doc(farm, field)
    file_name = doc['gif']['name']
    pil_img = Image.open(io.BytesIO(doc['jpg']['image']))
    data = io.BytesIO()
    #First save image as in-memory.
    pil_img.save(data, "JPEG")
    #Then encode the saved image file.
    encoded_img_data = base64.b64encode(data.getvalue()).decode('utf-8')
    # display for testing
    #pil_img.show()
    return doc['jpg']['time_str'], doc['jpg']['name'], encoded_img_data

    
def test():
    print("Test PNG")
    farm = "OpenAgBloom"
    field = "GBE_D_3"
    print("Get Image")
    doc = get_doc(farm,  field)
    #get_png(doc)
    get_jpg(doc)
    print("Done")
    
 
if __name__=="__main__":
    test()
    #test2()
    #test3()