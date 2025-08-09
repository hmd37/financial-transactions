from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from .database import init_db, get_session
from .models import User, UserCreate, UserProfile
from .auth import hash_password, verify_password, create_access_token, decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (optional cleanup)

app = FastAPI(lifespan=lifespan)

# User Registration
@app.post("/api/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

# User Login
@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Swagger will send "username" field — we treat it as email
    db_user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

# Get User Profile
@app.get("/api/profile", response_model=UserProfile)
def profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.get(User, int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(user_id=user.id, username=user.username, email=user.email, created_at=user.created_at)
