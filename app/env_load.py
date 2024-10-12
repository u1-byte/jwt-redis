import os

flask_env = os.getenv("FLASK_ENV", "development")
jwt_algorithm = os.getenv("JWT_ALG", "HS256")
jwt_secret_key = os.getenv("JWT_SECRET_KEY", "SuperS3cr3t!")
jwt_access_exp = int(os.getenv("JWT_ACCESS_EXP", "1800"))
jwt_refresh_exp = int(os.getenv("JWT_REFRESH_EXP", "3600"))
