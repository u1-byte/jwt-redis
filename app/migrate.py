from app.lib.redis_client import user_client
from app.sample_data import users_data
import logging


def migrate_users_data():
    count = 0
    for user_info in users_data:
        username = user_info["username"]
        redis_key = f"user:{username}"
        if not (user_client.hget(redis_key, "username") == username):
            user_client.hset(redis_key, mapping=user_info)
            count += 1
            logging.warning(f"Add {username} records.")
    logging.warning(f"Migration completed. Added {count} records.")
