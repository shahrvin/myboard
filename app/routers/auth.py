from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_password_hash, verify_password
from app.database import get_db
from app.models import Admin
from app.schemas import AdminCreate, AdminLogin, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/setup", status_code=status.HTTP_201_CREATED)
def setup_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(Admin).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An admin already exists. Setup can only be run once.",
        )
    hashed = get_password_hash(admin_data.password)
    admin = Admin(username=admin_data.username, hashed_password=hashed)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"message": "Admin created successfully", "admin_id": admin.id}


@router.post("/login", response_model=Token)
def login(login_data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(username = login_data.username).first()
    
    if not admin or not verify_password(login_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(data={"sub": admin.username, "admin_id": admin.id})
    return Token(access_token=token)
