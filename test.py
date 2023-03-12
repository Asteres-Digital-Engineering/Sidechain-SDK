from sidechain.xrp.client import XrpClient
from sidechain.xrp.commands import *
import time

if __name__ == "__main__":
    url = 'wss://s.altnet.rippletest.net'
    url = 'wss://s1.ripple.com'
    port = 51233
    listener = XrpClient(url, port)
    listener.connect()
    listener.listen(subscribe_stream())
    