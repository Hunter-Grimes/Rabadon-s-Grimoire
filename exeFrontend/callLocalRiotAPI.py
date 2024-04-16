from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import asyncio
from willump import Willump

global client
client = True


def clientClosed():
    global client
    client = False


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


async def lobbyStartListener():
    global lobby
    global client
    
    lobby = False
    wllp = await Willump.start()
    
    lobby_start = await wllp.subscribe('OnJsonApiEvent')
    wllp.subscription_filter_endpoint(lobby_start, '/lol-champ-select/v1/session', handler=lobbyCreated)
    
    while True:
        if lobby or not client:
            await wllp.close()
            return
        await asyncio.sleep(5)

       
async def lobbyCreated(data):
    global lobby
    lobby = True
    return


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

class champSelectSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    progress = Signal(int)

class champSelectWorker(QRunnable):
    def __init__(self, puuid):
        super(champSelectWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.puuid = puuid
        self.selected = None
        self.signals = champSelectSignals()
    
    @Slot()
    def run(self):
        asyncio.run(self.runHelper())
        self.signals.finished.emit()
    
    async def runHelper(self):
        wllp = await Willump.start()
        
        all_events_subscription = await wllp.subscribe('OnJsonApiEvent')
    
        wllp.subscription_filter_endpoint(all_events_subscription, '/lol-champ-select/v1/session', handler=lambda data: self.sessionData(data['data']))
        
        while True:
            data = await wllp.request('get', '/lol-champ-select/v1/current-champion')
            data = await data.json()

            if data != 0:
                self.signals.progress.emit(data)
                break
            
            await asyncio.sleep(5)
        
        await wllp.close()
            
    async def sessionData(self, data):
        for player in data['myTeam']:
            if player['puuid'] == self.puuid:
                if self.selected == player['championId'] or player['championId'] == 0:
                    break
                self.signals.progress.emit(player['championId'])
                self.selected = player['championId']
        
        
        
async def main():
    pass
    
if __name__ == "__main__":
    puuid = asyncio.run(getCurrPlayer())