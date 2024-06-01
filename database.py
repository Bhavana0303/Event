from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


POSTGRES_DB_PSWD = 'maang@123'
encoded_password = quote(POSTGRES_DB_PSWD, safe='')
POSTGRES_DB_URL = 'postgres_db_url'
POSTGRES_DB_USERNAME = 'postgres_db_username'
POSTGRES_DB_NAME = 'postgres_db_name'

SQLALCHEMY_DATABASE_URL = f'postgresql://maang:{encoded_password}@178.16.139.18:5432/event_management'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
pool_size=30, pool_timeout=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
