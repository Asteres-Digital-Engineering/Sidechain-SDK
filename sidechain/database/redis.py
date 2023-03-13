import sys
import redis

class RedisAccessObject:

    def __init__(self, host="localhost", port=6379, db=0, blockchain=None, sidechain=None, logger=print):
        if blockchain == None or sidechain == None:
            raise Exception(f"Can not create access object without blockchain ('{blockchain}') or sidechain ('{sidechain}') values.")

        try:
            self.connection = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.database_name = f"{sidechain}:{blockchain}"
            self.logger = logger
        except Exception as e:
            #TODO: Upgrade to 3.11 and use e.add_note()
            self.logger("'RedisAccessObject' has failed at establishing connection. Please check connection variables.")
            sys.exit(e)

    def commit(self, blocktime, transaction_index, data):
        try:
            unique_id = f"{blocktime}-{transaction_index}"
            self.connection.xadd(name=self.database_name, id=unique_id, fields=data)
        except Exception as e:
            self.logger(e)

    def retrieve(self, id):
        try:
            return self.connection.xrange(name=self.database_name, min=id, max=id, count=1)
        except Exception as e:
            self.logger(e)
            return None
    
    def retrieve_range(self, start, end):
        try:
            return self.connection.xrange(name=self.database_name, min=start, max=end)
        except Exception as e:
            self.logger(e)
            return None