from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 'postresql://<username>:<password>@<ip-address>/hostname/<database name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Laughforhelp1!@localhost/fastapi'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#This code generally stays the same except the database url