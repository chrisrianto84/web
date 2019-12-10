from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

REDIS_KEY = os.environ.get("REDIS_KEY")

SESSION_ID = ''

def init_session_id(SESSION_ID):
    import uuid

    ids = uuid.uuid1()
    
    return ids