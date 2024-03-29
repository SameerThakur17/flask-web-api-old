from flask_restful import reqparse, Resource

from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field is required"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        else:
            return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return ({"message": f"An item with name {name} already exists"}, 400)

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data["price"])
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        # return {"items": [item.json() for item in ItemModel.query.all()]}, 200
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}, 200
