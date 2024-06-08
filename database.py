from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class UserGameResult(Base):
    __tablename__ = 'user_game_results'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    victories = Column(Integer, default=0)

# Setup engine and session
DATABASE_URL = 'sqlite:///./game_results.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
