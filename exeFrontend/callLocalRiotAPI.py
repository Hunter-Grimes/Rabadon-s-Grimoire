from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import asyncio
from willump import Willump

def waitForLogin():
    try:
        summoner = asyncio.run(getCurrPlayer())
    except Exception:
        summoner = waitForLogin()

    return summoner


async def getCurrPlayer():
    wllp = await Willump.start()
    
    data = await wllp.request("get", '/lol-summoner/v1/current-summoner')
    data = await data.json()
    summoner = {
        "gameName": data["gameName"],
        "tagLine": data["tagLine"],
        "puuid": data["puuid"]
    }
    
    await wllp.close()
    
    return summoner


async def setRunes(runes):
    wllp = await Willump.start()
    
    currentRunes = await wllp.request('get', '/lol-perks/v1/pages')
    currentRunes = await currentRunes.json()
    
    toReplace = None
    
    for page in currentRunes:
        if 'Rabadon\'s Grimoire' in page['name']:
            toReplace = page['id']
            
    if toReplace is None:
        currentPage = await wllp.request('get', '/lol-perks/v1/currentpage')
        currentPage = await currentPage.json()
        toReplace = currentPage['id']
        print(toReplace)
        
    _ = await wllp.request('delete', '/lol-perks/v1/pages/' + str(toReplace))
    
    _ = await wllp.request('post', '/lol-perks/v1/pages', data=runes)
    
    await wllp.close()


class willumpWorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    progress = Signal(object)
    result = Signal(object)


class champSelectWorker(QRunnable):
    def __init__(self, puuid):
        super(champSelectWorker, self).__init__()
        self.puuid = puuid
        self.selected = None
        self.signals = willumpWorkerSignals()
    
    @Slot()
    def run(self):
        asyncio.run(self.runHelper())
    
    async def runHelper(self):
        wllp = await Willump.start()
        
        all_events_subscription = await wllp.subscribe('OnJsonApiEvent')
    
        wllp.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/session', handler=lambda data: self.sessionData(data['data']))
        
        while True:
            data = await wllp.request('get', '/lol-champ-select/v1/session')
            data = await data.json()

            if data['timer']['adjustedTimeLeftInPhase'] == 0:
                self.signals.finished.emit()
                break
            
            await asyncio.sleep(5)
        
        await wllp.close()
            
    async def sessionData(self, data):
        # for player in data['myTeam']:
        #     if player['puuid'] == self.puuid:
        #         if self.selected == player['championId'] or player['championId'] == 0:
        #             break
        #         self.signals.progress.emit(player['championId'])
        #         self.selected = player['championId']
        self.signals.progress.emit(data)

              
class lobbyListener(QRunnable):
    def __init__(self):
        super(lobbyListener, self).__init__()
        self.signals = willumpWorkerSignals()
        self.notLobby = True

    @Slot()
    def run(self):
        asyncio.run(self.runHelper())

    async def runHelper(self):
        wllp = await Willump.start()

        all_events_subscription = await wllp.subscribe('OnJsonApiEvent')

        wllp.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/session', handler=lambda data: self.sessionStarted(data))

        while self.notLobby:
            await asyncio.sleep(5)

        await wllp.close()

    async def sessionStarted(self, data):
        if self.notLobby:
            self.signals.result.emit(None)
            self.notLobby = False
    
    @Slot()
    def clientClosed(self):
        self.notLobby = False
        

async def main():
    pass
    
if __name__ == "__main__":
    puuid = asyncio.run(getCurrPlayer())