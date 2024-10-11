from redis import Redis

HOST = "redis"
PORT = 6379
AUTH_DB = "AUTH_URL"
USER_DB = "USER_URL"
REDIS_CONFIG = {
    AUTH_DB: 0,
    USER_DB: 1,
}


class RedisClient:
    _clients = {}

    @classmethod
    def get_client(cls, config_key: str) -> Redis:
        if config_key not in cls._clients:
            if config_key not in REDIS_CONFIG:
                raise ValueError(f"Invalid config key: {config_key}")
            db_index = REDIS_CONFIG[config_key]
            # Initialize redis client for specified db index
            cls._clients[config_key] = Redis(
                host=HOST, port=PORT, db=db_index, decode_responses=True
            )
        return cls._clients[config_key]


auth_client = RedisClient.get_client(AUTH_DB)
user_client = RedisClient.get_client(USER_DB)
