from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
Database_url = os.getenv("DATABASE_URL")
engine = create_engine(Database_url)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()