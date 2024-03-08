from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from callAPI import *


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

basedir = os.path.abspath(os.path.dirname(__file__)) + "/data/"

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)


class PlayedGame(db.Model):
    __tablename__ = 'Played_Game'
    user_id = db.Column(db.Integer, db.ForeignKey('User.UID'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.GID'), primary_key=True)
    
    item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    kills = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    
    true_damage = db.Column(db.Integer, nullable=True)
    ad_damage = db.Column(db.Integer, nullable=True)
    magic_damage = db.Column(db.Integer, nullable=True)
    
    position = db.Column(db.String, nullable=False)
    
    gold_earned = db.Column(db.Integer, nullable=False)
    gold_spent = db.Column(db.Integer, nullable=False)
    
    CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    
    total_minions = db.Column(db.Integer, nullable=True)
    
    vision_score = db.Column(db.Integer, nullable=True)
    
    user = db.relationship('UserModel', back_populates = 'games')
    game = db.relationship('GameModel', back_populates = 'users')


class UserModel(db.Model):
    __tablename__ = 'User'
    UID = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String, nullable=True)
    profileIcon = db.Column(db.Integer, nullable=True)
    revisionDate = db.Column(db.Integer, nullable=False)
    
    games = db.relationship('PlayedGame', back_populates = 'user')


class GameModel(db.Model):
    __tablename__ = 'Game'
    GID = db.Column(db.String, primary_key=True)
    time_start = db.Column(db.Integer, nullable=False)
    time_end = db.Column(db.Integer, nullable=True)
    
    users = db.relationship('PlayedGame', back_populates = 'game')


class ItemModel(db.Model):
    __tablename__ = 'Item'
    IID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    totalPrice = db.Column(db.String, nullable=False)


class ChampionModel(db.Model):
    __tablename__ = 'Champion'
    CID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
 
   
class SummonerSpellModel(db.Model):
    __tablename__ = 'SummonerSpell'
    SID = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=True)


with app.app_context():
    db.create_all()
    
resource_fields = {
    'UID': fields.String,
    'name': fields.String,
    'rank': fields.String,
    'profileIcon': fields.Integer,
    'revisionDate': fields.Integer
}


class UserByName(Resource):
    @marshal_with(resource_fields)
    def get(self, name):
        if not bool(UserModel.query.filter_by(name=name).first()):
            userData = getSummonerByName(name)
            newUser = UserModel(
                UID=userData['puuid'], 
                name=name, 
                profileIcon=userData['profileIconId'], 
                revisionDate=userData['revisionDate']
            )
            db.session.add(newUser)
            db.session.commit()
        
        result = UserModel.query.filter_by(name=name).first()
        
        return result, 200


api.add_resource(UserByName, "/user/by-name/<name>")


class UserByPUUID(Resource):
    @marshal_with(resource_fields)
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(UID=PUUID).first()):
            userData = getSummonerByPUUID(PUUID)
            newUser = UserModel(
                UID=PUUID, 
                name=userData['name'], 
                profileIcon=userData['profileIconId'], 
                revisionDate=userData['revisionDate']
            )
            db.session.add(newUser)
            db.session.commit()
            
        result = UserModel.query.filter_by(UID=PUUID).first()

        return result, 200


api.add_resource(UserByPUUID, "/user/by-PUUID/<PUUID>")


if __name__ == "__main__":
    app.run(debug = True) #CHANGE BEFORE PRODUCTION