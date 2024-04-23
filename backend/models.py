from extensions import db
from sqlalchemy import ForeignKeyConstraint

class PlayedGame(db.Model):
    __tablename__ = 'Played_Game'
    PUUID = db.Column(db.String, db.ForeignKey('User.PUUID'), primary_key=True)
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    
    gameName = db.Column(db.String, nullable=False)
    tagLine = db.Column(db.String, nullable=False)
    
    summonerId = db.Column(db.String, nullable=True)
    summonerLevel = db.Column(db.BigInteger, nullable=True)
    
    primaryStyleID = db.Column(db.BigInteger, nullable=True)
    subStyleID = db.Column(db.BigInteger, nullable=True)
    
    primaryStyle1 = db.Column(db.BigInteger, nullable=True)
    primaryStyle2 = db.Column(db.BigInteger, nullable=True)
    primaryStyle3 = db.Column(db.BigInteger, nullable=True)
    primaryStyle4 = db.Column(db.BigInteger, nullable=True)
    
    subStyle1 = db.Column(db.BigInteger, nullable=True)
    subStyle2 = db.Column(db.BigInteger, nullable=True)
    
    offensePerk = db.Column(db.BigInteger, nullable=True)
    flexPerk = db.Column(db.BigInteger, nullable=True)
    defensePerk = db.Column(db.BigInteger, nullable=True)
    
    firstBloodAssist = db.Column(db.Boolean, nullable=True)
    firstBloodKill = db.Column(db.Boolean, nullable=True)
    
    firstTowerAssist = db.Column(db.Boolean, nullable=True)
    firstTowerKill = db.Column(db.Boolean, nullable=True)
    
    bountyLevel = db.Column(db.BigInteger, nullable=True)
    longestTimeSpentLiving = db.Column(db.BigInteger, nullable=True)
    
    killingSprees = db.Column(db.BigInteger, nullable=True)
    largestKillingSpree = db.Column(db.BigInteger, nullable=True)
    largestMultiKill = db.Column(db.BigInteger, nullable=True)
    
    doubleKills = db.Column(db.BigInteger, nullable=True)
    tripleKills = db.Column(db.BigInteger, nullable=True)
    quadraKills = db.Column(db.BigInteger, nullable=True)
    pentaKills = db.Column(db.BigInteger, nullable=True)
    unrealKills = db.Column(db.BigInteger, nullable=True)
    
    largestCriticalStrike = db.Column(db.BigInteger, nullable=True)
    
    damageDealtToBuildings = db.Column(db.BigInteger, nullable=True)
    damageDealtToObjectives = db.Column(db.BigInteger, nullable=True)
    damageDealtToTurrets = db.Column(db.BigInteger, nullable=True)
    
    damageSelfMitigated = db.Column(db.BigInteger, nullable=True)
    
    magicDamageDealt = db.Column(db.BigInteger, nullable=True)
    magicDamageDealtToChampions = db.Column(db.BigInteger, nullable=True)
    magicDamageTaken = db.Column(db.BigInteger, nullable=True)
    
    physicalDamageDealt = db.Column(db.BigInteger, nullable=True)
    physicalDamageDealtToChampions = db.Column(db.BigInteger, nullable=True)
    physicalDamageTaken = db.Column(db.BigInteger, nullable=True)
    
    trueDamageDealt = db.Column(db.BigInteger, nullable=True)
    trueDamageDealtToChampions = db.Column(db.BigInteger, nullable=True)
    trueDamageTaken = db.Column(db.BigInteger, nullable=True)
    
    totalDamageDealt = db.Column(db.BigInteger, nullable=True)
    totalDamageDealtToChampions = db.Column(db.BigInteger, nullable=True)
    totalDamageTaken = db.Column(db.BigInteger, nullable=True)
    totalDamageShieldedOnTeammates = db.Column(db.BigInteger, nullable=True)
    
    totalHeal = db.Column(db.BigInteger, nullable=True)
    totalHealsOnTeammates = db.Column(db.BigInteger, nullable=True)
    totalUnitsHealed = db.Column(db.BigInteger, nullable=True)
    
    timeCCingOthers = db.Column(db.BigInteger, nullable=True)
    totalTimeCCDealt = db.Column(db.BigInteger, nullable=True)
    totalTimeSpentDead = db.Column(db.BigInteger, nullable=True)
    
    spell1Casts = db.Column(db.BigInteger, nullable=True)
    spell2Casts = db.Column(db.BigInteger, nullable=True)
    spell3Casts = db.Column(db.BigInteger, nullable=True)
    spell4Casts = db.Column(db.BigInteger, nullable=True)
    
    summoner1Casts = db.Column(db.BigInteger, nullable=True)
    summoner1Id = db.Column(db.BigInteger, nullable=True)
    
    summoner2Casts = db.Column(db.BigInteger, nullable=True)
    summoner2Id = db.Column(db.BigInteger, nullable=True)

    neutralMinionsKilled = db.Column(db.BigInteger, nullable=True)
    totalMinionsKilled = db.Column(db.BigInteger, nullable=True)

    baronKills = db.Column(db.BigInteger, nullable=True)
    dragonKills = db.Column(db.BigInteger, nullable=True)
    
    inhibitorKills = db.Column(db.BigInteger, nullable=True)
    inhibitorTakedowns = db.Column(db.BigInteger, nullable=True)
    inhibitorsLost = db.Column(db.BigInteger, nullable=True)

    turretKills = db.Column(db.BigInteger, nullable=True)
    turretTakedowns = db.Column(db.BigInteger, nullable=True)
    turretsLost = db.Column(db.BigInteger, nullable=True)
    
    nexusKills = db.Column(db.BigInteger, nullable=True)
    nexusTakedowns = db.Column(db.BigInteger, nullable=True)
    nexusLost = db.Column(db.BigInteger, nullable=True)
    
    objectivesStolen = db.Column(db.BigInteger, nullable=True)
    objectivesStolenAssists = db.Column(db.BigInteger, nullable=True)
    
    visionScore = db.Column(db.BigInteger, nullable=True)
    visionWardsBoughtInGame = db.Column(db.BigInteger, nullable=True)
    wardsKilled = db.Column(db.BigInteger, nullable=True)
    wardsPlaced = db.Column(db.BigInteger, nullable=True)
    detectorWardsPlaced = db.Column(db.BigInteger, nullable=True)
    sightWardsBoughtInGame = db.Column(db.BigInteger, nullable=True)
    
    position = db.Column(db.String, nullable=False)
    CID = db.Column(db.BigInteger, nullable=False)
    championName = db.Column(db.String, nullable=True)
    
    champExperience = db.Column(db.BigInteger, nullable=True)
    champLevel = db.Column(db.BigInteger, nullable=True)
    
    kills = db.Column(db.BigInteger, nullable=False)
    deaths = db.Column(db.BigInteger, nullable=False)
    assists = db.Column(db.BigInteger, nullable=False)
    
    goldEarned = db.Column(db.BigInteger, nullable=False)
    goldSpent = db.Column(db.BigInteger, nullable=False)
    
    itemsPurchased = db.Column(db.BigInteger, nullable=True)
    consumablesPurchased = db.Column(db.BigInteger, nullable=True)
    
    item0 = db.Column(db.BigInteger, nullable=True)
    item1 = db.Column(db.BigInteger, nullable=True)
    item2 = db.Column(db.BigInteger, nullable=True)
    item3 = db.Column(db.BigInteger, nullable=True)
    item4 = db.Column(db.BigInteger, nullable=True)
    item5 = db.Column(db.BigInteger, nullable=True)
    item6 = db.Column(db.BigInteger, nullable=True)
    
    timePlayed = db.Column(db.BigInteger, nullable=True)
    
    gameEndedInEarlySurrender = db.Column(db.Boolean, nullable=True)
    gameEndedInSurrender = db.Column(db.Boolean, nullable=True)
    teamEarlySurrendered = db.Column(db.Boolean, nullable=True)
    
    won = db.Column(db.Boolean, nullable=True)

    user = db.relationship('UserModel', back_populates = 'games')
    game = db.relationship('GameModel', back_populates = 'users')


class UserModel(db.Model):
    __tablename__ = 'User'
    PUUID = db.Column(db.String, primary_key=True)
    SID = db.Column(db.String, nullable=False)

    tagLine=db.Column(db.String, nullable=False)
    gameName=db.Column(db.String, nullable=False)
    
    profileIcon = db.Column(db.BigInteger, nullable=True)
    
    tier = db.Column(db.String, nullable=True)
    rank = db.Column(db.String, nullable=True)
    
    wins = db.Column(db.BigInteger, nullable=True)
    losses = db.Column(db.BigInteger, nullable=True)
    
    revisionDate = db.Column(db.BigInteger, nullable=False)
    
    games = db.relationship('PlayedGame', back_populates = 'user')
    # player_frame = db.relationship('PlayerFrame', back_populates = 'user')
    
    
    def to_dict(self):
        return {
            'PUUID': self.PUUID,
            'SID': self.SID,

            'tagLine': self.tagLine,
            'gameName': self.gameName,

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
    
    time_start = db.Column(db.BigInteger, nullable=False)
    time_end = db.Column(db.BigInteger, nullable=True)
    
    season = db.Column(db.BigInteger, nullable=False)
    patch = db.Column(db.String, nullable=False)
    
    users = db.relationship('PlayedGame', back_populates = 'game')
    time_line = db.relationship('GameTimeLine', back_populates = 'game')
    # entry_number = db.relationship('TimeLineEntry', back_populates = 'game')
    # player_frame = db.relationship('PlayerFrame', back_populates = 'game')
    # event = db.relationship('Event', back_populates = 'game')

  
class GameTimeLine(db.Model):
    __tablename__ = 'Time_Line'
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    
    dataVersion = db.Column(db.BigInteger, nullable=False)
    
    frameInterval = db.Column(db.BigInteger, nullable=False)
    numFrames = db.Column(db.BigInteger, nullable=False)
    
    game = db.relationship('GameModel', back_populates = 'time_line')


class TimeLineEntry(db.Model):
    __tablename__ = 'Time_Line_Entry'
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    entryNumber = db.Column(db.BigInteger, primary_key=True)
    
    timestamp = db.Column(db.BigInteger, nullable=False)
    
    # game = db.relationship('GameModel', back_populates = 'entry_number')
    # player_frame = db.relationship('PlayerFrame', back_populates = 'entry_number')
    # event = db.relationship('Event', back_populates = 'entry_number')


class PlayerFrame(db.Model):
    __tablename__ = 'Player_Frame'
    GID = db.Column(db.String, primary_key=True)
    entryNumber = db.Column(db.BigInteger, primary_key=True)
    PUUID = db.Column(db.String, primary_key=True)
    
    #Personal Stats
    abilityHaste = db.Column(db.BigInteger, nullable=True)
    abilityPower = db.Column(db.BigInteger, nullable=True)
    armor = db.Column(db.BigInteger, nullable=True)
    armorPen = db.Column(db.BigInteger, nullable=True)
    armorPenPercent = db.Column(db.BigInteger, nullable=True)
    attackDamage = db.Column(db.BigInteger, nullable=True)
    attackSpeed = db.Column(db.BigInteger, nullable=True)
    bonusArmorPenPercent = db.Column(db.BigInteger, nullable=True)
    bonusMagicPenPercent = db.Column(db.BigInteger, nullable=True)
    ccReduction = db.Column(db.BigInteger, nullable=True)
    cooldownReduction = db.Column(db.BigInteger, nullable=True)
    health = db.Column(db.BigInteger, nullable=True)
    healthMax = db.Column(db.BigInteger, nullable=True)
    healthRegen = db.Column(db.BigInteger, nullable=True)
    lifesteal = db.Column(db.BigInteger, nullable=True)
    magicPen = db.Column(db.BigInteger, nullable=True)
    magicPenPercent = db.Column(db.BigInteger, nullable=True)
    magicResist = db.Column(db.BigInteger, nullable=True)
    movementSpeed = db.Column(db.BigInteger, nullable=True)
    omnivamp = db.Column(db.BigInteger, nullable=True)
    physicalVamp = db.Column(db.BigInteger, nullable=True)
    power = db.Column(db.BigInteger, nullable=True)
    powerMax = db.Column(db.BigInteger, nullable=True)
    powerRegen = db.Column(db.BigInteger, nullable=True)
    spellVamp = db.Column(db.BigInteger, nullable=True)
    
    #Damage Stats
    magicDamageDone = db.Column(db.BigInteger, nullable=True)
    magicDamageDoneToChampions = db.Column(db.BigInteger, nullable=True)
    magicDamageTaken = db.Column(db.BigInteger, nullable=True)
    
    physicalDamageDone = db.Column(db.BigInteger, nullable=True)
    physicalDamageDoneToChampions = db.Column(db.BigInteger, nullable=True)
    physicalDamageTaken = db.Column(db.BigInteger, nullable=True)
    
    trueDamageDone = db.Column(db.BigInteger, nullable=True)
    trueDamageDoneToChampions = db.Column(db.BigInteger, nullable=True)
    trueDamageTaken = db.Column(db.BigInteger, nullable=True)
    
    totalDamageDone = db.Column(db.BigInteger, nullable=True)
    totalDamageDoneToChampions = db.Column(db.BigInteger, nullable=True)
    totalDamageTaken = db.Column(db.BigInteger, nullable=True)
    
    #Other Stats
    currentGold = db.Column(db.BigInteger, nullable=True)
    goldPerSecond = db.Column(db.BigInteger, nullable=True)
    totalGold = db.Column(db.BigInteger, nullable=True)
    
    jungleMinionsKilled = db.Column(db.BigInteger, nullable=True)
    minionsKilled = db.Column(db.BigInteger, nullable=True)
    
    level = db.Column(db.BigInteger, nullable=True)
    xp = db.Column(db.BigInteger, nullable=True)
    
    timeEnemySpentControlled = db.Column(db.BigInteger, nullable=True)
    
    __table_args__ = (
        ForeignKeyConstraint(['GID', 'entryNumber'], ['Time_Line_Entry.GID', 'Time_Line_Entry.entryNumber']),
        ForeignKeyConstraint(['PUUID'], ['User.PUUID']),
    )
    
    # game = db.relationship('GameModel', back_populates = 'player_frame')
    # user = db.relationship('UserModel', back_populates = 'player_frame')
    # entry_number = db.relationship('TimeLineEntry', back_populates = 'player_frame')

  
class Event(db.Model):
    __tablename__ = 'Event'
    GID = db.Column(db.String, primary_key=True)
    entryNumber = db.Column(db.BigInteger, primary_key=True)
    eventNumber = db.Column(db.BigInteger, primary_key=True)
    
    timestamp = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['GID', 'entryNumber'], ['Time_Line_Entry.GID', 'Time_Line_Entry.entryNumber']),
    )