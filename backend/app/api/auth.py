from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    # password validation
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")

    if len(payload.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be at most 72 characters",
        )

    # check existing user
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # hash password safely
    try:
        password_hash = hash_password(payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # create user
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # create JWT
    try:
        access_token = create_access_token({"sub": str(user.id)})
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        token = create_access_token({"sub": str(user.id)})
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"access_token": token, "token_type": "bearer"}
