import os

from dotenv import load_dotenv

env = os.getenv('FLASK_ENV')
load_dotenv(os.path.join(os.path.dirname(
    __file__), '..', '..', '.env'))


class Config():
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "blacklist")
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


env_config = dict(
    config=Config,
)
