from flask import Flask

from flask_restful import Api, Resource, fields, marshal_with

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from sqlalchemy import func

import os
import time
import sys

from accessRiotApi import (
    getMatchByMatchID, getMatchXtoX, getMatchTimeLineByMatchID, getSummonerByName, 
    getSummonerByPUUID, getLeagueInfoBySID, getACCTInfoByRiotID, getAccountByPUUID
)

basedir = os.path.abspath(os.path.dirname(__file__)) + "/data/"

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

#
#Database Declarations
#
class PlayedGame(db.Model):
    __tablename__ = 'Played_Game'
    PUUID = db.Column(db.String, db.ForeignKey('User.PUUID'), primary_key=True)
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    
    name = db.Column(db.String, nullable=False)
    
    riotIdGameName = db.Column(db.String, nullable=False)
    riotIdTagline = db.Column(db.String, nullable=False)
    
    summonerId = db.Column(db.Integer, nullable=True)
    summonerLevel = db.Column(db.Integer, nullable=True)
    
    firstBloodAssist = db.Column(db.Boolean, nullable=True)
    firstBloodKill = db.Column(db.Boolean, nullable=True)
    
    firstTowerAssist = db.Column(db.Boolean, nullable=True)
    firstTowerKill = db.Column(db.Boolean, nullable=True)
    
    bountyLevel = db.Column(db.Integer, nullable=True)
    longestTimeSpentLiving = db.Column(db.Integer, nullable=True)
    
    killingSprees = db.Column(db.Integer, nullable=True)
    largestKillingSpree = db.Column(db.Integer, nullable=True)
    largestMultiKill = db.Column(db.Integer, nullable=True)
    
    doubleKills = db.Column(db.Integer, nullable=True)
    tripleKills = db.Column(db.Integer, nullable=True)
    quadraKills = db.Column(db.Integer, nullable=True)
    pentaKills = db.Column(db.Integer, nullable=True)
    unrealKills = db.Column(db.Integer, nullable=True)
    
    largestCriticalStrike = db.Column(db.Integer, nullable=True)
    
    damageDealtToBuildings = db.Column(db.Integer, nullable=True)
    damageDealtToObjectives = db.Column(db.Integer, nullable=True)
    damageDealtToTurrets = db.Column(db.Integer, nullable=True)
    
    damageSelfMitigated = db.Column(db.Integer, nullable=True)
    
    magicDamageDealt = db.Column(db.Integer, nullable=True)
    magicDamageDealtToChampions = db.Column(db.Integer, nullable=True)
    magicDamageTaken = db.Column(db.Integer, nullable=True)
    
    physicalDamageDealt = db.Column(db.Integer, nullable=True)
    physicalDamageDealtToChampions = db.Column(db.Integer, nullable=True)
    physicalDamageTaken = db.Column(db.Integer, nullable=True)
    
    trueDamageDealt = db.Column(db.Integer, nullable=True)
    trueDamageDealtToChampions = db.Column(db.Integer, nullable=True)
    trueDamageTaken = db.Column(db.Integer, nullable=True)
    
    totalDamageDealt = db.Column(db.Integer, nullable=True)
    totalDamageDealtToChampions = db.Column(db.Integer, nullable=True)
    totalDamageTaken = db.Column(db.Integer, nullable=True)
    totalDamageShieldedOnTeammates = db.Column(db.Integer, nullable=True)
    
    totalHeal = db.Column(db.Integer, nullable=True)
    totalHealsOnTeammates = db.Column(db.Integer, nullable=True)
    totalUnitsHealed = db.Column(db.Integer, nullable=True)
    
    timeCCingOthers = db.Column(db.Integer, nullable=True)
    totalTimeCCDealt = db.Column(db.Integer, nullable=True)
    totalTimeSpentDead = db.Column(db.Integer, nullable=True)
    
    spell1Casts = db.Column(db.Integer, nullable=True)
    spell2Casts = db.Column(db.Integer, nullable=True)
    spell3Casts = db.Column(db.Integer, nullable=True)
    spell4Casts = db.Column(db.Integer, nullable=True)
    
    summoner1Casts = db.Column(db.Integer, nullable=True)
    summoner1Id = db.Column(db.Integer, nullable=True)
    
    summoner2Casts = db.Column(db.Integer, nullable=True)
    summoner2Id = db.Column(db.Integer, nullable=True)

    neutralMinionsKilled = db.Column(db.Integer, nullable=True)
    totalMinionsKilled = db.Column(db.Integer, nullable=True)

    baronKills = db.Column(db.Integer, nullable=True)
    dragonKills = db.Column(db.Integer, nullable=True)
    
    inhibitorKills = db.Column(db.Integer, nullable=True)
    inhibitorTakedowns = db.Column(db.Integer, nullable=True)
    inhibitorsLost = db.Column(db.Integer, nullable=True)

    turretKills = db.Column(db.Integer, nullable=True)
    turretTakedowns = db.Column(db.Integer, nullable=True)
    turretsLost = db.Column(db.Integer, nullable=True)
    
    nexusKills = db.Column(db.Integer, nullable=True)
    nexusTakedowns = db.Column(db.Integer, nullable=True)
    nexusLost = db.Column(db.Integer, nullable=True)
    
    objectivesStolen = db.Column(db.Integer, nullable=True)
    objectivesStolenAssists = db.Column(db.Integer, nullable=True)
    
    visionScore = db.Column(db.Integer, nullable=True)
    visionWardsBoughtInGame = db.Column(db.Integer, nullable=True)
    wardsKilled = db.Column(db.Integer, nullable=True)
    wardsPlaced = db.Column(db.Integer, nullable=True)
    detectorWardsPlaced = db.Column(db.Integer, nullable=True)
    sightWardsBoughtInGame = db.Column(db.Integer, nullable=True)
    
    position = db.Column(db.String, nullable=False)
    CID = db.Column(db.Integer, db.ForeignKey('Champion.CID'), nullable=False)
    championName = db.Column(db.String, nullable=True)
    
    champExperience = db.Column(db.Integer, nullable=True)
    champLevel = db.Column(db.Integer, nullable=True)
    
    kills = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    
    goldEarned = db.Column(db.Integer, nullable=False)
    goldSpent = db.Column(db.Integer, nullable=False)
    
    itemsPurchased = db.Column(db.Integer, nullable=True)
    consumablesPurchased = db.Column(db.Integer, nullable=True)
    
    item0 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item1 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item2 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item3 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item4 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item5 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    item6 = db.Column(db.Integer, db.ForeignKey('Item.IID'), nullable=True)
    
    timePlayed = db.Column(db.Integer, nullable=True)
    
    gameEndedInEarlySurrender = db.Column(db.Boolean, nullable=True)
    gameEndedInSurrender = db.Column(db.Boolean, nullable=True)
    teamEarlySurrendered = db.Column(db.Integer, nullable=True)
    
    won = db.Column(db.Boolean, nullable=True)

    user = db.relationship('UserModel', back_populates = 'games')
    game = db.relationship('GameModel', back_populates = 'users')


class UserModel(db.Model):
    __tablename__ = 'User'
    PUUID = db.Column(db.String, primary_key=True)
    SID = db.Column(db.String, nullable=False)

    tagLine=db.Column(db.String, nullable=False)
    gameName=db.Column(db.String, nullable=False)

    name = db.Column(db.String, nullable=False)
    profileIcon = db.Column(db.Integer, nullable=True)
    
    tier = db.Column(db.String, nullable=True)
    rank = db.Column(db.String, nullable=True)
    
    wins = db.Column(db.Integer, nullable=True)
    losses = db.Column(db.Integer, nullable=True)
    
    revisionDate = db.Column(db.Integer, nullable=False)
    
    games = db.relationship('PlayedGame', back_populates = 'user')
    player_frame = db.relationship('PlayerFrame', back_populates = 'user')
    
    
    def to_dict(self):
        return {
            'PUUID': self.PUUID,
            'SID': self.SID,

            'tagLine': self.tagLine,
            'gameName': self.gameName,

            'name': self.name,
            'profileIcon': self.profileIcon,

            'tier': self.tier,
            'rank': self.rank,

            'wins': self.wins,
            'losses': self.losses,

            'revisionDate': self.revisionDate
        }


class GameModel(db.Model):
    __tablename__ = 'Game'
    GID = db.Column(db.String, primary_key=True)
    
    time_start = db.Column(db.Integer, nullable=False)
    time_end = db.Column(db.Integer, nullable=True)
    
    season = db.Column(db.Integer, nullable=False)
    patch = db.Column(db.String, nullable=False)
    
    users = db.relationship('PlayedGame', back_populates = 'game')
    time_line = db.relationship('GameTimeLine', back_populates = 'game')
    entry_number = db.relationship('TimeLineEntry', back_populates = 'game')
    player_frame = db.relationship('PlayerFrame', back_populates = 'game')
    event = db.relationship('Event', back_populates = 'game')

  
class GameTimeLine(db.Model):
    __tablename__ = 'Time_Line'
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    
    dataVersion = db.Column(db.Integer, nullable=False)
    
    frameInterval = db.Column(db.Integer, nullable=False)
    numFrames = db.Column(db.Integer, nullable=False)
    
    game = db.relationship('GameModel', back_populates = 'time_line')


class TimeLineEntry(db.Model):
    __tablename__ = 'Time_Line_Entry'
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    entryNumber = db.Column(db.Integer, primary_key=True)
    
    timestamp = db.Column(db.Integer, nullable=False)
    
    game = db.relationship('GameModel', back_populates = 'entry_number')
    player_frame = db.relationship('PlayerFrame', back_populates = 'entry_number')
    event = db.relationship('Event', back_populates = 'entry_number')


class PlayerFrame(db.Model):
    __tablename__ = 'Player_Frame'
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    entryNumber = db.Column(db.Integer, db.ForeignKey('Time_Line_Entry.entryNumber'), primary_key=True)
    PUUID = db.Column(db.String, db.ForeignKey('User.PUUID'), primary_key=True)
    
    #Personal Stats
    abilityHaste = db.Column(db.Integer, nullable=True)
    abilityPower = db.Column(db.Integer, nullable=True)
    armor = db.Column(db.Integer, nullable=True)
    armorPen = db.Column(db.Integer, nullable=True)
    armorPenPercent = db.Column(db.Integer, nullable=True)
    attackDamage = db.Column(db.Integer, nullable=True)
    attackSpeed = db.Column(db.Integer, nullable=True)
    bonusArmorPenPercent = db.Column(db.Integer, nullable=True)
    bonusMagicPenPercent = db.Column(db.Integer, nullable=True)
    ccReduction = db.Column(db.Integer, nullable=True)
    cooldownReduction = db.Column(db.Integer, nullable=True)
    health = db.Column(db.Integer, nullable=True)
    healthMax = db.Column(db.Integer, nullable=True)
    healthRegen = db.Column(db.Integer, nullable=True)
    lifesteal = db.Column(db.Integer, nullable=True)
    magicPen = db.Column(db.Integer, nullable=True)
    magicPenPercent = db.Column(db.Integer, nullable=True)
    magicResist = db.Column(db.Integer, nullable=True)
    movementSpeed = db.Column(db.Integer, nullable=True)
    omnivamp = db.Column(db.Integer, nullable=True)
    physicalVamp = db.Column(db.Integer, nullable=True)
    power = db.Column(db.Integer, nullable=True)
    powerMax = db.Column(db.Integer, nullable=True)
    powerRegen = db.Column(db.Integer, nullable=True)
    spellVamp = db.Column(db.Integer, nullable=True)
    
    #Damage Stats
    magicDamageDone = db.Column(db.Integer, nullable=True)
    magicDamageDoneToChampions = db.Column(db.Integer, nullable=True)
    magicDamageTaken = db.Column(db.Integer, nullable=True)
    
    physicalDamageDone = db.Column(db.Integer, nullable=True)
    physicalDamageDoneToChampions = db.Column(db.Integer, nullable=True)
    physicalDamageTaken = db.Column(db.Integer, nullable=True)
    
    trueDamageDone = db.Column(db.Integer, nullable=True)
    trueDamageDoneToChampions = db.Column(db.Integer, nullable=True)
    trueDamageTaken = db.Column(db.Integer, nullable=True)
    
    totalDamageDone = db.Column(db.Integer, nullable=True)
    totalDamageDoneToChampions = db.Column(db.Integer, nullable=True)
    totalDamageTaken = db.Column(db.Integer, nullable=True)
    
    #Other Stats
    currentGold = db.Column(db.Integer, nullable=True)
    goldPerSecond = db.Column(db.Integer, nullable=True)
    totalGold = db.Column(db.Integer, nullable=True)
    
    jungleMinionsKilled = db.Column(db.Integer, nullable=True)
    minionsKilled = db.Column(db.Integer, nullable=True)
    
    level = db.Column(db.Integer, nullable=True)
    xp = db.Column(db.Integer, nullable=True)
    
    timeEnemySpentControlled = db.Column(db.Integer, nullable=True)
    
    game = db.relationship('GameModel', back_populates = 'player_frame')
    user = db.relationship('UserModel', back_populates = 'player_frame')
    entry_number = db.relationship('TimeLineEntry', back_populates = 'player_frame')

  
class Event(db.Model):
    __tablename__ = 'Event'
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    entryNumber = db.Column(db.Integer, db.ForeignKey('Time_Line_Entry.entryNumber'), primary_key=True)
    eventNumber = db.Column(db.Integer, primary_key=True)
    
    timestamp = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    game = db.relationship('GameModel', back_populates = 'event')
    entry_number = db.relationship('TimeLineEntry', back_populates = 'event')


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


#
#Api Methods
#


resource_fields = {
    'PUUID': fields.String,
    'SID': fields.String,
    
    'tagLine': fields.String,
    'gameName': fields.String,
    
    'name': fields.String,
    'profileIcon': fields.Integer,
    
    'tier': fields.String,
    'rank': fields.String,
    
    'wins': fields.Integer,
    'losses': fields.Integer,

    'revisionDate': fields.Integer
}   


class UserByRiotID(Resource):
    @marshal_with(resource_fields)
    def get(self, tagLine, gameName):
        if not bool(UserModel.query.filter_by(tagLine=tagLine, gameName=gameName).first()):
            status = self.put(tagLine, gameName)
            if status != 201:
                return status

        result = UserModel.query.filter_by(tagLine=tagLine, gameName=gameName).first()

        return result, 200

    def put(self, tagLine, gameName):
        userAccountInfo = getACCTInfoByRiotID(tagLine, gameName)
        userData = getSummonerByPUUID(userAccountInfo['puuid'])
        userLeagueInfo = getLeagueInfoBySID(userData['id'])
        
        if bool(UserModel.query.filter_by(PUUID=(userData['puuid'])).first()):
            db.session.delete(UserModel.query.filter_by(PUUID=(userData['puuid'])).first())
            db.session.commit()
        
        for item in userLeagueInfo:
            if item['queueType'] == 'RANKED_SOLO_5x5':
                userLeagueInfo = item
                break
        
        newUser = createUser(userData, userLeagueInfo, userAccountInfo)
        
        db.session.add(newUser)
        db.session.commit()
        
        return 201
    
api.add_resource(UserByRiotID, "/user/by-riotID/<tagLine>/<gameName>")


class UserByName(Resource):
    @marshal_with(resource_fields)
    def get(self, name):
        if not bool(UserModel.query.filter_by(name=name).first()):
            status = self.put(name)
            if status != 201:
                return status
            
        result = UserModel.query.filter_by(name=name).first()

        return result, 200

    def put(self, name):
        userData = getSummonerByName(name)
        userLeagueInfo = getLeagueInfoBySID(userData['id'])
        userAccountInfo = getAccountByPUUID(userData['puuid'])
        
        if bool(UserModel.query.filter_by(PUUID=(userData['puuid'])).first()):
            db.session.delete(UserModel.query.filter_by(PUUID=(userData['puuid'])).first())
            db.session.commit()
        
        for item in userLeagueInfo:
            if item['queueType'] == 'RANKED_SOLO_5x5':
                userLeagueInfo = item
                break
        
        newUser = createUser(userData, userLeagueInfo, userAccountInfo)
        
        db.session.add(newUser)
        db.session.commit()
        
        return 201

api.add_resource(UserByName, "/user/by-name/<name>")


class UserByPUUID(Resource):
    @marshal_with(resource_fields)
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            status = self.put(PUUID)
            if status != 201:
                return status
            
        result = UserModel.query.filter_by(PUUID=PUUID).first()

        return result, 200
    
    def put(self, PUUID):
        if bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            db.session.delete(UserModel.query.filter_by(PUUID=PUUID).first())
            db.session.commit()
        
        userData = getSummonerByPUUID(PUUID)
        userLeagueInfo = getLeagueInfoBySID(userData['id'])
        userAccountInfo = getAccountByPUUID(userData['puuid'])
        
        for item in userLeagueInfo:
            if item['queueType'] == 'RANKED_SOLO_5x5':
                userLeagueInfo = item
                break
        
        newUser = createUser(userData, userLeagueInfo, userAccountInfo)
        
        db.session.add(newUser)
        db.session.commit()
        
        return 201

api.add_resource(UserByPUUID, "/user/by-PUUID/<PUUID>")


class GameDataByPlayer(Resource):
    def get(self, GID, PUUID):
        if not bool(GameModel.query.filter_by(GID=GID).first()):
            return 404

        gameData = GameModel.query.filter_by(GID=GID).first()
        playerData = PlayedGame.query.filter_by(GID=GID, PUUID=PUUID).first()
        
        playerStats = getPlayerStats(gameData, playerData)
        
        return playerStats, 200      

api.add_resource(GameDataByPlayer, "/game-data/by-Player/<GID>/<PUUID>")


class GameDataAll(Resource):
    def get(self, GID):
        if not bool(GameModel.query.filter_by(GID=GID).first()):
            return 404
        
        players = getPlayersInGame(GID)
        
        gameData = GameModel.query.filter_by(GID=GID).first()
        
        allGameData = {}
        
        for player in players:
            
            playerData = PlayedGame.query.filter_by(GID=GID, PUUID=player).first()
            playerDataDict = getPlayerStats(gameData, playerData)
            
            allGameData[player] = playerDataDict
        
        return allGameData, 200
     
api.add_resource(GameDataAll, "/game-data/all/<GID>")


class GameIDLast20(Resource):
    def get(self, PUUID):
        result = db.session.query(GameModel.GID).select_from(GameModel).join(PlayedGame).filter(GameModel.GID == PlayedGame.GID).filter(PlayedGame.PUUID == PUUID).order_by(GameModel.time_start.desc()).limit(20).all()
        result = [game[0] for game in result]
        
        return result, 200

api.add_resource(GameIDLast20, "/game-id/last-20/<PUUID>")


#TODO Fix to work with the addition of games more recent than those in our database
#UPDATE FUNCTION ADDED MAY FIX THIS
class GameIDXtoX(Resource):
    def get(self, PUUID, x, y):
        numEntries = PlayedGame.query.filter_by(PUUID=PUUID).count()
        if int(y) > numEntries:
            matchIds = getMatchXtoX(PUUID, int(numEntries), int(y))
            addGames(matchIds)

        result = db.session.query(GameModel.GID).select_from(GameModel).join(PlayedGame).filter(GameModel.GID == PlayedGame.GID).filter(PlayedGame.PUUID == PUUID).order_by(GameModel.time_start.desc()).offset(x).limit(y).all()
        result = [game[0] for game in result]

        return result, 200

api.add_resource(GameIDXtoX, "/game-id/x-x/<PUUID>/<x>/<y>")


class GameDataXtoX(Resource):
    def put(self, PUUID, x, y):
        gameIds = getMatchXtoX(PUUID, int(x), int(y))
        return addGames(gameIds)

api.add_resource(GameDataXtoX, "/game-data/x-x/<PUUID>/<x>/<y>")


class UpdateUser(Resource):
    def put(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404
        
        if not bool(PlayedGame.query.filter_by(PUUID=PUUID).first()):
            try:
                gameIds = getMatchXtoX(PUUID, 0, 20)
                addGames(gameIds)
            except Exception:
                return 500
            return 201
        
        try:
            userData = getSummonerByPUUID(PUUID)
            userLeagueInfo = getLeagueInfoBySID(userData['id'])
            userAccountInfo = getAccountByPUUID(PUUID)
        except Exception:
            return 500
        
        for item in userLeagueInfo:
            if item['queueType'] == 'RANKED_SOLO_5x5':
                userLeagueInfo = item
                break

        updatedUser = createUser(userData, userLeagueInfo, userAccountInfo)
        db.session.execute(
            update(UserModel).where(UserModel.PUUID == PUUID).values(updatedUser.to_dict())
        )
        db.session.commit()

        #Get Game Data
        toUpdate = []
        
        updateIndex = 0
        gettingNew = True
        while(gettingNew):
            try:
                games = getMatchXtoX(PUUID, updateIndex, updateIndex + 100)
            except Exception:
                return 500
            
            for item in games:
                if not db.session.query(GameModel.GID).select_from(PlayedGame).join(GameModel).filter(PlayedGame.PUUID == PUUID).filter(GameModel.GID==item).first():
                    toUpdate.append(item)
                    updateIndex += 1
                else:
                    gettingNew = False
                    break
            if(updateIndex == 100):
                gettingNew = False
        if updateIndex != 0:
            try:
                addGames(toUpdate)
            except Exception:
                return 500
        
        return 201

api.add_resource(UpdateUser, "/update-user/<PUUID>")


class AsyncUpdateUser(Resource):
    maxCalls = 50
    callIndex = 0
    callLookup = dict()
    
    def put(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404
        try:
            userData = getSummonerByPUUID(PUUID)
            userLeagueInfo = getLeagueInfoBySID(userData['id'])
            userAccountInfo = getAccountByPUUID(PUUID)
        except Exception:
            return 500
        
        for item in userLeagueInfo:
            if item['queueType'] == 'RANKED_SOLO_5x5':
                userLeagueInfo = item
                break

        updatedUser = createUser(userData, userLeagueInfo, userAccountInfo)
        db.session.execute(
            update(UserModel).where(UserModel.PUUID == PUUID).values(updatedUser.to_dict())
        )
        db.session.commit()
        
        #Getting matches
        currSeason = db.session.query(GameModel.season).order_by(GameModel.season.desc()).first()[0]
        numCurrSeasonGames = db.session.query(GameModel.GID).select_from(PlayedGame).join(GameModel).filter(PlayedGame.PUUID == PUUID).filter(GameModel.season == currSeason).count()
        
        updateIndex = 0
        gettingNew = True
        needPrev = True
        while(gettingNew):
            print("checking to " + str(updateIndex), file=sys.stderr)
            try:
                games = getMatchXtoX(PUUID, updateIndex, updateIndex + 100)
                self.limHandler(1)
            except Exception:
                return 500
            
            for item in games:
                if not db.session.query(GameModel.GID).select_from(PlayedGame).join(GameModel).filter(PlayedGame.PUUID == PUUID).filter(GameModel.GID==item).first():
                    game = addGame(item)
                    
                    if game == 409:
                        pass
                    else:
                        self.limHandler(2)
                        if int(game.season) != currSeason:
                            gettingNew = False
                            needPrev = False
                            break
                        else:
                            updateIndex += 1
                else:
                    gettingNew = False
                    break
            
        if needPrev:
            gettingNew = True
        updateIndex += numCurrSeasonGames
        
        while(gettingNew):
            print("checking to " + str(updateIndex), file=sys.stderr)
            try:
                games = getMatchXtoX(PUUID, updateIndex, updateIndex + 100)
                self.limHandler(1)
            except Exception:
                return 500
            
            for item in games:
                if not db.session.query(GameModel.GID).select_from(PlayedGame).join(GameModel).filter(PlayedGame.PUUID == PUUID).filter(GameModel.GID==item).first():
                    game = addGame(item)
                    
                    if game == 409:
                        pass
                    else:
                        self.limHandler(2)
                        if int(game.season) != currSeason:
                            gettingNew = False
                            break
                        else:
                            updateIndex += 1
                else:
                    gettingNew = False
                    break
        return 201
    
    
    def limHandler(self, numCalls):
        for call in range(numCalls):
            if self.callIndex == self.maxCalls:
                self.callIndex = 0
            
            self.callIndex += 1
            
            if self.callIndex in self.callLookup:
                timeSinceCall = (time.time() - self.callLookup[self.callIndex])
                if timeSinceCall < 120:
                    print("sleeping for " + str(120 - timeSinceCall), file=sys.stderr)
                    time.sleep(120 - timeSinceCall)
            
            self.callLookup[self.callIndex] = time.time()

api.add_resource(AsyncUpdateUser, "/update-user/async/<PUUID>")


class generalChampStats(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404
        
        UpdateUser().put(PUUID)
        
        champStats = dict()
        playedChamps = db.session.query(PlayedGame.championName, PlayedGame.CID).filter_by(PUUID=PUUID).distinct().all()
        
        for champ in playedChamps:
            stats = dict()
            
            stats['champID'] = champ[1]
            
            stats['wins'] = db.session.query(PlayedGame).filter_by(PUUID=PUUID, championName=champ[0]).filter(PlayedGame.won).count()
            stats['losses'] = db.session.query(PlayedGame).filter_by(PUUID=PUUID, championName=champ[0]).filter(not PlayedGame.won).count()
            stats['gamesPlayed'] = db.session.query(PlayedGame).filter_by(PUUID=PUUID, championName=champ[0]).count()
            stats['avgKill'] = round(db.session.query(func.avg(PlayedGame.kills)).filter_by(PUUID=PUUID, championName=champ[0]).scalar(), 1)
            stats['avgDeath'] = round(db.session.query(func.avg(PlayedGame.deaths)).filter_by(PUUID=PUUID, championName=champ[0]).scalar(), 1)
            stats['avgAssist'] = round(db.session.query(func.avg(PlayedGame.assists)).filter_by(PUUID=PUUID, championName=champ[0]).scalar(), 1)
        
            champStats[champ[0]] = stats
        
        return champStats, 200

api.add_resource(generalChampStats, "/champ-stats/<PUUID>")


class userTags(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404
        
        tags = dict()
        
        #Champ Lover
        playedChamps = db.session.query(PlayedGame.championName, PlayedGame.CID).filter_by(PUUID=PUUID).distinct().all()
        for champ in playedChamps:
            playedGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID, championName=champ[0]).count()
            if playedGames >= 20:
                tags[champ[0] + ' lover'] = (0, "This player has played " + str(playedGames) + " of " + champ[0])
                
        #Streak
        streak = None
        streakGames = 0
        for game in db.session.query(PlayedGame.won).select_from(PlayedGame).join(GameModel).filter(GameModel.GID == PlayedGame.GID).filter(PlayedGame.PUUID == PUUID).order_by(GameModel.time_start.desc()).all():
            if streak is None:
                streak = game[0]
            else:
                if streak != game[0]:
                    break
            streakGames += 1
        
        if streakGames >= 3:
            if streak:
                tags['Win Streak'] = (0, "This player has won " + str(streakGames) + " games in a row")
            else:
                tags['Loss Streak'] = (1, "This player has lost " + str(streakGames) + " games in a row")
                
        #Role Tag
        totalGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID).count()
        
        topGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID).filter(PlayedGame.position == 'TOP').count()
        jgGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID).filter(PlayedGame.position == 'JUNGLE').count()
        midGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID).filter(PlayedGame.position == 'MIDDLE').count()
        adcGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID).filter(PlayedGame.position == 'BOTTOM').count()
        supGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID).filter(PlayedGame.position == 'UTILITY').count()
        
        if topGames >= totalGames * 0.5:
            tags['Top Player'] = (2, "This player mostly plays top lane")
        
        if jgGames >= totalGames * 0.5:
            tags['Jungle Player'] = (2, "This player mostly plays jungle")
        
        if midGames >= totalGames * 0.5:
            tags['Mid Player'] = (2, "This player mostly plays mid lane")
            
        if adcGames >= totalGames * 0.5:
            tags['ADC Player'] = (2, "This player mostly plays adc")
        
        if supGames >= totalGames * 0.5:
            tags['Support Player'] = (2, "This player mostly plays support")
        
        return tags, 200

api.add_resource(userTags, "/user/tags/<PUUID>")


class getUserGamesPlayed(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404

        result = PlayedGame.query.filter_by(PUUID=PUUID).count()

        return result, 200

api.add_resource(getUserGamesPlayed, "/user/games-played/<PUUID>")


#
#Helper Methods
#

def getPlayersInGame(GID):
    result = PlayedGame.query.filter_by(GID=GID).all()
    result = [user.PUUID for user in result]

    return result


def parseGameData(gameData) -> tuple[GameModel, list[PlayedGame]]:
    newGame = GameModel(
        GID=gameData['metadata']['matchId'],
        
        season=int(gameData['info']['gameVersion'].split('.')[0]),
        patch=str('.'.join(gameData['info']['gameVersion'].split('.')[1:])),
                    
        time_start=gameData['info']['gameStartTimestamp'],
        time_end=gameData['info']['gameEndTimestamp'],
    )
    
    newPlayedGames = []
    
    for player in range(len(gameData['info']['participants'])):
        played = PlayedGame(
            PUUID=gameData['info']['participants'][player]['puuid'],
            GID=gameData['metadata']['matchId'],
            
            name=gameData['info']['participants'][player]['summonerName'],
            
            riotIdGameName=gameData['info']['participants'][player]['riotIdGameName'],
            riotIdTagline=gameData['info']['participants'][player]['riotIdTagline'],
            
            summonerId=gameData['info']['participants'][player]['summonerId'],
            summonerLevel=gameData['info']['participants'][player]['summonerLevel'],
            
            firstBloodAssist=gameData['info']['participants'][player]['firstBloodAssist'],
            firstBloodKill=gameData['info']['participants'][player]['firstBloodKill'],
            
            firstTowerAssist=gameData['info']['participants'][player]['firstTowerAssist'],
            firstTowerKill=gameData['info']['participants'][player]['firstTowerKill'],
            
            bountyLevel=gameData['info']['participants'][player]['bountyLevel'],
            longestTimeSpentLiving=gameData['info']['participants'][player]['longestTimeSpentLiving'],
            
            killingSprees=gameData['info']['participants'][player]['killingSprees'],
            largestKillingSpree=gameData['info']['participants'][player]['largestKillingSpree'],
            largestMultiKill=gameData['info']['participants'][player]['largestMultiKill'],

            doubleKills=gameData['info']['participants'][player]['doubleKills'],
            tripleKills=gameData['info']['participants'][player]['tripleKills'],
            quadraKills=gameData['info']['participants'][player]['quadraKills'],
            pentaKills=gameData['info']['participants'][player]['pentaKills'],
            unrealKills=gameData['info']['participants'][player]['unrealKills'],
            
            largestCriticalStrike=gameData['info']['participants'][player]['largestCriticalStrike'],

            damageDealtToBuildings=gameData['info']['participants'][player]['damageDealtToBuildings'],
            damageDealtToObjectives=gameData['info']['participants'][player]['damageDealtToObjectives'],
            damageDealtToTurrets=gameData['info']['participants'][player]['damageDealtToTurrets'],
            
            damageSelfMitigated=gameData['info']['participants'][player]['damageSelfMitigated'],
            
            magicDamageDealt=gameData['info']['participants'][player]['magicDamageDealt'],
            magicDamageDealtToChampions=gameData['info']['participants'][player]['magicDamageDealtToChampions'],
            magicDamageTaken=gameData['info']['participants'][player]['magicDamageTaken'],
            
            physicalDamageDealt=gameData['info']['participants'][player]['physicalDamageDealt'],
            physicalDamageDealtToChampions=gameData['info']['participants'][player]['physicalDamageDealtToChampions'],
            physicalDamageTaken=gameData['info']['participants'][player]['physicalDamageTaken'],
            
            trueDamageDealt=gameData['info']['participants'][player]['trueDamageDealt'],
            trueDamageDealtToChampions=gameData['info']['participants'][player]['trueDamageDealtToChampions'],
            trueDamageTaken=gameData['info']['participants'][player]['trueDamageTaken'],
            
            totalDamageDealt=gameData['info']['participants'][player]['totalDamageDealt'],
            totalDamageDealtToChampions=gameData['info']['participants'][player]['totalDamageDealtToChampions'],
            totalDamageTaken=gameData['info']['participants'][player]['totalDamageTaken'],
            
            totalHeal=gameData['info']['participants'][player]['totalHeal'],
            totalHealsOnTeammates=gameData['info']['participants'][player]['totalHealsOnTeammates'],
            totalUnitsHealed=gameData['info']['participants'][player]['totalUnitsHealed'],

            timeCCingOthers=gameData['info']['participants'][player]['timeCCingOthers'],
            totalTimeCCDealt=gameData['info']['participants'][player]['totalTimeCCDealt'],
            totalTimeSpentDead=gameData['info']['participants'][player]['totalTimeSpentDead'],
            
            spell1Casts=gameData['info']['participants'][player]['spell1Casts'],
            spell2Casts=gameData['info']['participants'][player]['spell2Casts'],
            spell3Casts=gameData['info']['participants'][player]['spell3Casts'],
            spell4Casts=gameData['info']['participants'][player]['spell4Casts'],
            
            summoner1Casts=gameData['info']['participants'][player]['summoner1Casts'],
            summoner1Id=gameData['info']['participants'][player]['summoner1Id'],
            
            summoner2Casts=gameData['info']['participants'][player]['summoner2Casts'],
            summoner2Id=gameData['info']['participants'][player]['summoner2Id'],
            
            neutralMinionsKilled=gameData['info']['participants'][player]['neutralMinionsKilled'],
            totalMinionsKilled=gameData['info']['participants'][player]['totalMinionsKilled'],
            
            baronKills=gameData['info']['participants'][player]['baronKills'],
            dragonKills=gameData['info']['participants'][player]['dragonKills'],
            
            inhibitorKills=gameData['info']['participants'][player]['inhibitorKills'],
            inhibitorTakedowns=gameData['info']['participants'][player]['inhibitorTakedowns'],
            inhibitorsLost=gameData['info']['participants'][player]['inhibitorsLost'],

            turretKills=gameData['info']['participants'][player]['turretKills'],
            turretTakedowns=gameData['info']['participants'][player]['turretTakedowns'],
            turretsLost=gameData['info']['participants'][player]['turretsLost'],
            
            nexusKills=gameData['info']['participants'][player]['nexusKills'],
            nexusTakedowns=gameData['info']['participants'][player]['nexusTakedowns'],
            nexusLost=gameData['info']['participants'][player]['nexusLost'],
            
            objectivesStolen=gameData['info']['participants'][player]['objectivesStolen'],
            objectivesStolenAssists=gameData['info']['participants'][player]['objectivesStolenAssists'],
            
            visionScore=gameData['info']['participants'][player]['visionScore'],
            visionWardsBoughtInGame=gameData['info']['participants'][player]['visionWardsBoughtInGame'],
            wardsKilled=gameData['info']['participants'][player]['wardsKilled'],
            wardsPlaced=gameData['info']['participants'][player]['wardsPlaced'],
            detectorWardsPlaced=gameData['info']['participants'][player]['detectorWardsPlaced'],
            sightWardsBoughtInGame=gameData['info']['participants'][player]['sightWardsBoughtInGame'],
            
            position=gameData['info']['participants'][player]['teamPosition'],
            CID=gameData['info']['participants'][player]['championId'],
            championName=gameData['info']['participants'][player]['championName'],
            
            champExperience=gameData['info']['participants'][player]['champExperience'],
            champLevel=gameData['info']['participants'][player]['champLevel'],
            
            kills=gameData['info']['participants'][player]['kills'],
            deaths=gameData['info']['participants'][player]['deaths'],
            assists=gameData['info']['participants'][player]['assists'],
            
            goldEarned=gameData['info']['participants'][player]['goldEarned'],
            goldSpent=gameData['info']['participants'][player]['goldSpent'],
            
            itemsPurchased=gameData['info']['participants'][player]['itemsPurchased'],
            consumablesPurchased=gameData['info']['participants'][player]['consumablesPurchased'],

            item0=gameData['info']['participants'][player]['item0'],
            item1=gameData['info']['participants'][player]['item1'],
            item2=gameData['info']['participants'][player]['item2'],
            item3=gameData['info']['participants'][player]['item3'],
            item4=gameData['info']['participants'][player]['item4'],
            item5=gameData['info']['participants'][player]['item5'],
            item6=gameData['info']['participants'][player]['item6'],
            
            timePlayed=gameData['info']['participants'][player]['timePlayed'],
            
            gameEndedInEarlySurrender=gameData['info']['participants'][player]['gameEndedInEarlySurrender'],
            gameEndedInSurrender=gameData['info']['participants'][player]['gameEndedInSurrender'],
            teamEarlySurrendered=gameData['info']['participants'][player]['teamEarlySurrendered'],

            won=gameData['info']['participants'][player]['win'],
        )
        
        newPlayedGames.append(played)
        
    return newGame, newPlayedGames


def makeTimeLine(timeLineData):
    puuidData = dict()
    for participants in timeLineData['info']['participants']:
        puuidData[int(participants['participantId'])] = participants['puuid']
    
    timeline = {
        'timeline': None,
        'entries': []
    }
    
    timeLineObj = GameTimeLine(
        GID=timeLineData['metadata']['matchId'],
        
        dataVersion=timeLineData['metadata']['dataVersion'],
        
        frameInterval=timeLineData['info']['frameInterval'],
        numFrames=len(timeLineData['info']['frames'])
    )
    
    timeline['timeline'] = timeLineObj
    
    for i, entry in enumerate(timeLineData['info']['frames']):
        entryData = {
            'entry': None,
            'frames': [],
            'events': []
        }
        
        entryObj = TimeLineEntry(
            GID=timeLineData['metadata']['matchId'],
            entryNumber=i,
            timestamp=entry['timestamp']
        )
        
        entryData['entry'] = entryObj
        
        for j, event in enumerate(entry['events']):
            eventObj = Event(
                GID=timeLineData['metadata']['matchId'],
                entryNumber=i,
                eventNumber=j,

                timestamp=event['timestamp'],
                type=event['type'],
            )

            entryData['events'].append(eventObj)
            
        for playerKey, playerData in entry['participantFrames'].items():
            playerObj = PlayerFrame(
                GID = timeLineData['metadata']['matchId'],
                entryNumber = i,
                PUUID = puuidData[int(playerKey)],
                
                #Personal Stats
                abilityHaste = playerData['championStats']['abilityHaste'],
                abilityPower = playerData['championStats']['abilityPower'],
                armor = playerData['championStats']['armor'],
                armorPen = playerData['championStats']['armorPen'],
                armorPenPercent = playerData['championStats']['armorPenPercent'],
                attackDamage = playerData['championStats']['attackDamage'],
                attackSpeed = playerData['championStats']['attackSpeed'],
                bonusArmorPenPercent = playerData['championStats']['bonusArmorPenPercent'],
                bonusMagicPenPercent = playerData['championStats']['bonusMagicPenPercent'],
                ccReduction = playerData['championStats']['ccReduction'],
                cooldownReduction = playerData['championStats']['cooldownReduction'],
                health = playerData['championStats']['health'],
                healthMax = playerData['championStats']['healthMax'],
                healthRegen = playerData['championStats']['healthRegen'],
                lifesteal = playerData['championStats']['lifesteal'],
                magicPen = playerData['championStats']['magicPen'],
                magicPenPercent = playerData['championStats']['magicPenPercent'],
                magicResist = playerData['championStats']['magicResist'],
                movementSpeed = playerData['championStats']['movementSpeed'],
                omnivamp = playerData['championStats']['omnivamp'],
                physicalVamp = playerData['championStats']['physicalVamp'],
                power = playerData['championStats']['power'],
                powerMax = playerData['championStats']['powerMax'],
                powerRegen = playerData['championStats']['powerRegen'],
                spellVamp = playerData['championStats']['spellVamp'],
                
                #Damage Stats
                magicDamageDone = playerData['damageStats']['magicDamageDone'],
                magicDamageDoneToChampions = playerData['damageStats']['magicDamageDoneToChampions'],
                magicDamageTaken = playerData['damageStats']['magicDamageTaken'],
                
                physicalDamageDone = playerData['damageStats']['physicalDamageDone'],
                physicalDamageDoneToChampions = playerData['damageStats']['physicalDamageDoneToChampions'],
                physicalDamageTaken = playerData['damageStats']['physicalDamageTaken'],
                
                trueDamageDone = playerData['damageStats']['trueDamageDone'],
                trueDamageDoneToChampions = playerData['damageStats']['trueDamageDoneToChampions'],
                trueDamageTaken = playerData['damageStats']['trueDamageTaken'],
                
                totalDamageDone = playerData['damageStats']['totalDamageDone'],
                totalDamageDoneToChampions = playerData['damageStats']['totalDamageDoneToChampions'],
                totalDamageTaken = playerData['damageStats']['totalDamageTaken'],
                
                #Other Stats
                currentGold = playerData['currentGold'],
                goldPerSecond = playerData['goldPerSecond'],
                totalGold = playerData['totalGold'],
                
                jungleMinionsKilled = playerData['jungleMinionsKilled'],
                minionsKilled = playerData['minionsKilled'],
                
                level = playerData['level'],
                xp = playerData['xp'],
                
                timeEnemySpentControlled = playerData['timeEnemySpentControlled']
            )

            entryData['frames'].append(playerObj)
            
        timeline['entries'].append(entryData)
    
    return timeline


def addGames(games):
    for item in games:
        addGame(item)

    return 201


def addGame(GID): 
    if not bool(GameModel.query.filter_by(GID=GID).first()):
        gameData = getMatchByMatchID(GID)
        timeLineData = getMatchTimeLineByMatchID(GID)
        
        newGameData, newPlayedGames = parseGameData(gameData)
        timeLine = makeTimeLine(timeLineData)
        
        db.session.add(newGameData)

        for played in newPlayedGames:
            db.session.add(played)
        
        db.session.add(timeLine['timeline'])
        
        for entry in timeLine['entries']:
            db.session.add(entry['entry'])

            for frame in entry['frames']:
                db.session.add(frame)

            for event in entry['events']:
                db.session.add(event)

        db.session.commit()
    else:
        return 409
    
    return newGameData


def createUser(userData, userLeagueInfo, userAccountInfo) -> UserModel:
    if not userLeagueInfo:
        userLeagueInfo = {
            'tier': 'UNRANKED',
            'rank': 'UNRANKED',
            'wins': 0,
            'losses': 0
        }
        
    newUser = UserModel(
            PUUID=userData['puuid'],
            SID=userData['id'],

            name=userData['name'],
            profileIcon=userData['profileIconId'],
            
            tagLine=userAccountInfo['tagLine'],
            gameName=userAccountInfo['gameName'],

            tier=userLeagueInfo['tier'],
            rank=userLeagueInfo['rank'],

            wins=userLeagueInfo['wins'],
            losses=userLeagueInfo['losses'],

            revisionDate=userData['revisionDate']
        )
    
    return newUser


def getPlayerStats(gameData, playerData) -> dict:
    playerStats = {
        #GameInfo
        'patch': getattr(gameData, 'patch'),
        'time_start': getattr(gameData, 'time_start'),
        'time_end': getattr(gameData, 'time_end'),
        
        #PlayerInfo
        'PUUID': getattr(playerData, 'PUUID'),
        
        'GID': getattr(playerData, 'GID'),
        
        'name': getattr(playerData, 'name'),
        
        'riotIdGameName': getattr(playerData, 'riotIdGameName'),
        'riotIdTagline': getattr(playerData, 'riotIdTagline'),

        'summonerId': getattr(playerData, 'summonerId'),
        'summonerLevel': getattr(playerData, 'summonerLevel'),
        
        'firstBloodAssist': getattr(playerData, 'firstBloodAssist'),
        'firstBloodKill': getattr(playerData, 'firstBloodKill'),

        'firstTowerAssist': getattr(playerData, 'firstTowerAssist'),
        'firstTowerKill': getattr(playerData, 'firstTowerKill'),

        'bountyLevel': getattr(playerData, 'bountyLevel'),
        'longestTimeSpentLiving': getattr(playerData, 'longestTimeSpentLiving'),

        'killingSprees': getattr(playerData, 'killingSprees'),
        'largestKillingSpree': getattr(playerData, 'largestKillingSpree'),
        'largestMultiKill': getattr(playerData, 'largestMultiKill'),

        'doubleKills': getattr(playerData, 'doubleKills'),
        'tripleKills': getattr(playerData, 'tripleKills'),
        'quadraKills': getattr(playerData, 'quadraKills'),
        'pentaKills': getattr(playerData, 'pentaKills'),
        'unrealKills': getattr(playerData, 'unrealKills'),

        'largestCriticalStrike': getattr(playerData, 'largestCriticalStrike'),
        
        'damageDealtToBuildings': getattr(playerData, 'damageDealtToBuildings'),
        'damageDealtToObjectives': getattr(playerData, 'damageDealtToObjectives'),
        'damageDealtToTurrets': getattr(playerData, 'damageDealtToTurrets'),

        'damageSelfMitigated': getattr(playerData, 'damageSelfMitigated'),

        'magicDamageDealt': getattr(playerData, 'magicDamageDealt'),
        'magicDamageDealtToChampions': getattr(playerData, 'magicDamageDealtToChampions'),
        'magicDamageTaken': getattr(playerData, 'magicDamageTaken'),
        
        'physicalDamageDealt': getattr(playerData, 'physicalDamageDealt'),
        'physicalDamageDealtToChampions': getattr(playerData, 'physicalDamageDealtToChampions'),
        'physicalDamageTaken': getattr(playerData, 'physicalDamageTaken'),
        
        'trueDamageDealt': getattr(playerData, 'trueDamageDealt'),
        'trueDamageDealtToChampions': getattr(playerData, 'trueDamageDealtToChampions'),
        'trueDamageTaken': getattr(playerData, 'trueDamageTaken'),
        
        'totalDamageDealt': getattr(playerData, 'totalDamageDealt'),
        'totalDamageDealtToChampions': getattr(playerData, 'totalDamageDealtToChampions'),
        'totalDamageTaken': getattr(playerData, 'totalDamageTaken'),
        'totalDamageShieldedOnTeammates': getattr(playerData, 'totalDamageShieldedOnTeammates'),

        'totalHeal': getattr(playerData, 'totalHeal'),
        'totalHealsOnTeammates': getattr(playerData, 'totalHealsOnTeammates'),
        'totalUnitsHealed': getattr(playerData, 'totalUnitsHealed'),

        'timeCCingOthers': getattr(playerData, 'timeCCingOthers'),
        'totalTimeCCDealt': getattr(playerData, 'totalTimeCCDealt'),
        'totalTimeSpentDead': getattr(playerData, 'totalTimeSpentDead'),

        'spell1Casts': getattr(playerData, 'spell1Casts'),
        'spell2Casts': getattr(playerData, 'spell2Casts'),
        'spell3Casts': getattr(playerData, 'spell3Casts'),
        'spell4Casts': getattr(playerData, 'spell4Casts'),
        
        'summoner1Casts': getattr(playerData, 'summoner1Casts'),
        'summoner1Id': getattr(playerData, 'summoner1Id'),

        'summoner2Casts': getattr(playerData, 'summoner2Casts'),
        'summoner2Id': getattr(playerData, 'summoner2Id'),

        'neutralMinionsKilled': getattr(playerData, 'neutralMinionsKilled'),
        'totalMinionsKilled': getattr(playerData, 'totalMinionsKilled'),

        'baronKills': getattr(playerData, 'baronKills'),
        'dragonKills': getattr(playerData, 'dragonKills'),
        
        'inhibitorKills': getattr(playerData, 'inhibitorKills'),
        'inhibitorTakedowns': getattr(playerData, 'inhibitorTakedowns'),
        'inhibitorsLost': getattr(playerData, 'inhibitorsLost'),

        'turretKills': getattr(playerData, 'turretKills'),
        'turretTakedowns': getattr(playerData, 'turretTakedowns'),
        'turretsLost': getattr(playerData, 'turretsLost'),

        'nexusKills': getattr(playerData, 'nexusKills'),
        'nexusTakedowns': getattr(playerData, 'nexusTakedowns'),
        'nexusLost': getattr(playerData, 'nexusLost'),

        'objectivesStolen': getattr(playerData, 'objectivesStolen'),
        'objectivesStolenAssists': getattr(playerData, 'objectivesStolenAssists'),

        'visionScore': getattr(playerData, 'visionScore'),
        'visionWardsBoughtInGame': getattr(playerData, 'visionWardsBoughtInGame'),
        'wardsKilled': getattr(playerData, 'wardsKilled'),
        'wardsPlaced': getattr(playerData, 'wardsPlaced'),
        'detectorWardsPlaced': getattr(playerData, 'detectorWardsPlaced'),
        'sightWardsBoughtInGame': getattr(playerData, 'sightWardsBoughtInGame'),

        'position': getattr(playerData, 'position'),
        'CID': getattr(playerData, 'CID'),
        'championName': getattr(playerData, 'championName'),

        'champExperience': getattr(playerData, 'champExperience'),
        'champLevel': getattr(playerData, 'champLevel'),

        'kills': getattr(playerData, 'kills'),
        'deaths': getattr(playerData, 'deaths'),
        'assists': getattr(playerData, 'assists'),
        
        'goldEarned': getattr(playerData, 'goldEarned'),
        'goldSpent': getattr(playerData, 'goldSpent'),
        
        'itemsPurchased': getattr(playerData, 'itemsPurchased'),
        'consumablesPurchased': getattr(playerData, 'consumablesPurchased'),

        'item0': getattr(playerData, 'item0'),
        'item1': getattr(playerData, 'item1'),
        'item2': getattr(playerData, 'item2'),
        'item3': getattr(playerData, 'item3'),
        'item4': getattr(playerData, 'item4'),
        'item5': getattr(playerData, 'item5'),
        'item6': getattr(playerData, 'item6'),

        'timePlayed': getattr(playerData, 'timePlayed'),

        'gameEndedInEarlySurrender': getattr(playerData, 'gameEndedInEarlySurrender'),
        'gameEndedInSurrender': getattr(playerData, 'gameEndedInSurrender'),
        'teamEarlySurrendered': getattr(playerData, 'teamEarlySurrendered'),

        'won': getattr(playerData, 'won'),
    }
    
    return playerStats


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=8080) #TODO CHANGE BEFORE PRODUCTION