import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from Schemas.schemas import StoreSchema
from bson import ObjectId
from flask import jsonify
from db import stores_collection
from db import redis_client

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:storeID>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, storeID):
        store = redis_client.get(f"store:{storeID}")
        if store:
            return jsonify(eval(store))
        
        store = stores_collection.find_one({"_id": ObjectId(storeID)})
        if store is None:
            abort(404, message="Bookstore not found")
        
        store["_id"] = str(store["_id"])
        
        redis_client.setex(f"store:{storeID}", 600, str(store))

        return jsonify(store) 
    
    def delete(self, storeID):
        result = stores_collection.delete_one({"id": storeID}) 
        if result.deleted_count == 0:
            abort(404, message="Store not found")
        
        redis_client.delete(f"store:{storeID}")
        
        return {"message": "Store has been deleted"}
    
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = list(stores_collection.find())
        if not stores:
            abort(404, message="No Bookstores were found")
        return stores
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        if stores_collection.find_one({"name": store_data["name"]}):
            abort(400, message="A store with that name already exists")
        
        storeID = uuid.uuid4().hex
        newStore = {**store_data, "id": storeID}
        stores_collection.insert_one(newStore)
        
        redis_client.setex(f"store:{storeID}", 600, str(newStore))
            
        return newStore, 201
