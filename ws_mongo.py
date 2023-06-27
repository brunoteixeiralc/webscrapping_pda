from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from decouple import config

def connectMongoDB():
    uri = config('URI')
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")        
    except Exception as e:
        print(e)
    
    return client
        
def insert_update_best_price_products(res_top3):
    client = connectMongoDB()
    db = client['ws_pda']
    collection = db['best_price_products']
    
    for product in res_top3:
        busca = collection.find_one( { '_id': product["id"] } )
        
        if busca is None: 
            products = {
                    "_id": product["id"],
                    "name": product["name"],
                    "discount": product["discount_int"],
                    "price": product["old_price"],
                    "discount_price": product["price"],
                    "insert_date": datetime.today().strftime("%d/%m/%Y %H:%M:%S")
                }
            collection.insert_one(products)
        else:
            if product["discount_int"] > busca["discount"]:
                collection.update_one( busca, { '$set': { "discount": product["discount_int"], "price" : product["old_price"], "discount_price" : product["price"], "insert_date" : datetime.today().strftime("%d/%m/%Y %H:%M:%S") } } )
        