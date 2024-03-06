"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorites

#from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():
        users = db.session.execute(db.select(User).order_by(User.email)).scalars()
        user_list = [user.serialize() for user in users]
        response_body = {'message': 'List of Users',
                         'results': user_list}
        return response_body, 200


@app.route('/people', methods=['GET'])
def get_people():
        people = db.session.execute(db.select(People).order_by(People.full_name)).scalars()
        people_list = [people.serialize() for people in people]
        response_body = {'message': 'List of people',
                         'results': people_list}
        return response_body, 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
        people = db.session.get(People, people_id)
        if people is None:
            response_body = {'message': 'People not found.'}
            return response_body, 404
        response_body = people.serialize()
        return response_body, 200  


@app.route('/planet', methods=['GET'])
def get_planet():
        planets = db.session.execute(db.select(Planet).order_by(Planet.name)).scalars()
        planet_list = [planet.serialize() for planet in planets]
        response_body = {'message': 'List of planets',
                         'results': planet_list}
        return response_body, 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    if request.method == 'GET':
        planet = db.session.get(Planet, planet_id)
        if planet is None:
            response_body = {'message': 'Planet not found.'}
            return response_body, 404
        response_body = planet.serialize()
        return response_body, 200   


@app.route('/user/favorite', methods=['GET'])
def user_favorites():
    favorites = db.session.execute(db.select(Favorites).order_by(Favorites.id)).scalars()
    favorite_list = [favorites.serialize() for favorites in favorites]
    response_body = {'message': 'Favorites List',
                     'results': favorite_list}
    return response_body, 200


@app.route('/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_planet(planet_id):
    request_body = request.get_json()
    planet = db.session.query(Planet).get(planet_id)
    if not planet:
            response_body = {'message': 'Planet not added to favorites.'}
            return response_body, 404
    new_favorite = Favorites(user_id=request_body['user_id'],
                             planet_id=request_body['planet_id'])
    db.session.add(new_favorite)
    db.session.commit()
    response_body = {'message': 'Planet added to favorite', 
                     'result': new_favorite.serialize()}
    return response_body, 200


@app.route('/favorite/people/<int:people_id>', methods = ['POST'])
def add_people(people_id):
    request_body = request.get_json()
    people = db.session.query(People).get(people_id)
    if not people:
            response_body = {'message': 'People not added to favorites.'}
            return response_body, 404
    new_favorite = Favorites(user_id=request_body['user_id'],
                             people_id=request_body['people_id'])
    db.session.add(new_favorite)
    db.session.commit()
    response_body = {'message': 'People added to favorites', 
                     'result': new_favorite.serialize()}
    return response_body, 200


@app.route('/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_people(people_id):
    favoritesList = Favorites.query.all()
    toDelete = None
    for item in favoritesList:
        if item.serialize()['people_id'] == people_id:
            toDelete = item
    if toDelete == None:
        response_body = {'message': 'Invalid people id.'}
        return response_body, 400
    else:
        db.session.delete(toDelete)
        db.session.commit()
        response_body = {'message': 'Favorite people deleted.'}
        return response_body, 200


@app.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_planet(planet_id):
    favoritesList = Favorites.query.all()
    toDelete = None
    for item in favoritesList:
        if item.serialize()['planet_id'] == planet_id:
            toDelete = item
    if toDelete == None:
        response_body = {'message': 'Invalid planet id.'}
        return response_body, 400
    else:
        db.session.delete(toDelete)
        db.session.commit()
        response_body = {'message': 'Favorite planet deleted.'}
        return response_body, 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)