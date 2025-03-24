from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "postgresql://postgres:ashish2002@localhost:5432/contacts_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    linkedId = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    linkPrecedence = Column(String, nullable=False)  # "primary" or "secondary"
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    deletedAt = Column(DateTime, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Model
class ContactRequest(BaseModel):
    email: str = None
    phoneNumber: str = None

# API Endpoint
@app.post("/identify")
def identify_contact(request: ContactRequest, db: Session = Depends(get_db)):
    existing_contact = db.query(Contact).filter(
        (Contact.email == request.email) | (Contact.phoneNumber == request.phoneNumber)
    ).first()
    
    if existing_contact:
        return {"message": "Contact found", "contact": existing_contact}
    
    new_contact = Contact(
        email=request.email,
        phoneNumber=request.phoneNumber,
        linkPrecedence="primary"
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    
    return {"message": "New contact created", "contact": new_contact}
