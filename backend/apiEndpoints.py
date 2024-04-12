from flask import Response

from flask_restful import Resource, fields, marshal_with

from sqlalchemy import update, func

import time
import sys

from accessRiotApi import (
    getMatchXtoX, getSummonerByPUUID, getLeagueInfoBySID, getACCTInfoByRiotID, 
    getAccountByPUUID
)

from extensions import db

from models import (
    PlayedGame, UserModel, GameModel
)

from apiHelpers import (
    addGames, addGame, createUser, getPlayerStats, 
    getGameDataAll
)


resource_fields = {
    'PUUID': fields.String,
    'SID': fields.String,
    
    'tagLine': fields.String,
    'gameName': fields.String,
    
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
            status = self.put(tagLine, gameName).status_code
            if status != 201:
                return Response(status=status)

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
        
        return Response(status=201)


class UserByPUUID(Resource):
    @marshal_with(resource_fields)
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            status = self.put(PUUID).status_code
            if status != 201:
                return Response(status=status)
            
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
        
        return Response(status=201)


class GameDataByPlayer(Resource):
    def get(self, GID, PUUID):
        if not bool(GameModel.query.filter_by(GID=GID).first()):
            return Response(status=404)

        gameData = GameModel.query.filter_by(GID=GID).first()
        playerData = PlayedGame.query.filter_by(GID=GID, PUUID=PUUID).first()
        
        playerStats = getPlayerStats(gameData, playerData)
        
        return Response(playerStats, 200)


class GameDataAll(Resource):
    def get(self, GID):
        if not bool(GameModel.query.filter_by(GID=GID).first()):
            return Response(status=404)
        
        allGameData = getGameDataAll(GID)
        
        return allGameData, 200


class GameIDLast20(Resource):
    def get(self, PUUID):
        result = db.session.query(GameModel.GID).select_from(GameModel).join(PlayedGame).filter(GameModel.GID == PlayedGame.GID).filter(PlayedGame.PUUID == PUUID).order_by(GameModel.time_start.desc()).limit(20).all()
        result = [game[0] for game in result]
        
        return result, 200


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


class GameDataXtoX(Resource):
    def put(self, PUUID, x, y):
        gameIds = getMatchXtoX(PUUID, int(x), int(y))
        return addGames(gameIds)


class UpdateUser(Resource):
    def put(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return Response(status=404)
        
        if not bool(PlayedGame.query.filter_by(PUUID=PUUID).first()):
            try:
                gameIds = getMatchXtoX(PUUID, 0, 20)
                addGames(gameIds)
            except Exception:
                return Response(status=500)
            return Response(status=201)
        
        try:
            userData = getSummonerByPUUID(PUUID)
            userLeagueInfo = getLeagueInfoBySID(userData['id'])
            userAccountInfo = getAccountByPUUID(PUUID)
        except Exception:
            return Response(status=500)
        
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
                return Response(status=500)
            
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
                return Response(status=500)
        
        return Response(status=201)


class AsyncUpdateUser(Resource):
    maxCalls = 50
    callIndex = 0
    callLookup = dict()
    
    def put(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return Response(status=404)
        try:
            userData = getSummonerByPUUID(PUUID)
            userLeagueInfo = getLeagueInfoBySID(userData['id'])
            userAccountInfo = getAccountByPUUID(PUUID)
        except Exception:
            return Response(status=500)
        
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
                return Response(status=500)
            
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
                return Response(status=500)
            
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
        return Response(status=201)
    
    
    def limHandler(self, numCalls):
        for call in range(numCalls):
            if self.callIndex > self.maxCalls:
                self.callIndex = 0
            
            if self.callIndex in self.callLookup:
                timeSinceCall = (time.time() - self.callLookup[self.callIndex])
                if timeSinceCall < 120:
                    print("sleeping for " + str(120 - timeSinceCall), file=sys.stderr)
                    time.sleep(120 - timeSinceCall)
            
            self.callLookup[self.callIndex] = time.time()
            
            self.callIndex += 1


class generalChampStats(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return Response(status=404)
        
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


class userTags(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return Response(status=404)
        
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


class getUserGamesPlayed(Resource):
    def get(self, PUUID):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return Response(status=404)

        result = PlayedGame.query.filter_by(PUUID=PUUID).count()

        return result, 200


class userChampionInfoPage(Resource):
    def get(self, PUUID, championName):
        if not bool(UserModel.query.filter_by(PUUID=PUUID).first()):
            return Response(status=404)
        
        info = {
            'userData': None,
            'gameData': None,
            'playerStats': None,
            'averageStats': None,
            'tags': None,
        }
        
        userData = UserByPUUID().get(PUUID)[0]
        info['userData'] = userData
        
        games = db.session.query(PlayedGame).filter_by(PUUID=PUUID, championName=championName).all()
        
        if not games:
            return Response(status=404)
        
        gameIDs = [game.GID for game in games]
        
        games = dict()
        for game in gameIDs:
            gameData = getGameDataAll(game)
            games[game] = gameData

        info['games'] = games
        return info, 200