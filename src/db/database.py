from databases import Database
from sqlalchemy import MetaData, create_engine


DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL, echo=True)
