from sqlalchemy.orm import Session

from passlib.context import CryptContext

from ..models.user_model import User

from ..schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user:UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email,
                   name=user.name,
                   password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session):
    return db.query(User).all()

