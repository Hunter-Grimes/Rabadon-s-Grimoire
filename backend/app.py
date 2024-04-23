from flask import Flask

import os

from extensions import db, api

from apiEndpoints import(
    UserByRiotID, UserByPUUID, GameDataByPlayer, GameDataAll,
    GameIDLast20, GameIDXtoX, GameDataXtoX, UpdateUser,
    AsyncUpdateUser, generalChampStats, userTags, getUserGamesPlayed,
    userChampionInfoPage, runeRecommendation, champSelectChampInfoGeneric, champSelectChampInfoSpecific,
    getChampSpecificTags
)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
    register_endpoints()
    register_extensions(app)
    return app

def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    api.init_app(app)
    return None

def register_endpoints():
    api.add_resource(UserByRiotID, "/user/by-riotID/<tagLine>/<gameName>")
    api.add_resource(UserByPUUID, "/user/by-PUUID/<PUUID>")
    api.add_resource(GameDataByPlayer, "/game-data/by-Player/<GID>/<PUUID>")
    api.add_resource(GameDataAll, "/game-data/all/<GID>")
    api.add_resource(GameIDLast20, "/game-id/last-20/<PUUID>")
    api.add_resource(GameIDXtoX, "/game-id/x-x/<PUUID>/<x>/<y>")
    api.add_resource(GameDataXtoX, "/game-data/x-x/<PUUID>/<x>/<y>")
    api.add_resource(UpdateUser, "/update-user/<PUUID>")
    api.add_resource(AsyncUpdateUser, "/update-user/async/<PUUID>")
    api.add_resource(generalChampStats, "/user/champ-info-summary/<PUUID>")
    api.add_resource(userTags, "/user/tags/<PUUID>")
    api.add_resource(getUserGamesPlayed, "/user/games-played/<PUUID>")
    api.add_resource(userChampionInfoPage, "/user/champ-info-page/<PUUID>/<championName>")
    api.add_resource(runeRecommendation, "/rune-recommendation/<CID>")
    api.add_resource(champSelectChampInfoGeneric, "/champ-select/generic/<CID>")
    api.add_resource(champSelectChampInfoSpecific, "/champ-select/specific/<CID>/<gameName>/<tagLine>")
    api.add_resource(getChampSpecificTags, "/champ-select/tags/<CID>/<gameName>/<tagLine>/<role>")
    return None

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, threaded=True, port=8080, host="0.0.0.0") #TODO CHANGE BEFORE PRODUCTION