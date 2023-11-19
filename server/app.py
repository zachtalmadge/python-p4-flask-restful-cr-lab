#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

# flask app instance
app = Flask(__name__)

# configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

# api instance
api = Api(app)

class Plants(Resource):
    def get(self):
        plants_dict = [plant.to_dict() for plant in Plant.query.all()]
        return plants_dict, 200
    
    def post(self):
        plant_json = request.get_json()
        new_plant = Plant(**plant_json)
        # print(new_plant.to_dict())
        db.session.add(new_plant)
        db.session.commit()
        
        return new_plant.to_dict(), 201

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        
        return plant, 200
    
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
