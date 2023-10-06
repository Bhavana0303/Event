from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:bhavana12@localhost:1234/events'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
pool_size=30, pool_timeout=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()