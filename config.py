from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://ocbymgrarztnfz:800cf3f95f36cc2981e8f941bae2e38e1df2d7b5945f7344a208da7e8c3ca872@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d922ac2o6nekuf"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
