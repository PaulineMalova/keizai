from decouple import config

DATABASE = {
    "drivername": "postgresql",
    "host": config("DB_HOST", "localhost"),
    "port": config("DB_PORT", "5432"),
    "username": config("DB_USER", "postgres"),
    "password": config("DB_PASSWORD", "password"),
    "database": config("DB_NAME", "postgres"),
}
ACCESS_TOKEN_EXPIRATION = config("ACCESS_TOKEN_EXPIRATION", 12)
JWT_SECRET = config("JWT_SECRET", "")
