from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

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


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/stock")
def check_stock(prenda: str, talla: str, color: str, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(
        Stock.prenda == prenda,
        Stock.talla == talla,
        Stock.color == color
    ).first()
    
    if stock:
        return {"prenda": prenda, "talla": talla, "color": color, "cantidad": stock.cantidad}
    
    raise HTTPException(status_code=404, detail="No se ha encontrado ninguna prenda")
