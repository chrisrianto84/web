from dotenv import load_dotenv
import os
import redis
from os.path import join, dirname

dotenv_path = '.env'
print(dotenv_path)
load_dotenv(dotenv_path)

# REDIS_KEY = os.environ.get("REDIS_KEY")

SESSION_ID = ''

def init_session_id():
    import uuid

    ids = uuid.uuid1()
    
    return ids

def get_redis_config():
    REDIS_KEY = os.environ.get("REDIS_ADDRESS")
    print(REDIS_KEY)
    REDIS_KEY_SUB = os.environ.get("REDIS_ADDRESS_SUB")
    print(REDIS_KEY_SUB)
    return redis.Redis(host=REDIS_KEY, port=REDIS_KEY_SUB, decode_responses=True, db=0)