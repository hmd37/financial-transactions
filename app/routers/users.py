from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..database import get_session
from ..models import User
from ..schemas import UserCreate, UserProfile, UserLogin
from ..auth import hash_password, verify_password, create_access_token, decode_token
from ..dependencies import login_for_access_token, get_current_user

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):

    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pw)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):

    db_user = session.exec(select(User).where(User.email == user.email)).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token")
def token_route(token_data=Depends(login_for_access_token)):
    return token_data


@router.get("/profile", response_model=UserProfile)
def profile(current_user: User = Depends(get_current_user)):
    return UserProfile(
        user_id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at
    )
