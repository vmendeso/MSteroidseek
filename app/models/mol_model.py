# app/models/mol_model.py
"""
Modelos de Dados - Moléculas e Parâmetros
-----------------------------------------
Define modelos ORM e Pydantic para moléculas, parâmetros de similaridade e requisições de dopping.
"""

# Imports SQLAlchemy e Pydantic
from sqlalchemy import Column, Integer, String
from app.config.database import Base
from pydantic import BaseModel, ConfigDict

# ---------------------- MODELO ORM ----------------------

class SimilaryStructurMol(Base):
    """
    Modelo ORM para tabela de estruturas similares de moléculas.
    """
    __tablename__ = "similary_structur_mol"
    # __table_args__ = {"schema": "msteroid"}  # Se estiver usando schema
    id = Column(Integer, primary_key=True, index=True)
    smiles = Column(String)
    model_config = ConfigDict(from_attributes=True)

# ---------------------- MODELOS PYDANTIC ----------------------

class SimilarityParams(BaseModel):
    """
    Parâmetros para análise de similaridade.
    """
    threshold: float
    mode: str
    user_input: str
    degree_freedom: int
    model_config = ConfigDict(from_attributes=True)

class DoppingRequest(BaseModel):
    """
    Modelo de requisição para análise de dopping.
    """
    mz_file: str
    intensity_file: str
    exact_mass: str
    model_config = ConfigDict(from_attributes=True)