from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://cumyuvqypiiecy:e8d5c5b495af28e70576f51b69949f62c168d6b3acba2e6077195db0be8d3994@ec2-54-157-74-211.compute-1.amazonaws.com:5432/d1oegjl2qpqe47"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
