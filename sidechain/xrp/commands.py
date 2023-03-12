import json
'''
XRP Public API Commands
'''
def ping_command(id="ping"):
    command = { "id":id, "command": "ping" }
    return json.dumps(command)

def subscribe_accounts(id="subscribe", accounts=[]):
    #["rrpNnNLKrartuEqfJGpqyDwPj1AFPg9vn1"]
    subscribe = { "id": id, "command": "subscribe", "accounts": accounts }
    return json.dumps(subscribe)

def subscribe_stream(id="subscribe", streams=["transactions_proposed"]):
    #["rrpNnNLKrartuEqfJGpqyDwPj1AFPg9vn1"]
    subscribe = { "id": id, "command": "subscribe", "streams":streams }
    return json.dumps(subscribe)


