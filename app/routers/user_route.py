from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user_crud
from app.schemas import user_schema
from app.database.db import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter()

@router.post("/user", response_model=user_schema.UserOut)
def post_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email já cadastrado!")
    return user_crud.create_user(db=db, user=user)

@router.get("/user", response_model=list[user_schema.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return users

@router.get("/user/{user_id}", response_model=user_schema.UserOut, dependencies=[Depends(JWTBearer())])
def get_user(user_id: int, db:Session=Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

