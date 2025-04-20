import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

df = pd.read_csv('app/config/data/df_all_EI.csv')

DATABASE_URL = "postgresql+psycopg2://vitor:Sakod_123@localhost:5432/msteroid_db?options=-csearch_path=msteroid"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

df.to_sql('similary_structur_mol', engine, if_exists='replace', index=False)