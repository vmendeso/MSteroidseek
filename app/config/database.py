from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
with engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS msteroid"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função utilitária para carregar DataFrame no banco, caso necessário
def load_dataframe_to_db():
    import pandas as pd
    df = pd.read_csv('app/config/data/df_all_EI.csv')
    df.to_sql('similary_structur_mol', engine, if_exists='replace', index=False)