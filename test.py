from sidechain.xrp.client import XrpClient
from sidechain.database.redis import RedisAccessObject
from sidechain.xrp.commands import *

if __name__ == "__main__":
    #url = 'wss://s.altnet.rippletest.net'
    url = 'wss://s1.ripple.com'
    port = 51233
    database = RedisAccessObject(blockchain="xrp", sidechain="test")
    listener = XrpClient(url, port, database)
    listener.connect()
    listener.listen(subscribe_stream())