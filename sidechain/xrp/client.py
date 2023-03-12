import websocket
import rel

'''
Websocket Events
'''
class XrpClient:

    def __init__(self, url, port):
        self.url = f"{url}:{port}"
        self.websocket = None

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Closed Connection.")

    def on_open(self, ws):
        print("Opened Connection.")

    def connect(self):
        ws = websocket.WebSocketApp(self.url, 
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.websocket = ws
    
    def listen(self, message=""):
        self.websocket.run_forever(dispatcher=rel, reconnect=5)
        self.send(message)
        rel.signal(2,rel.abort)
        rel.dispatch()
    
    def send(self, message):
        self.websocket.send(message)
    