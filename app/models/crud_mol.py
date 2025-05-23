from sqlalchemy.orm import Session
from app.models.mol_model import SimilaryStructurMol

def get_all_molecules(db: Session):
    return db.query(SimilaryStructurMol).all()