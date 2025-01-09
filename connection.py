from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config import keys


engine = create_engine(keys.db_url)

Base = declarative_base()