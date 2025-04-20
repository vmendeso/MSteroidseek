from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://vitor:Sakod_123@localhost:5432/msteroid_db?options=-csearch_path=msteroid"

engine = create_engine(DATABASE_URL)
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