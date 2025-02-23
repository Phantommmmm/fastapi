from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os
import json

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
def check_stock(prenda: str, db: Session = Depends(get_db)):
    try:
        prenda_data = json.loads(prenda)
        if isinstance(prenda_data, str):
            prenda_data = json.loads(prenda_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for prenda")

    for key in ["prenda", "talla", "color"]:
        if key not in prenda_data:
            raise HTTPException(status_code=400, detail=f"Missing '{key}' in prenda JSON")
    
    stock_item = db.query(Stock).filter(
        Stock.prenda == prenda_data["prenda"],
        Stock.talla == prenda_data["talla"],
        Stock.color == prenda_data["color"]
    ).first()

    if stock_item:
        return {"stock": stock_item.stock}
    
    raise HTTPException(status_code=404, detail="No se ha encontrado ninguna prenda")
