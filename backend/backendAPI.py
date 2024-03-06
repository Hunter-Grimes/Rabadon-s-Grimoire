from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    UID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String, nullable=True)
    
    def __repr__(self) -> str:
        return f"User(name={self.name}, rank={self.rank})"

class GameModel(db.Model):
    GID = db.Column(db.Integer, primary_key=True)

playedGame = db.Table('playedGame',
    db.Column('user_id', db.Integer, db.ForeignKey('UserModel.UID'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('GameModel.GID'), primary_key=True)
)

with app.app_context():
    db.create_all()

# @app.route("/")
# def home():
#     return "Home"

# @app.route("/get-user/<user_id>")
# def get_user(user_id):
#     user_data = {
#         "user_id" : user_id,
#         "name": "temp"
#     }
    
#     extra = request.args.get("extra")
#     if extra:
#         user_data["extra"] = extra
        
#     return jsonify(user_data), 200

# @app.route("/create-user", methods=["POST"])
# def create_user():
#     # if request.method == "POST":
#     data = request.get_json()
#     return jsonify(data), 201

class User(Resource):
    def get(self, UID):
        return {"UID": UID}

api.add_resource(User, "/user/<string:UID>")

if __name__ == "__main__":
    app.run(debug = True) #CHANGE BEFORE PRODUCTION
    