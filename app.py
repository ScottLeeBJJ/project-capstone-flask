from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144), unique=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


class GameSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')


game_schema = GameSchema()
games_schema = GameSchema(many=True)

# Endpoint to create a new guide
@app.route('/games', methods=["POST"])
def add_guide():
    title = request.json['title']
    content = request.json['content']

    new_game = Game(title, content)

    db.session.add(new_game)
    db.session.commit()

    game = Game.query.get(new_game.id)

    return game_schema.jsonify(game)


# Endpoint to query all games
@app.route("/games", methods=["GET"])
def get_games():
    all_games = Game.query.all()
    result = games_schema.dump(all_games)
    return jsonify(result)


# Endpoint for querying a single game
@app.route("/game/<id>", methods=["GET"])
def get_game(id):
    game = Game.query.get(id)
    return game_schema.jsonify(game)


# Endpoint for updating a game
@app.route("/game/<id>", methods=["PUT"])
def game_update(id):
    game = Game.query.get(id)
    title = request.json['title']
    content = request.json['content']

    game.title = title
    game.content = content

    db.session.commit()
    return game_schema.jsonify(game)


# Endpoint for deleting a record
@app.route("/game/<id>", methods=["DELETE"])
def game_delete(id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()

    return "Game was successfully deleted"

@app.route("/")
def hello():
    return("Hey Flask")


if __name__ == '__main__':
    app.run(debug=True)