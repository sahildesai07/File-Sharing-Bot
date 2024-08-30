#(©)CodeXBotz




import pymongo, os
from config import DB_URI, DB_NAME
from datetime import datetime, timedelta

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']
verification_log_collection = db['verification_logs']

async def log_verification(user_id):
    await verification_log_collection.insert_one({
        "user_id": user_id,
        "timestamp": datetime.utcnow()
    })

async def get_verification_count(timeframe):
    current_time = datetime.utcnow()
    
    if timeframe == "24h":
        start_time = current_time - timedelta(hours=24)
    elif timeframe == "today":
        start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    elif timeframe == "monthly":
        start_time = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    count = await verification_log_collection.count_documents({
        "timestamp": {"$gte": start_time, "$lt": current_time}
    })
    
    return count

async def cleanup_old_logs():
    expiry_time = datetime.utcnow() - timedelta(hours=24)
    await verification_log_collection.delete_many({
        "timestamp": {"$lt": expiry_time}
    })


async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return
