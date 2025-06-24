from ..extensions import mongo_db
from datetime import datetime, timezone

def create_log(action, user_id):
    log_entry = {'action': action, 'user_id': user_id, 'timestamp': datetime.now(timezone.utc)}
    mongo_db.logs.insert_one(log_entry)

def get_logs():
    logs = list(mongo_db.logs.find().sort('timestamp', -1))
    for log in logs:
        log['_id'] = str(log['_id'])
        log['timestamp'] = log['timestamp'].isoformat()
    return logs
