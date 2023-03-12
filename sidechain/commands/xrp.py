import websocket
import _thread
import time
import rel
import json

'''
XRP Public API Commands
'''
def ping_command(id="ping"):
    command = { "id":id, "command": "ping" }
    return command

def subscribe_command(id="subscribe", accounts=[]):
    #["rrpNnNLKrartuEqfJGpqyDwPj1AFPg9vn1"]
    subscribe = { "id": id, "command": "subscribe", "accounts": accounts }
    return subscribe


'''
Websocket Events
'''
def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

def listen(url):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url, 
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    return ws
    

if __name__ == "__main__":
    url = 'wss://s.altnet.rippletest.net:51233'
    listener = listen(url)
    listener.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2,rel.abort)
    rel.dispatch()