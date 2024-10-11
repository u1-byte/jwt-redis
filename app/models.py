from uuid import uuid4
from typing import Union
import logging
from app.lib.redis_client import user_client


class User:
    def __init__(
        self,
        username: str,
        password: str,
        city: str,
        country: str,
        role: str,
        id=str(uuid4()),
    ):
        self.id = id
        self.username = username
        self.password = password
        self.city = city
        self.country = country
        self.role = role
        self.redis_key = f"user:{username}"
        self.redis_client = user_client

    def _is_username_exists(self) -> bool:
        if self.redis_client.exists(self.redis_key):
            return True
        return False

    def _set_data(self):
        self.redis_client.hmset(
            self.redis_key,
            {
                "id": self.id,
                "username": self.username,
                "password": self.password,
                "city": self.city,
                "country": self.country,
                "role": self.role,
            },
        )

    def save(self):
        if self._is_username_exists():
            raise ValueError("Username already used. Please choose different username.")
        self._set_data()
        logging.warning(f"Add {self.username} records success.")

    def update(self):
        if not self._is_username_exists():
            raise ValueError("Username not found.")
        self.id = self.redis_client.hget(self.redis_key, "id")
        self._set_data()
        logging.warning(f"Update {self.username} records success.")

    def delete(self):
        if not self._is_username_exists():
            raise ValueError("Username not found.")
        self.id = self.redis_client.delete(self.redis_key)
        logging.warning(f"Delete {self.username} records success.")

    @classmethod
    def get(cls, username: str) -> Union["User", None]:
        redis_key = f"user:{username}"
        if user_client.exists(redis_key):
            user_data = user_client.hgetall(redis_key)
            return cls(
                id=user_data["id"],
                username=user_data["username"],
                password=user_data["password"],
                city=user_data["city"],
                country=user_data["country"],
                role=user_data["role"],
            )
        return None
