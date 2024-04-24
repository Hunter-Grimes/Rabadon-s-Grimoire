from extensions import db
from sqlalchemy import ForeignKeyConstraint

class PlayedGame(db.Model):
    __tablename__ = 'Played_Game'
    PUUID = db.Column(db.String, db.ForeignKey('User.PUUID'), primary_key=True)
    GID = db.Column(db.String, db.ForeignKey('Game.GID'), primary_key=True)
    
    gameName = db.Column(db.String, nullable=False)
    tagLine = db.Column(db.String, nullable=False)
    
    summonerId = db.Column(db.String, nullable=True)
    summonerLevel = db.Column(db.SmallInteger, nullable=True)
    
    primaryStyleID = db.Column(db.SmallInteger, nullable=True)
    subStyleID = db.Column(db.SmallInteger, nullable=True)
    
    primaryStyle1 = db.Column(db.SmallInteger, nullable=True)
    primaryStyle2 = db.Column(db.SmallInteger, nullable=True)
    primaryStyle3 = db.Column(db.SmallInteger, nullable=True)
    primaryStyle4 = db.Column(db.SmallInteger, nullable=True)
    
    subStyle1 = db.Column(db.SmallInteger, nullable=True)
    subStyle2 = db.Column(db.SmallInteger, nullable=True)
    
    offensePerk = db.Column(db.SmallInteger, nullable=True)
    flexPerk = db.Column(db.SmallInteger, nullable=True)
    defensePerk = db.Column(db.SmallInteger, nullable=True)
    
    firstBloodAssist = db.Column(db.Boolean, nullable=True)
    firstBloodKill = db.Column(db.Boolean, nullable=True)
    
    firstTowerAssist = db.Column(db.Boolean, nullable=True)
    firstTowerKill = db.Column(db.Boolean, nullable=True)
    
    bountyLevel = db.Column(db.Integer, nullable=True)
    longestTimeSpentLiving = db.Column(db.BigInteger, nullable=True)
    
    killingSprees = db.Column(db.SmallInteger, nullable=True)
    largestKillingSpree = db.Column(db.SmallInteger, nullable=True)
    largestMultiKill = db.Column(db.SmallInteger, nullable=True)
    
    doubleKills = db.Column(db.SmallInteger, nullable=True)
    tripleKills = db.Column(db.SmallInteger, nullable=True)
    quadraKills = db.Column(db.SmallInteger, nullable=True)
    pentaKills = db.Column(db.SmallInteger, nullable=True)
    unrealKills = db.Column(db.SmallInteger, nullable=True)
    
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

    baronKills = db.Column(db.SmallInteger, nullable=True)
    dragonKills = db.Column(db.SmallInteger, nullable=True)
    
    inhibitorKills = db.Column(db.SmallInteger, nullable=True)
    inhibitorTakedowns = db.Column(db.SmallInteger, nullable=True)
    inhibitorsLost = db.Column(db.SmallInteger, nullable=True)

    turretKills = db.Column(db.SmallInteger, nullable=True)
    turretTakedowns = db.Column(db.SmallInteger, nullable=True)
    turretsLost = db.Column(db.SmallInteger, nullable=True)
    
    nexusKills = db.Column(db.SmallInteger, nullable=True)
    nexusTakedowns = db.Column(db.SmallInteger, nullable=True)
    nexusLost = db.Column(db.SmallInteger, nullable=True)
    
    objectivesStolen = db.Column(db.SmallInteger, nullable=True)
    objectivesStolenAssists = db.Column(db.SmallInteger, nullable=True)
    
    visionScore = db.Column(db.Integer, nullable=True)
    visionWardsBoughtInGame = db.Column(db.Integer, nullable=True)
    wardsKilled = db.Column(db.Integer, nullable=True)
    wardsPlaced = db.Column(db.Integer, nullable=True)
    detectorWardsPlaced = db.Column(db.Integer, nullable=True)
    sightWardsBoughtInGame = db.Column(db.Integer, nullable=True)
    
    position = db.Column(db.String, nullable=False)
    CID = db.Column(db.SmallInteger, nullable=False)
    championName = db.Column(db.String, nullable=True)
    
    champExperience = db.Column(db.BigInteger, nullable=True)
    champLevel = db.Column(db.Integer, nullable=True)
    
    kills = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    
    goldEarned = db.Column(db.Integer, nullable=False)
    goldSpent = db.Column(db.Integer, nullable=False)
    
    itemsPurchased = db.Column(db.SmallInteger, nullable=True)
    consumablesPurchased = db.Column(db.SmallInteger, nullable=True)
    
    item0 = db.Column(db.Integer, nullable=True)
    item1 = db.Column(db.Integer, nullable=True)
    item2 = db.Column(db.Integer, nullable=True)
    item3 = db.Column(db.Integer, nullable=True)
    item4 = db.Column(db.Integer, nullable=True)
    item5 = db.Column(db.Integer, nullable=True)
    item6 = db.Column(db.Integer, nullable=True)
    
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
    
    profileIcon = db.Column(db.Integer, nullable=True)
    
    tier = db.Column(db.String, nullable=True)
    rank = db.Column(db.String, nullable=True)
    
    wins = db.Column(db.Integer, nullable=True)
    losses = db.Column(db.Integer, nullable=True)
    
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
    
    season = db.Column(db.Integer, nullable=False)
    patch = db.Column(db.String, nullable=False)
    
    users = db.relationship('PlayedGame', back_populates = 'game')
    time_line = db.relationship('GameTimeLine', back_populates = 'game')
    # entry_number = db.relationship('TimeLineEntry', back_populates = 'game')
    # player_frame = db.relationship('PlayerFrame', back_populates = 'game')
    # event = db.relationship('Event', back_populates = 'game')

  
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
    
    timestamp = db.Column(db.BigInteger, nullable=False)
    
    # game = db.relationship('GameModel', back_populates = 'entry_number')
    # player_frame = db.relationship('PlayerFrame', back_populates = 'entry_number')
    # event = db.relationship('Event', back_populates = 'entry_number')


class PlayerFrame(db.Model):
    __tablename__ = 'Player_Frame'
    GID = db.Column(db.String, primary_key=True)
    entryNumber = db.Column(db.Integer, primary_key=True)
    PUUID = db.Column(db.String, primary_key=True)
    
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
    
    level = db.Column(db.SmallInteger, nullable=True)
    xp = db.Column(db.Integer, nullable=True)
    
    timeEnemySpentControlled = db.Column(db.Integer, nullable=True)
    
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
    entryNumber = db.Column(db.Integer, primary_key=True)
    eventNumber = db.Column(db.Integer, primary_key=True)
    
    timestamp = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['GID', 'entryNumber'], ['Time_Line_Entry.GID', 'Time_Line_Entry.entryNumber']),
    )