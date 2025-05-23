from sqlalchemy import Column, Integer, String
from app.config.database import Base  # Ou de onde vier seu Base
from pydantic import BaseModel

class SimilaryStructurMol(Base):
    __tablename__ = "similary_structur_mol"
    __table_args__ = {"schema": "msteroid"}  # Se estiver usando esquema

    id = Column(Integer, primary_key=True, index=True)  # Obrigatório!
    smiles = Column(String)
    
class SimilarityParams(BaseModel):
    threshold: float
    mode: str
    user_input: str
    degree_freedom: int