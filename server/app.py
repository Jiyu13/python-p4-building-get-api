#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# compact=False, each item will be formated on separate line
# has JSON responses print on separate lines with indentation
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

#  1. Get All Game Records
@app.route('/games')
def games():

    games = []

    # other examples about how the data is returned by using SQLAlchemy
    games_by_title = Game.query.order_by(Game.title).all()
    first_10_games = Game.query.limit(10).all()

    all_games_from_db = Game.query.all()
    
    for game in all_games_from_db:
        # make data into a python dict obj
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            'price': game.price
        }
        games.append(game_dict)
    response = make_response(
        # serialises SQLAlchemy data obj to JSON format
        jsonify(games),
        200,
        # optional, can be done with jsonify()
        {"Content-Type": "application/json"}    
    )
    return response


# 2.Getting One Game Using Params
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    # game_dict = {
    #         "title": game.title,
    #         "genre": game.genre,
    #         "platform": game.platform,
    #         'price': game.price
    # }
    game_dict = game.to_dict()
    response = make_response(game_dict, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)