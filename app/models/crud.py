from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.schema import UserCreate

# Criar novo usuário
def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Buscar usuário por ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Buscar usuário por nome de usuário
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Listar usuários
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Deletar usuário
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    return None