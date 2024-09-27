from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
SQLALCHEMY_DATABASE_URL='postgresql://postgres:@localhost:5432/todoapp'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


