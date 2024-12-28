from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config import db_url


engine = create_engine(db_url)

Base = declarative_base()