from uuid import uuid4
from app.lib.pwd_util import hash_password

users_data = [
    {
        "id": str(uuid4()),
        "username": "john_doe",
        "password": hash_password("hashed_password_123"),
        "city": "New York",
        "country": "USA",
        "role": "admin",
    },
    {
        "id": str(uuid4()),
        "username": "jane_smith",
        "password": hash_password("hashed_password_456"),
        "city": "London",
        "country": "UK",
        "role": "member",
    },
    {
        "id": str(uuid4()),
        "username": "mike_ross",
        "password": hash_password("hashed_password_789"),
        "city": "Toronto",
        "country": "Canada",
        "role": "member",
    },
    {
        "id": str(uuid4()),
        "username": "lucy_adams",
        "password": hash_password("hashed_password_101"),
        "city": "Sydney",
        "country": "Australia",
        "role": "member",
    },
    {
        "id": str(uuid4()),
        "username": "alice_walker",
        "password": hash_password("hashed_password_202"),
        "city": "Berlin",
        "country": "Germany",
        "role": "member",
    },
]
