from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from callAPI import getMatchByMatchID, getMatchLast20, getSummonerByName, getSummonerByPUUID
import os

basedir = os.path.abspath(os.path.dirname(__file__)) + "/data/"

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)


class PlayedGame(db.Model):
    __tablename__ = 'Played_Game'
    user_id = db.Column(db.String, db.ForeignKey('User.UID'), primary_key=True)
    game_id = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    
    time_start = db.Column(db.Integer, nullable=False)
    time_end = db.Column(db.Integer, nullable=True)
    
    patch = db.Column(db.String, nullable=False)
    
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
    patch = db.Column(db.String, nullable=False)
    
    
    p0_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p0_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p0_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p0_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p0_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p0_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p0_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p0_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p0_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p0_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p0_kills = db.Column(db.Integer, nullable=False)
    p0_deaths = db.Column(db.Integer, nullable=False)
    p0_assists = db.Column(db.Integer, nullable=False)
    
    p0_true_damage = db.Column(db.Integer, nullable=True)
    p0_ad_damage = db.Column(db.Integer, nullable=True)
    p0_magic_damage = db.Column(db.Integer, nullable=True)
    
    p0_position = db.Column(db.String, nullable=False)
    
    p0_gold_earned = db.Column(db.Integer, nullable=False)
    p0_gold_spent = db.Column(db.Integer, nullable=False)
    
    p0_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p0_champion_name = db.Column(db.String, nullable=True)
    
    p0_total_minions = db.Column(db.Integer, nullable=True)
    
    p0_vision_score = db.Column(db.Integer, nullable=True)
    
    p0_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p1_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p1_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p1_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p1_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p1_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p1_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p1_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p1_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p1_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p1_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p1_kills = db.Column(db.Integer, nullable=False)
    p1_deaths = db.Column(db.Integer, nullable=False)
    p1_assists = db.Column(db.Integer, nullable=False)
    
    p1_true_damage = db.Column(db.Integer, nullable=True)
    p1_ad_damage = db.Column(db.Integer, nullable=True)
    p1_magic_damage = db.Column(db.Integer, nullable=True)
    
    p1_position = db.Column(db.String, nullable=False)
    
    p1_gold_earned = db.Column(db.Integer, nullable=False)
    p1_gold_spent = db.Column(db.Integer, nullable=False)
    
    p1_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p1_champion_name = db.Column(db.String, nullable=True)
    
    p1_total_minions = db.Column(db.Integer, nullable=True)
    
    p1_vision_score = db.Column(db.Integer, nullable=True)
    
    p1_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p2_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p2_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p2_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p2_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p2_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p2_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p2_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p2_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p2_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p2_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p2_kills = db.Column(db.Integer, nullable=False)
    p2_deaths = db.Column(db.Integer, nullable=False)
    p2_assists = db.Column(db.Integer, nullable=False)
    
    p2_true_damage = db.Column(db.Integer, nullable=True)
    p2_ad_damage = db.Column(db.Integer, nullable=True)
    p2_magic_damage = db.Column(db.Integer, nullable=True)
    
    p2_position = db.Column(db.String, nullable=False)
    
    p2_gold_earned = db.Column(db.Integer, nullable=False)
    p2_gold_spent = db.Column(db.Integer, nullable=False)
    
    p2_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p2_champion_name = db.Column(db.String, nullable=True)
    
    p2_total_minions = db.Column(db.Integer, nullable=True)
    
    p2_vision_score = db.Column(db.Integer, nullable=True)
    
    p2_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p3_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p3_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p3_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p3_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p3_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p3_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p3_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p3_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p3_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p3_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p3_kills = db.Column(db.Integer, nullable=False)
    p3_deaths = db.Column(db.Integer, nullable=False)
    p3_assists = db.Column(db.Integer, nullable=False)
    
    p3_true_damage = db.Column(db.Integer, nullable=True)
    p3_ad_damage = db.Column(db.Integer, nullable=True)
    p3_magic_damage = db.Column(db.Integer, nullable=True)
    
    p3_position = db.Column(db.String, nullable=False)
    
    p3_gold_earned = db.Column(db.Integer, nullable=False)
    p3_gold_spent = db.Column(db.Integer, nullable=False)
    
    p3_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p3_champion_name = db.Column(db.String, nullable=True)
    
    p3_total_minions = db.Column(db.Integer, nullable=True)
    
    p3_vision_score = db.Column(db.Integer, nullable=True)
    
    p3_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p4_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p4_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p4_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p4_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p4_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p4_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p4_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p4_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p4_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p4_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p4_kills = db.Column(db.Integer, nullable=False)
    p4_deaths = db.Column(db.Integer, nullable=False)
    p4_assists = db.Column(db.Integer, nullable=False)
    
    p4_true_damage = db.Column(db.Integer, nullable=True)
    p4_ad_damage = db.Column(db.Integer, nullable=True)
    p4_magic_damage = db.Column(db.Integer, nullable=True)
    
    p4_position = db.Column(db.String, nullable=False)
    
    p4_gold_earned = db.Column(db.Integer, nullable=False)
    p4_gold_spent = db.Column(db.Integer, nullable=False)
    
    p4_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p4_champion_name = db.Column(db.String, nullable=True)
    
    p4_total_minions = db.Column(db.Integer, nullable=True)
    
    p4_vision_score = db.Column(db.Integer, nullable=True)
    
    p4_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p5_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p5_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p5_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p5_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p5_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p5_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p5_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p5_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p5_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p5_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p5_kills = db.Column(db.Integer, nullable=False)
    p5_deaths = db.Column(db.Integer, nullable=False)
    p5_assists = db.Column(db.Integer, nullable=False)
    
    p5_true_damage = db.Column(db.Integer, nullable=True)
    p5_ad_damage = db.Column(db.Integer, nullable=True)
    p5_magic_damage = db.Column(db.Integer, nullable=True)
    
    p5_position = db.Column(db.String, nullable=False)
    
    p5_gold_earned = db.Column(db.Integer, nullable=False)
    p5_gold_spent = db.Column(db.Integer, nullable=False)
    
    p5_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p5_champion_name = db.Column(db.String, nullable=True)
    
    p5_total_minions = db.Column(db.Integer, nullable=True)
    
    p5_vision_score = db.Column(db.Integer, nullable=True)
    
    p5_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p6_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p6_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p6_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p6_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p6_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p6_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p6_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p6_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p6_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p6_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p6_kills = db.Column(db.Integer, nullable=False)
    p6_deaths = db.Column(db.Integer, nullable=False)
    p6_assists = db.Column(db.Integer, nullable=False)
    
    p6_true_damage = db.Column(db.Integer, nullable=True)
    p6_ad_damage = db.Column(db.Integer, nullable=True)
    p6_magic_damage = db.Column(db.Integer, nullable=True)
    
    p6_position = db.Column(db.String, nullable=False)
    
    p6_gold_earned = db.Column(db.Integer, nullable=False)
    p6_gold_spent = db.Column(db.Integer, nullable=False)
    
    p6_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p6_champion_name = db.Column(db.String, nullable=True)
    
    p6_total_minions = db.Column(db.Integer, nullable=True)
    
    p6_vision_score = db.Column(db.Integer, nullable=True)
    
    p6_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p7_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p7_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p7_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p7_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p7_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p7_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p7_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p7_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p7_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p7_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p7_kills = db.Column(db.Integer, nullable=False)
    p7_deaths = db.Column(db.Integer, nullable=False)
    p7_assists = db.Column(db.Integer, nullable=False)
    
    p7_true_damage = db.Column(db.Integer, nullable=True)
    p7_ad_damage = db.Column(db.Integer, nullable=True)
    p7_magic_damage = db.Column(db.Integer, nullable=True)
    
    p7_position = db.Column(db.String, nullable=False)
    
    p7_gold_earned = db.Column(db.Integer, nullable=False)
    p7_gold_spent = db.Column(db.Integer, nullable=False)
    
    p7_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p7_champion_name = db.Column(db.String, nullable=True)
    
    p7_total_minions = db.Column(db.Integer, nullable=True)
    
    p7_vision_score = db.Column(db.Integer, nullable=True)
    
    p7_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p8_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p8_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p8_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p8_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p8_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p8_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p8_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p8_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p8_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p8_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p8_kills = db.Column(db.Integer, nullable=False)
    p8_deaths = db.Column(db.Integer, nullable=False)
    p8_assists = db.Column(db.Integer, nullable=False)
    
    p8_true_damage = db.Column(db.Integer, nullable=True)
    p8_ad_damage = db.Column(db.Integer, nullable=True)
    p8_magic_damage = db.Column(db.Integer, nullable=True)
    
    p8_position = db.Column(db.String, nullable=False)
    
    p8_gold_earned = db.Column(db.Integer, nullable=False)
    p8_gold_spent = db.Column(db.Integer, nullable=False)
    
    p8_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p8_champion_name = db.Column(db.String, nullable=True)
    
    p8_total_minions = db.Column(db.Integer, nullable=True)
    
    p8_vision_score = db.Column(db.Integer, nullable=True)
    
    p8_won_game = db.Column(db.Boolean, nullable=False)
    
    
    p9_PUUID = db.Column(db.String, db.ForeignKey('User.UID'), nullable=False)
    
    p9_item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p9_item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p9_item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p9_item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p9_item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p9_item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    p9_item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    p9_summoner1ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    p9_summoner2ID = db.Column(db.Integer, db.ForeignKey('SummonerSpell.SID'), nullable=True)
    
    p9_kills = db.Column(db.Integer, nullable=False)
    p9_deaths = db.Column(db.Integer, nullable=False)
    p9_assists = db.Column(db.Integer, nullable=False)
    
    p9_true_damage = db.Column(db.Integer, nullable=True)
    p9_ad_damage = db.Column(db.Integer, nullable=True)
    p9_magic_damage = db.Column(db.Integer, nullable=True)
    
    p9_position = db.Column(db.String, nullable=False)
    
    p9_gold_earned = db.Column(db.Integer, nullable=False)
    p9_gold_spent = db.Column(db.Integer, nullable=False)
    
    p9_CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    p9_champion_name = db.Column(db.String, nullable=True)
    
    p9_total_minions = db.Column(db.Integer, nullable=True)
    
    p9_vision_score = db.Column(db.Integer, nullable=True)
    
    p9_won_game = db.Column(db.Boolean, nullable=False)
    
    
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


class UserByName(Resource):
    resource_fields = {
        'UID': fields.String,
        'name': fields.String,
        'rank': fields.String,
        'profileIcon': fields.Integer,
        'revisionDate': fields.Integer
    }
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
    resource_fields = {
        'UID': fields.String,
        'name': fields.String,
        'rank': fields.String,
        'profileIcon': fields.Integer,
        'revisionDate': fields.Integer
    }
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


class GameIDLast20(Resource):
    def get(self, PUUID):
        result = PlayedGame.query.filter_by(user_id=PUUID).order_by(PlayedGame.time_start.desc()).limit(20).all()
        result = [game.game_id for game in result]
        return result, 200

api.add_resource(GameIDLast20, "/game-id/last-20/<PUUID>")


class GameDataByPlayer(Resource):
    def get(self, GID, PUUID):
        if not bool(GameModel.query.filter_by(GID=GID).first()):
            return 404

        result = GameModel.query.filter_by(GID=GID).first()
        playerOptions = ['p0_', 'p1_', 'p2_', 'p3_', 'p4_', 'p5_', 'p6_', 'p7_', 'p8_', 'p9_']
        
        playerNum = None
        
        for player in playerOptions:
            if getattr(result, player + 'PUUID') == PUUID:
                playerNum = player
        
        playerStats = {
            'patch': getattr(result, 'patch'),
            'time_start': getattr(result, 'time_start'),
            'time_end': getattr(result, 'time_end'),
            
            'item0': getattr(result, playerNum + 'item0'),
            'item1': getattr(result, playerNum + 'item1'),
            'item2': getattr(result, playerNum + 'item2'),
            'item3': getattr(result, playerNum + 'item3'),
            'item4': getattr(result, playerNum + 'item4'),
            'item5': getattr(result, playerNum + 'item5'),
            'item6': getattr(result, playerNum + 'item6'),
            'summoner1ID': getattr(result, playerNum + 'summoner1ID'),
            'summoner2ID': getattr(result, playerNum + 'summoner2ID'),
            'kills': getattr(result, playerNum + 'kills'),
            'deaths': getattr(result, playerNum + 'deaths'),
            'assists': getattr(result, playerNum + 'assists'),
            'true_damage': getattr(result, playerNum + 'true_damage'),
            'ad_damage': getattr(result, playerNum + 'ad_damage'),
            'magic_damage': getattr(result, playerNum + 'magic_damage'),
            'position': getattr(result, playerNum + 'position'),
            'gold_earned': getattr(result, playerNum + 'gold_earned'),
            'gold_spent': getattr(result, playerNum + 'gold_spent'),
            'CID': getattr(result, playerNum + 'CID'),
            'champion_name': getattr(result, playerNum + 'champion_name'),
            'total_minions': getattr(result, playerNum + 'total_minions'),
            'vision_score': getattr(result, playerNum + 'vision_score'),
            'won_game': getattr(result, playerNum + "won_game")
        }
        return playerStats, 200      

api.add_resource(GameDataByPlayer, "/game-data/by-Player/<GID>/<PUUID>")

   
class GameDataLast20(Resource):
    def put(self, PUUID):
        if not bool(UserModel.query.filter_by(UID=PUUID).first()):
            return 404

        games = getMatchLast20(PUUID)
        for item in games:
            gameData = getMatchByMatchID(item)
            if not bool(GameModel.query.filter_by(GID=gameData['metadata']['matchId']).first()):
                newGame = GameModel(
                    GID=gameData['metadata']['matchId'],
                    patch=gameData['info']['gameVersion'],
                    
                    time_start=gameData['info']['gameStartTimestamp'],
                    time_end=gameData['info']['gameEndTimestamp'],
                    
                    p0_PUUID=gameData['metadata']['participants'][0],
                    p1_PUUID=gameData['metadata']['participants'][1],
                    p2_PUUID=gameData['metadata']['participants'][2],
                    p3_PUUID=gameData['metadata']['participants'][3],
                    p4_PUUID=gameData['metadata']['participants'][4],
                    p5_PUUID=gameData['metadata']['participants'][5],
                    p6_PUUID=gameData['metadata']['participants'][6],
                    p7_PUUID=gameData['metadata']['participants'][7],
                    p8_PUUID=gameData['metadata']['participants'][8],
                    p9_PUUID=gameData['metadata']['participants'][9],
                    
                    
                    
                    p0_item0=gameData['info']['participants'][0]['item0'],
                    p0_item1=gameData['info']['participants'][0]['item1'],
                    p0_item2=gameData['info']['participants'][0]['item2'],
                    p0_item3=gameData['info']['participants'][0]['item3'],
                    p0_item4=gameData['info']['participants'][0]['item4'],
                    p0_item5=gameData['info']['participants'][0]['item5'],
                    p0_item6=gameData['info']['participants'][0]['item6'],

                    p0_summoner1ID=gameData['info']['participants'][0]['summoner1Id'],
                    p0_summoner2ID=gameData['info']['participants'][0]['summoner2Id'],

                    p0_kills=gameData['info']['participants'][0]['kills'],
                    p0_deaths=gameData['info']['participants'][0]['deaths'],
                    p0_assists=gameData['info']['participants'][0]['assists'],
                    
                    p0_true_damage=gameData['info']['participants'][0]['trueDamageDealtToChampions'],
                    p0_ad_damage=gameData['info']['participants'][0]['totalDamageDealtToChampions'],
                    p0_magic_damage=gameData['info']['participants'][0]['magicDamageDealtToChampions'],

                    p0_position=gameData['info']['participants'][0]['teamPosition'],

                    p0_gold_earned=gameData['info']['participants'][0]['goldEarned'],
                    p0_gold_spent=gameData['info']['participants'][0]['goldSpent'],

                    p0_CID=gameData['info']['participants'][0]['championId'],
                    p0_champion_name=gameData['info']['participants'][0]['championName'],

                    p0_total_minions=gameData['info']['participants'][0]['totalMinionsKilled'],

                    p0_vision_score=gameData['info']['participants'][0]['visionScore'],
                    
                    p0_won_game=gameData['info']['participants'][0]['win'],
                    
                    
                    p1_item0=gameData['info']['participants'][1]['item0'],
                    p1_item1=gameData['info']['participants'][1]['item1'],
                    p1_item2=gameData['info']['participants'][1]['item2'],
                    p1_item3=gameData['info']['participants'][1]['item3'],
                    p1_item4=gameData['info']['participants'][1]['item4'],
                    p1_item5=gameData['info']['participants'][1]['item5'],
                    p1_item6=gameData['info']['participants'][1]['item6'],

                    p1_summoner1ID=gameData['info']['participants'][1]['summoner1Id'],
                    p1_summoner2ID=gameData['info']['participants'][1]['summoner2Id'],

                    p1_kills=gameData['info']['participants'][1]['kills'],
                    p1_deaths=gameData['info']['participants'][1]['deaths'],
                    p1_assists=gameData['info']['participants'][1]['assists'],

                    p1_true_damage=gameData['info']['participants'][1]['trueDamageDealtToChampions'],
                    p1_ad_damage=gameData['info']['participants'][1]['totalDamageDealtToChampions'],
                    p1_magic_damage=gameData['info']['participants'][1]['magicDamageDealtToChampions'],

                    p1_position=gameData['info']['participants'][1]['teamPosition'],

                    p1_gold_earned=gameData['info']['participants'][1]['goldEarned'],
                    p1_gold_spent=gameData['info']['participants'][1]['goldSpent'],

                    p1_CID=gameData['info']['participants'][1]['championId'],
                    p1_champion_name=gameData['info']['participants'][1]['championName'],

                    p1_total_minions=gameData['info']['participants'][1]['totalMinionsKilled'],

                    p1_vision_score=gameData['info']['participants'][1]['visionScore'],
                    
                    p1_won_game=gameData['info']['participants'][1]['win'],


                    p2_item0=gameData['info']['participants'][2]['item0'],
                    p2_item1=gameData['info']['participants'][2]['item1'],
                    p2_item2=gameData['info']['participants'][2]['item2'],
                    p2_item3=gameData['info']['participants'][2]['item3'],
                    p2_item4=gameData['info']['participants'][2]['item4'],
                    p2_item5=gameData['info']['participants'][2]['item5'],
                    p2_item6=gameData['info']['participants'][2]['item6'],

                    p2_summoner1ID=gameData['info']['participants'][2]['summoner1Id'],
                    p2_summoner2ID=gameData['info']['participants'][2]['summoner2Id'],

                    p2_kills=gameData['info']['participants'][2]['kills'],
                    p2_deaths=gameData['info']['participants'][2]['deaths'],
                    p2_assists=gameData['info']['participants'][2]['assists'],

                    p2_true_damage=gameData['info']['participants'][2]['trueDamageDealtToChampions'],
                    p2_ad_damage=gameData['info']['participants'][2]['totalDamageDealtToChampions'],
                    p2_magic_damage=gameData['info']['participants'][2]['magicDamageDealtToChampions'],

                    p2_position=gameData['info']['participants'][2]['teamPosition'],

                    p2_gold_earned=gameData['info']['participants'][2]['goldEarned'],
                    p2_gold_spent=gameData['info']['participants'][2]['goldSpent'],

                    p2_CID=gameData['info']['participants'][2]['championId'],
                    p2_champion_name=gameData['info']['participants'][2]['championName'],

                    p2_total_minions=gameData['info']['participants'][2]['totalMinionsKilled'],

                    p2_vision_score=gameData['info']['participants'][2]['visionScore'],
                    
                    p2_won_game=gameData['info']['participants'][2]['win'],


                    p3_item0=gameData['info']['participants'][3]['item0'],
                    p3_item1=gameData['info']['participants'][3]['item1'],
                    p3_item2=gameData['info']['participants'][3]['item2'],
                    p3_item3=gameData['info']['participants'][3]['item3'],
                    p3_item4=gameData['info']['participants'][3]['item4'],
                    p3_item5=gameData['info']['participants'][3]['item5'],
                    p3_item6=gameData['info']['participants'][3]['item6'],

                    p3_summoner1ID=gameData['info']['participants'][3]['summoner1Id'],
                    p3_summoner2ID=gameData['info']['participants'][3]['summoner2Id'],

                    p3_kills=gameData['info']['participants'][3]['kills'],
                    p3_deaths=gameData['info']['participants'][3]['deaths'],
                    p3_assists=gameData['info']['participants'][3]['assists'],

                    p3_true_damage=gameData['info']['participants'][3]['trueDamageDealtToChampions'],
                    p3_ad_damage=gameData['info']['participants'][3]['totalDamageDealtToChampions'],
                    p3_magic_damage=gameData['info']['participants'][3]['magicDamageDealtToChampions'],
                    
                    p3_position=gameData['info']['participants'][3]['teamPosition'],

                    p3_gold_earned=gameData['info']['participants'][3]['goldEarned'],
                    p3_gold_spent=gameData['info']['participants'][3]['goldSpent'],

                    p3_CID=gameData['info']['participants'][3]['championId'],
                    p3_champion_name=gameData['info']['participants'][3]['championName'],

                    p3_total_minions=gameData['info']['participants'][3]['totalMinionsKilled'],

                    p3_vision_score=gameData['info']['participants'][3]['visionScore'],
                    
                    p3_won_game=gameData['info']['participants'][3]['win'],


                    p4_item0=gameData['info']['participants'][4]['item0'],
                    p4_item1=gameData['info']['participants'][4]['item1'],
                    p4_item2=gameData['info']['participants'][4]['item2'],
                    p4_item3=gameData['info']['participants'][4]['item3'],
                    p4_item4=gameData['info']['participants'][4]['item4'],
                    p4_item5=gameData['info']['participants'][4]['item5'],
                    p4_item6=gameData['info']['participants'][4]['item6'],

                    p4_summoner1ID=gameData['info']['participants'][4]['summoner1Id'],
                    p4_summoner2ID=gameData['info']['participants'][4]['summoner2Id'],

                    p4_kills=gameData['info']['participants'][4]['kills'],
                    p4_deaths=gameData['info']['participants'][4]['deaths'],
                    p4_assists=gameData['info']['participants'][4]['assists'],

                    p4_true_damage=gameData['info']['participants'][4]['trueDamageDealtToChampions'],
                    p4_ad_damage=gameData['info']['participants'][4]['totalDamageDealtToChampions'],
                    p4_magic_damage=gameData['info']['participants'][4]['magicDamageDealtToChampions'],

                    p4_position=gameData['info']['participants'][4]['teamPosition'],
                    
                    p4_gold_earned=gameData['info']['participants'][4]['goldEarned'],
                    p4_gold_spent=gameData['info']['participants'][4]['goldSpent'],

                    p4_CID=gameData['info']['participants'][4]['championId'],
                    p4_champion_name=gameData['info']['participants'][4]['championName'],

                    p4_total_minions=gameData['info']['participants'][4]['totalMinionsKilled'],

                    p4_vision_score=gameData['info']['participants'][4]['visionScore'],
                    
                    p4_won_game=gameData['info']['participants'][4]['win'],
                    
                    
                    p5_item0=gameData['info']['participants'][5]['item0'],
                    p5_item1=gameData['info']['participants'][5]['item1'],
                    p5_item2=gameData['info']['participants'][5]['item2'],
                    p5_item3=gameData['info']['participants'][5]['item3'],
                    p5_item4=gameData['info']['participants'][5]['item4'],
                    p5_item5=gameData['info']['participants'][5]['item5'],
                    p5_item6=gameData['info']['participants'][5]['item6'],

                    p5_summoner1ID=gameData['info']['participants'][5]['summoner1Id'],
                    p5_summoner2ID=gameData['info']['participants'][5]['summoner2Id'],

                    p5_kills=gameData['info']['participants'][5]['kills'],
                    p5_deaths=gameData['info']['participants'][5]['deaths'],
                    p5_assists=gameData['info']['participants'][5]['assists'],
                    
                    p5_true_damage=gameData['info']['participants'][5]['trueDamageDealtToChampions'],
                    p5_ad_damage=gameData['info']['participants'][5]['totalDamageDealtToChampions'],
                    p5_magic_damage=gameData['info']['participants'][5]['magicDamageDealtToChampions'],
                    
                    p5_position=gameData['info']['participants'][5]['teamPosition'],
                    
                    p5_gold_earned=gameData['info']['participants'][5]['goldEarned'],
                    p5_gold_spent=gameData['info']['participants'][5]['goldSpent'],
                    
                    p5_CID=gameData['info']['participants'][5]['championId'],
                    p5_champion_name=gameData['info']['participants'][5]['championName'],
                    
                    p5_total_minions=gameData['info']['participants'][5]['totalMinionsKilled'],
                    
                    p5_vision_score=gameData['info']['participants'][5]['visionScore'],
                    
                    p5_won_game=gameData['info']['participants'][5]['win'],
                    
                    
                    p6_item0=gameData['info']['participants'][6]['item0'],
                    p6_item1=gameData['info']['participants'][6]['item1'],
                    p6_item2=gameData['info']['participants'][6]['item2'],
                    p6_item3=gameData['info']['participants'][6]['item3'],
                    p6_item4=gameData['info']['participants'][6]['item4'],
                    p6_item5=gameData['info']['participants'][6]['item5'],
                    p6_item6=gameData['info']['participants'][6]['item6'],

                    p6_summoner1ID=gameData['info']['participants'][6]['summoner1Id'],
                    p6_summoner2ID=gameData['info']['participants'][6]['summoner2Id'],

                    p6_kills=gameData['info']['participants'][6]['kills'],
                    p6_deaths=gameData['info']['participants'][6]['deaths'],
                    p6_assists=gameData['info']['participants'][6]['assists'],
                    
                    p6_true_damage=gameData['info']['participants'][6]['trueDamageDealtToChampions'],
                    p6_ad_damage=gameData['info']['participants'][6]['totalDamageDealtToChampions'],
                    p6_magic_damage=gameData['info']['participants'][6]['magicDamageDealtToChampions'],

                    p6_position=gameData['info']['participants'][6]['teamPosition'],

                    p6_gold_earned=gameData['info']['participants'][6]['goldEarned'],
                    p6_gold_spent=gameData['info']['participants'][6]['goldSpent'],

                    p6_CID=gameData['info']['participants'][6]['championId'],
                    p6_champion_name=gameData['info']['participants'][6]['championName'],

                    p6_total_minions=gameData['info']['participants'][6]['totalMinionsKilled'],

                    p6_vision_score=gameData['info']['participants'][6]['visionScore'],
                    
                    p6_won_game=gameData['info']['participants'][6]['win'],


                    p7_item0=gameData['info']['participants'][7]['item0'],
                    p7_item1=gameData['info']['participants'][7]['item1'],
                    p7_item2=gameData['info']['participants'][7]['item2'],
                    p7_item3=gameData['info']['participants'][7]['item3'],
                    p7_item4=gameData['info']['participants'][7]['item4'],
                    p7_item5=gameData['info']['participants'][7]['item5'],
                    p7_item6=gameData['info']['participants'][7]['item6'],

                    p7_summoner1ID=gameData['info']['participants'][7]['summoner1Id'],
                    p7_summoner2ID=gameData['info']['participants'][7]['summoner2Id'],

                    p7_kills=gameData['info']['participants'][7]['kills'],
                    p7_deaths=gameData['info']['participants'][7]['deaths'],
                    p7_assists=gameData['info']['participants'][7]['assists'],

                    p7_true_damage=gameData['info']['participants'][7]['trueDamageDealtToChampions'],
                    p7_ad_damage=gameData['info']['participants'][7]['totalDamageDealtToChampions'],
                    p7_magic_damage=gameData['info']['participants'][7]['magicDamageDealtToChampions'],

                    p7_position=gameData['info']['participants'][7]['teamPosition'],

                    p7_gold_earned=gameData['info']['participants'][7]['goldEarned'],
                    p7_gold_spent=gameData['info']['participants'][7]['goldSpent'],

                    p7_CID=gameData['info']['participants'][7]['championId'],
                    p7_champion_name=gameData['info']['participants'][7]['championName'],

                    p7_total_minions=gameData['info']['participants'][7]['totalMinionsKilled'],

                    p7_vision_score=gameData['info']['participants'][7]['visionScore'],
                    
                    p7_won_game=gameData['info']['participants'][7]['win'],


                    p8_item0=gameData['info']['participants'][8]['item0'],
                    p8_item1=gameData['info']['participants'][8]['item1'],
                    p8_item2=gameData['info']['participants'][8]['item2'],
                    p8_item3=gameData['info']['participants'][8]['item3'],
                    p8_item4=gameData['info']['participants'][8]['item4'],
                    p8_item5=gameData['info']['participants'][8]['item5'],
                    p8_item6=gameData['info']['participants'][8]['item6'],

                    p8_summoner1ID=gameData['info']['participants'][8]['summoner1Id'],
                    p8_summoner2ID=gameData['info']['participants'][8]['summoner2Id'],

                    p8_kills=gameData['info']['participants'][8]['kills'],
                    p8_deaths=gameData['info']['participants'][8]['deaths'],
                    p8_assists=gameData['info']['participants'][8]['assists'],

                    p8_true_damage=gameData['info']['participants'][8]['trueDamageDealtToChampions'],
                    p8_ad_damage=gameData['info']['participants'][8]['totalDamageDealtToChampions'],
                    p8_magic_damage=gameData['info']['participants'][8]['magicDamageDealtToChampions'],

                    p8_position=gameData['info']['participants'][8]['teamPosition'],

                    p8_gold_earned=gameData['info']['participants'][8]['goldEarned'],
                    p8_gold_spent=gameData['info']['participants'][8]['goldSpent'],

                    p8_CID=gameData['info']['participants'][8]['championId'],
                    p8_champion_name=gameData['info']['participants'][8]['championName'],

                    p8_total_minions=gameData['info']['participants'][8]['totalMinionsKilled'],

                    p8_vision_score=gameData['info']['participants'][8]['visionScore'],
                    
                    p8_won_game=gameData['info']['participants'][8]['win'],


                    p9_item0=gameData['info']['participants'][9]['item0'],
                    p9_item1=gameData['info']['participants'][9]['item1'],
                    p9_item2=gameData['info']['participants'][9]['item2'],
                    p9_item3=gameData['info']['participants'][9]['item3'],
                    p9_item4=gameData['info']['participants'][9]['item4'],
                    p9_item5=gameData['info']['participants'][9]['item5'],
                    p9_item6=gameData['info']['participants'][9]['item6'],

                    p9_summoner1ID=gameData['info']['participants'][9]['summoner1Id'],
                    p9_summoner2ID=gameData['info']['participants'][9]['summoner2Id'],

                    p9_kills=gameData['info']['participants'][9]['kills'],
                    p9_deaths=gameData['info']['participants'][9]['deaths'],
                    p9_assists=gameData['info']['participants'][9]['assists'],

                    p9_true_damage=gameData['info']['participants'][9]['trueDamageDealtToChampions'],
                    p9_ad_damage=gameData['info']['participants'][9]['totalDamageDealtToChampions'],
                    p9_magic_damage=gameData['info']['participants'][9]['magicDamageDealtToChampions'],
                    
                    p9_position=gameData['info']['participants'][9]['teamPosition'],

                    p9_gold_earned=gameData['info']['participants'][9]['goldEarned'],
                    p9_gold_spent=gameData['info']['participants'][9]['goldSpent'],

                    p9_CID=gameData['info']['participants'][9]['championId'],
                    p9_champion_name=gameData['info']['participants'][9]['championName'],

                    p9_total_minions=gameData['info']['participants'][9]['totalMinionsKilled'],

                    p9_vision_score=gameData['info']['participants'][9]['visionScore'],
                    
                    p9_won_game=gameData['info']['participants'][9]['win'],
                )
                
                db.session.add(newGame)
                
                for _ in range(10):
                    played = PlayedGame(
                        user_id=gameData['info']['participants'][_]['puuid'],
                        game_id=gameData['metadata']['matchId'],
                        
                        time_start=gameData['info']['gameStartTimestamp'],
                        time_end=gameData['info']['gameEndTimestamp'],
                        
                        patch=gameData['info']['gameVersion']
                    )
                    db.session.add(played)
        
        db.session.commit()
        return 201        

api.add_resource(GameDataLast20, "/game-data/last-20/<PUUID>")


if __name__ == "__main__":
    app.run(debug = True) #CHANGE BEFORE PRODUCTION