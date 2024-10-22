from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    isbn = fields.Str(required=True)
    price = fields.Float(required=True)
    storeID = fields.Str(required=True)
    
class BookPatchSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    isbn = fields.Str()
    price = fields.Float()
    storeID = fields.Str()
    
    
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    