import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://shop:shop@localhost:5432/shopdb")

engine = create_engine(DATABASE_URL,
                       pool_size=10,
                       max_overflow=5,
                       pool_timeout=30
                       )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()