from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def getSession():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

@app.get("/")
def getItems(session: Session = Depends(getSession)):
    items = session.query(models.Item).all()
    return items

@app.get("/{id}")
def getItem(id:int, session: Session = Depends(getSession)):
    item = session.query(models.Item).get(id)
    return item

@app.post("/")
def addItem(item: schemas.Item, session: Session = Depends(getSession)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.post("/{id}")
def updateItem(id:int, item:schemas.Item, session: Session = Depends(getSession)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

@app.delete("/{id}")
def deleteItem(id:int, session: Session = Depends(getSession)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return "Item was deleted!"

