from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine('sqlite:///./tes1t.db', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
