from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
from pydantic import BaseModel

import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    prenda = Column(String, index=True)
    talla = Column(String, index=True)
    color = Column(String, index=True)
    stock = Column(Integer)

class PrendaRequest(BaseModel):
    prenda: str
    talla: str
    color: str

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/stock")
def check_stock(prenda: PrendaRequest, db: Session = Depends(get_db)):
    stock_item = db.query(Stock).filter(
        Stock.prenda == prenda.prenda,
        Stock.talla == prenda.talla,
        Stock.color == prenda.color
    ).first()
    
    if stock_item:
        return {"stock": stock_item.stock}
    
    raise HTTPException(status_code=404, detail="No se ha encontrado ninguna prenda")
