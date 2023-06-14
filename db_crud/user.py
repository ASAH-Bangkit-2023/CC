from sqlalchemy.orm import Session

from models import asah_models
from schemas import user

def createUser(db: Session, user: user.UserDB):
    db_user = asah_models.User(username = user.username, full_name=user.full_name, email=user.email, password=user.hashed_password, date_user=user.date_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def getUser(db: Session, username: str):
    user = db.query(asah_models.User).filter(asah_models.User.username == username).first()
    return user if user else None

def getHashedPassword(db: Session, username: str):
    return db.query(asah_models.User.password).filter(asah_models.User.username == username).first()[0]

def getUsername(db: Session, username: str):
    user = db.query(asah_models.User.username).filter(asah_models.User.username == username).first()
    return user.username if user else None

def getEmail(db: Session, email: str):
    email_entry = db.query(asah_models.User.email).filter(asah_models.User.email == email).first()
    return email_entry.email if email_entry else None