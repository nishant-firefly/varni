from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role, Company, Entity, EntityRolePermission  # Import your SQLAlchemy models


# Database settings
SQLALCHEMY_DATABASE_URL = "postgresql://nishant:nishant@localhost/clockin"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app instance
app = FastAPI()

# Password encryption context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for input/output
class UserCreate(BaseModel):
    first_name: str
    last_name: str = None
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True

class RoleCreate(BaseModel):
    name: str

class CompanyCreate(BaseModel):
    name: str
    code: str = None
    address: str = None
    contact_number: str = None
    contact_email: str = None

class EntityCreate(BaseModel):
    entity_label: str
    url: str
    dashboard_url: str = None

# Utility function to hash passwords
def get_password_hash(password):
    return pwd_context.hash(password)

# Utility function to verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create user endpoint
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(first_name=user.first_name, last_name=user.last_name, username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by ID endpoint
@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Create role endpoint
@app.post("/roles/")
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return {"message": "Role created successfully", "role_id": db_role.id}

# Create company endpoint
@app.post("/companies/")
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(
        name=company.name, code=company.code, address=company.address, contact_number=company.contact_number, contact_email=company.contact_email
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return {"message": "Company created successfully", "company_id": db_company.id}

# Create entity endpoint
@app.post("/entities/")
def create_entity(entity: EntityCreate, db: Session = Depends(get_db)):
    db_entity = Entity(entity_label=entity.entity_label, url=entity.url, dashboard_url=entity.dashboard_url)
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return {"message": "Entity created successfully", "entity_id": db_entity.id}

# Token authentication for login
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Generate token (placeholder; implement JWT token generation here)
    token = "fake-token-for-" + user.username
    return {"access_token": token, "token_type": "bearer"}

# Assign roles to a user
@app.post("/users/{user_id}/roles/{role_id}")
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    user.roles.append(role)
    db.commit()
    return {"message": f"Role {role.name} assigned to user {user.username}"}

# Grant entity permissions to a role
@app.post("/roles/{role_id}/entities/{entity_id}/permissions")
def grant_entity_permissions(
    role_id: int, entity_id: int, create: bool = False, read: bool = False, update: bool = False, delete: bool = False, db: Session = Depends(get_db)
):
    db_role_permission = EntityRolePermission(role_id=role_id, entity_id=entity_id, create=create, read=read, update=update, delete=delete)
    db.add(db_role_permission)
    db.commit()
