from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from accessRiotApi import getMatchByMatchID, getMatchLast20, getSummonerByName, getSummonerByPUUID, getLeagueInfoBySID, getMatchXtoX, getACCTInfoByRiotID, getAccountByPUUID
import os
from sqlalchemy import func

basedir = os.path.abspath(os.path.dirname(__file__)) + "/data/"

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)


class PlayedGame(db.Model):
    __tablename__ = 'Played_Game'
    PUUID = db.Column(db.String, db.ForeignKey('User.PUUID'), primary_key=True)
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    
    name = db.Column(db.String, nullable=False)
    
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
    champion_name = db.Column(db.String, nullable=True)
    
    total_minions = db.Column(db.Integer, nullable=True)
    
    vision_score = db.Column(db.Integer, nullable=True)
    
    won_game = db.Column(db.Boolean, nullable=False)

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
    
    patch = db.Column(db.String, nullable=False)
    
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
            addGameXtoX(PUUID, numEntries, y)

        result = db.session.query(GameModel.GID).select_from(GameModel).join(PlayedGame).filter(GameModel.GID == PlayedGame.GID).filter(PlayedGame.PUUID == PUUID).order_by(GameModel.time_start.desc()).offset(x).limit(y).all()
        result = [game[0] for game in result]

        return result, 200

api.add_resource(GameIDXtoX, "/game-id/x-x/<PUUID>/<x>/<y>")


class GameDataLast20(Resource):
    def put(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404

        games = getMatchLast20(PUUID)
        for item in games:
            gameData = getMatchByMatchID(item)
            if not bool(GameModel.query.filter_by(GID=gameData['metadata']['matchId']).first()):
                newGameData, newPlayedGames = addGame(gameData)
                
                db.session.add(newGameData)
                for played in newPlayedGames:
                    db.session.add(played)
                
        db.session.commit()
        return 201        

api.add_resource(GameDataLast20, "/game-data/last-20/<PUUID>")


class GameDataXtoX(Resource):
    def put(self, PUUID, x, y):
        return addGameXtoX(PUUID, x, y)

api.add_resource(GameDataXtoX, "/game-data/x-x/<PUUID>/<x>/<y>")


class UpdateUser(Resource):
    def put(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404
        
        if not bool(PlayedGame.query.filter_by(PUUID=PUUID).first()):
            try:
                addGameXtoX(PUUID, 0, 20)
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

        toUpdate = []
        
        updateIndex = 0
        gettingNew = True
        while(gettingNew):
            try:
                games = getMatchXtoX(PUUID, updateIndex, updateIndex + 20)
            except Exception:
                return 500
            
            for item in games:
                if not GameModel.query.filter_by(GID=item).first():
                    toUpdate.append(item)
                    updateIndex += 1
                else:
                    gettingNew = False
                    break
            if(updateIndex == 100):
                gettingNew = False
        
        if updateIndex != 0:
            try:
                addGameXtoX(PUUID, 0, updateIndex)
            except Exception:
                return 500
        
        return 201

api.add_resource(UpdateUser, "/update-user/<PUUID>")


class generalChampStats(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404
        
        UpdateUser().put(PUUID)
        
        #TODO Gets all user games from the current season, unimplementable due to rate limits
        
        # userData = UserModel.query.filter_by(PUUID=PUUID).first()
        
        # neededGames = int(userData.wins) + int(userData.losses)
        
        # knownGames = PlayedGame.query.filter_by(PUUID=PUUID).count()
        
        # while(knownGames < neededGames):
        #     if (neededGames - knownGames) >= 100:
        #         addGameXtoX(PUUID, knownGames, knownGames + 100)
        #         knownGames += 100
        #     else:
        #         addGameXtoX(PUUID, neededGames - knownGames, neededGames)
        #         knownGames = neededGames
        
        champStats = dict()
        playedChamps = db.session.query(PlayedGame.champion_name, PlayedGame.CID).filter_by(PUUID=PUUID).distinct().all()
        
        for champ in playedChamps:
            stats = dict()
            
            stats['champID'] = champ[1]
            
            stats['wins'] = db.session.query(PlayedGame).filter_by(PUUID=PUUID, champion_name=champ[0]).filter(PlayedGame.won_game).count()
            stats['losses'] = db.session.query(PlayedGame).filter_by(PUUID=PUUID, champion_name=champ[0]).filter(not PlayedGame.won_game).count()
            stats['gamesPlayed'] = db.session.query(PlayedGame).filter_by(PUUID=PUUID, champion_name=champ[0]).count()
            stats['avgKill'] = round(db.session.query(func.avg(PlayedGame.kills)).filter_by(PUUID=PUUID, champion_name=champ[0]).scalar(), 1)
            stats['avgDeath'] = round(db.session.query(func.avg(PlayedGame.deaths)).filter_by(PUUID=PUUID, champion_name=champ[0]).scalar(), 1)
            stats['avgAssist'] = round(db.session.query(func.avg(PlayedGame.assists)).filter_by(PUUID=PUUID, champion_name=champ[0]).scalar(), 1)
        
            champStats[champ[0]] = stats
        
        return champStats, 200

api.add_resource(generalChampStats, "/champ-stats/<PUUID>")


class userTags(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404
        
        tags = dict()
        playedChamps = db.session.query(PlayedGame.champion_name, PlayedGame.CID).filter_by(PUUID=PUUID).distinct().all()
        for champ in playedChamps:
            playedGames = db.session.query(PlayedGame).filter_by(PUUID=PUUID, champion_name=champ[0]).count()
            if playedGames >= 20:
                tags[champ[0] + ' lover'] = playedGames
        
        return tags, 200
    
api.add_resource(userTags, "/user/tags/<PUUID>")


class getUserGamesPlayed(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return 404

        result = PlayedGame.query.filter_by(PUUID=PUUID).count()

        return result, 200

api.add_resource(getUserGamesPlayed, "/user/games-played/<PUUID>")


def getPlayersInGame(GID):
    result = PlayedGame.query.filter_by(GID=GID).all()
    result = [user.PUUID for user in result]

    return result


def addGame(gameData) -> tuple[GameModel, list[PlayedGame]]:
    newGame = GameModel(
        GID=gameData['metadata']['matchId'],
        patch=gameData['info']['gameVersion'],
                    
        time_start=gameData['info']['gameStartTimestamp'],
        time_end=gameData['info']['gameEndTimestamp'],
    )
    
    newPlayedGames = []
    
    for player in range(10):
        played = PlayedGame(
            PUUID=gameData['info']['participants'][player]['puuid'],
            GID=gameData['metadata']['matchId'],
            
            name=gameData['info']['participants'][player]['summonerName'],
            
            item0=gameData['info']['participants'][player]['item0'],
            item1=gameData['info']['participants'][player]['item1'],
            item2=gameData['info']['participants'][player]['item2'],
            item3=gameData['info']['participants'][player]['item3'],
            item4=gameData['info']['participants'][player]['item4'],
            item5=gameData['info']['participants'][player]['item5'],
            item6=gameData['info']['participants'][player]['item6'],

            summoner1ID=gameData['info']['participants'][player]['summoner1Id'],
            summoner2ID=gameData['info']['participants'][player]['summoner2Id'],

            kills=gameData['info']['participants'][player]['kills'],
            deaths=gameData['info']['participants'][player]['deaths'],
            assists=gameData['info']['participants'][player]['assists'],
            
            true_damage=gameData['info']['participants'][player]['trueDamageDealtToChampions'],
            ad_damage=gameData['info']['participants'][player]['totalDamageDealtToChampions'],
            magic_damage=gameData['info']['participants'][player]['magicDamageDealtToChampions'],

            position=gameData['info']['participants'][player]['teamPosition'],

            gold_earned=gameData['info']['participants'][player]['goldEarned'],
            gold_spent=gameData['info']['participants'][player]['goldSpent'],

            CID=gameData['info']['participants'][player]['championId'],
            champion_name=gameData['info']['participants'][player]['championName'],

            total_minions=gameData['info']['participants'][player]['totalMinionsKilled'],

            vision_score=gameData['info']['participants'][player]['visionScore'],
            
            won_game=gameData['info']['participants'][player]['win'],
        )
        
        newPlayedGames.append(played)
        
    return newGame, newPlayedGames


def addGameXtoX(PUUID, x, y):
    if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
        return 404

    games = getMatchXtoX(PUUID, int(x), int(y))
    for item in games:
        gameData = getMatchByMatchID(item)
        if not bool(GameModel.query.filter_by(GID=gameData['metadata']['matchId']).first()):
            
            newGameData, newPlayedGames = addGame(gameData)

            db.session.add(newGameData)

            for played in newPlayedGames:
                db.session.add(played)

    db.session.commit()

    return 201


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
        'patch': getattr(gameData, 'patch'),
        'time_start': getattr(gameData, 'time_start'),
        'time_end': getattr(gameData, 'time_end'),
        
        'name': getattr(playerData, 'name'),
        
        'item0': getattr(playerData, 'item0'),
        'item1': getattr(playerData, 'item1'),
        'item2': getattr(playerData, 'item2'),
        'item3': getattr(playerData, 'item3'),
        'item4': getattr(playerData, 'item4'),
        'item5': getattr(playerData, 'item5'),
        'item6': getattr(playerData, 'item6'),
        
        'summoner1ID': getattr(playerData, 'summoner1ID'),
        'summoner2ID': getattr(playerData, 'summoner2ID'),
        
        'kills': getattr(playerData, 'kills'),
        'deaths': getattr(playerData, 'deaths'),
        'assists': getattr(playerData, 'assists'),
        
        'true_damage': getattr(playerData, 'true_damage'),
        'ad_damage': getattr(playerData, 'ad_damage'),
        'magic_damage': getattr(playerData, 'magic_damage'),
        
        'position': getattr(playerData, 'position'),
        
        'gold_earned': getattr(playerData, 'gold_earned'),
        'gold_spent': getattr(playerData, 'gold_spent'),
        
        'CID': getattr(playerData, 'CID'),
        'champion_name': getattr(playerData, 'champion_name'),
        
        'total_minions': getattr(playerData, 'total_minions'),
        
        'vision_score': getattr(playerData, 'vision_score'),
        
        'won_game': getattr(playerData, "won_game")
    }
    
    return playerStats


if __name__ == "__main__":
    app.run(debug = True) #TODO CHANGE BEFORE PRODUCTION