from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config

DB_URL = Config.DATABASE_URL

engine = create_async_engine(url=DB_URL, echo=True)
