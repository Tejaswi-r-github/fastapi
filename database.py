from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine, create_engine


db_url = "postgresql+psycopg2://postgres:Adityateju@localhost:5432/tejaswidbb"
engine=create_engine(db_url)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)
