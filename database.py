import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. load configs
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'authdb')
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'postgres')

db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# 2. setup SQLAlchemy
Base = declarative_base()
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def init_db():
    import User 
    Base.metadata.create_all(engine)