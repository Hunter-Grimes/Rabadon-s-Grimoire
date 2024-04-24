from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt
import requests
from functools import cache


def fetchRolePixmap(role):
    match role:
        case 'TOP':
            pixmap = QPixmap('exeFrontend/CommunityDragon/roleIcons/icon-position-top.png')
        case 'JUNGLE':
            pixmap = QPixmap('exeFrontend/CommunityDragon/roleIcons/icon-position-jungle.png')
        case 'MIDDLE':
            pixmap = QPixmap('exeFrontend/CommunityDragon/roleIcons/icon-position-middle.png')
        case 'BOTTOM':
            pixmap = QPixmap('exeFrontend/CommunityDragon/roleIcons/icon-position-bottom.png')
        case 'UTILITY':
            pixmap = QPixmap('exeFrontend/CommunityDragon/roleIcons/icon-position-utility.png')
        case _:
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(100, 100, 100))
    
    pixmap = pixmap.scaled(30, 30, mode=Qt.SmoothTransformation)

    return pixmap


def fetchItemPixmap(itemID, IMAGE_LOCATION):
    if itemID == 0:
        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(100, 100, 100))
        return pixmap
    
    pixmap = QPixmap(IMAGE_LOCATION + 'item/' + str(itemID) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)
    
    return pixmap


def fetchChampPixmap(champName, IMAGE_LOCATION):
    pixmap = QPixmap(IMAGE_LOCATION + 'champion/' + str(champName) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)

    return pixmap


def fetchProfileInfo(PUUID, BASE_URL):
    reqStatus = requests.put(BASE_URL + '/update-user/' + str(PUUID)).status_code
    
    userData = requests.get(BASE_URL + '/user/by-PUUID/' + str(PUUID)).json()
    
    games = fetchGameInfo(userData, BASE_URL, '/0/20')
    
    data = {
        "userData": userData,
        "games": games
    }
    
    return data, reqStatus


def fetchGameInfo(userData, BASE_URL, indexes):
    gamesIDS = requests.get(BASE_URL + '/game-id/x-x/' + userData['PUUID'] + indexes).json()
    games = dict()
    for game in gamesIDS:
        gameData = requests.get(BASE_URL + '/game-data/all/' + game).json()
        games[game] = gameData

    return games


def fetchChampInfo(PUUID, BASE_URL):
    champStats = requests.get(BASE_URL + '/user/champ-info-summary/' + PUUID).json()
    gamesPlayed = requests.get(BASE_URL + '/user/games-played/' + PUUID).json()

    return gamesPlayed, champStats


def asyncUpdatePlayer(PUUID, BASE_URL):
    return requests.put(BASE_URL + '/update-user/async/' + PUUID)


def fetchChampInfoPage(PUUID, championName, BASE_URL):
    return requests.get(BASE_URL + '/user/champ-info-page/' + PUUID + '/' + championName).json()

@cache
def fetchRuneRecommendation(CID, BASE_URL):
    return requests.get(BASE_URL + '/rune-recommendation/' + str(CID)).json()

@cache
def fetchChampSelectInfoGeneric(CID, BASE_URL):
    return requests.get(BASE_URL + '/champ-select/generic/' + str(CID)).json()


def fetchChampSelectInfoSpecific(CID, gameName, tagLine, BASE_URL):
    return requests.get(BASE_URL + '/champ-select/specific/' + str(CID) + '/' + gameName + '/' + tagLine).json()


def fetchChampSpecificTags(CID, gameName, tagLine, role, BASE_URL):
    return requests.get(BASE_URL + '/champ-select/tags/' + str(CID) + '/' + gameName + '/' + tagLine + '/' + str(role)).json()