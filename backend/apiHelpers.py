from extensions import db

from accessRiotApi import (
    getMatchByMatchID, getMatchTimeLineByMatchID
)

from models import (
    PlayedGame, UserModel, GameModel, GameTimeLine,
    TimeLineEntry, PlayerFrame, Event
)

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
        perks = {}
        for style in gameData['info']['participants'][player]['perks']['styles']:
            perkChoices = {}
            for i, choice in enumerate(style['selections']):
                perkChoices[i] = choice['perk']
                perkChoices['ID'] = style['style']
            perks[style['description']] = perkChoices
        perks['offense'] = gameData['info']['participants'][player]['perks']['statPerks']['offense']
        perks['flex'] = gameData['info']['participants'][player]['perks']['statPerks']['flex']
        perks['defense'] = gameData['info']['participants'][player]['perks']['statPerks']['defense']
        
        played = PlayedGame(
            PUUID=gameData['info']['participants'][player]['puuid'],
            GID=gameData['metadata']['matchId'],
            
            gameName=gameData['info']['participants'][player]['riotIdGameName'],
            tagLine=gameData['info']['participants'][player]['riotIdTagline'],
            
            summonerId=gameData['info']['participants'][player]['summonerId'],
            summonerLevel=gameData['info']['participants'][player]['summonerLevel'],
            
            primaryStyleID = perks['primaryStyle']['ID'],
            subStyleID = perks['subStyle']['ID'],
            
            primaryStyle1 = perks['primaryStyle'][0],
            primaryStyle2 = perks['primaryStyle'][1],
            primaryStyle3 = perks['primaryStyle'][2],
            primaryStyle4 = perks['primaryStyle'][3],

            subStyle1 = perks['subStyle'][0],
            subStyle2 = perks['subStyle'][1],
            
            offensePerk = perks['offense'],
            flexPerk = perks['flex'],
            defensePerk = perks['defense'],
            
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
        
        'gameName': getattr(playerData, 'gameName'),
        'tagLine': getattr(playerData, 'tagLine'),
        
        'primaryStyleID': getattr(playerData, 'primaryStyleID'),
        'subStyleID': getattr(playerData, 'subStyleID'),
        
        'primaryStyle1': getattr(playerData, 'primaryStyle1'),
        'primaryStyle2': getattr(playerData, 'primaryStyle2'),
        'primaryStyle3': getattr(playerData, 'primaryStyle3'),
        'primaryStyle4': getattr(playerData, 'primaryStyle4'),

        'subStyle1': getattr(playerData, 'subStyle1'),
        'subStyle2': getattr(playerData, 'subStyle2'),
        
        'offensePerk': getattr(playerData, 'offensePerk'),
        'flexPerk': getattr(playerData, 'flexPerk'),
        'defensePerk': getattr(playerData, 'defensePerk'),

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

def getGameDataAll(GID):
    players = getPlayersInGame(GID)
        
    gameData = GameModel.query.filter_by(GID=GID).first()
    
    allGameData = {}
    
    for player in players:
        
        playerData = PlayedGame.query.filter_by(GID=GID, PUUID=player).first()
        playerDataDict = getPlayerStats(gameData, playerData)
        
        allGameData[player] = playerDataDict
    
    return allGameData
