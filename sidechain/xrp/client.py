import websocket
import rel
import json

class XrpClient:

    def __init__(self, url, port):
        self.url = f"{url}:{port}"
        self.websocket = None

    def on_message(self, ws, message):
        try:
            json_msg = json.loads(message)
            if "engine_result_code" not in json_msg:
                return
            if json_msg["engine_result_code"] != 0:
                return
            if "transaction" not in json_msg:
                return
            if "Memos" not in json_msg["transaction"]:
                return
            
            transaction = json_msg["transaction"]
            block_index = json_msg["ledger_index"]
            block_hash = json_msg["ledger_hash"]
            transaction_index = json_msg["meta"]["TransactionIndex"]
            transaction_hash = transaction["hash"]
            time = transaction["date"]
            
            transaction_type = None
            account = None

            if "TransactionType" in transaction:
                transaction_type = transaction["TransactionType"]
            if "Account" in transaction:
                account = transaction["Account"]

            for memo, mIdx in zip(transaction["Memos"], range(len(transaction["Memos"]))):
                memo = memo["Memo"]
                mType = None
                mFormat = None
                mData = bytearray.fromhex(memo["MemoData"]).decode()
                try:
                    mData = json.loads(mData)
                except:
                    pass

                if "MemoType" in memo:
                    mType = bytearray.fromhex(memo["MemoType"]).decode()
                if "MemoFormat" in memo:
                    mFormat = bytearray.fromhex(memo["MemoFormat"]).decode()

                parsed_memo = {
                    "account": account,
                    "block_index": block_index,
                    "block_hash": block_hash,
                    "transaction_index": transaction_index,
                    "transaction_hash": transaction_hash,
                    "transaction_time": time,
                    "transaction_type": transaction_type,
                    "memo_type": mType,
                    "memo_format": mFormat,
                    "memo_data": mData,
                    "memo_index": mIdx
                }
                print(json.dumps(parsed_memo, indent=2))
        except:
            print("Message Error.")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"Connection Closed: {close_status_code}")
        print(close_msg)

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