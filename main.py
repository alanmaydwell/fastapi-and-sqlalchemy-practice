from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from .database import SessionLocal
from .datalayer import get_creatures, add_creature, get_creature, delete_creature


class Thing(BaseModel):
    id: int
    name: str = ""

things = []


def get_next_id() -> int:
    return len(things)


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


app = FastAPI()


@app.get("/")
def confirmation_message():
    return "Howdy-doodly-do from API!"


@app.get("/show_creatures")
def show_creatures(database=Depends(get_db)):
    result = get_creatures(database)
    return result

@app.get("/show_creature")
def show_creature(id: int, database=Depends(get_db)):
    result = get_creature(id, database)
    return result


@app.post("/create_creature")
def create_creature(name: str, database=Depends(get_db)):
    creature_id = add_creature(name, database)
    return {"message": f"Created: {name} with id {creature_id}"}


@app.delete("/remove_creature")
def remove_creature(id: int, database=Depends(get_db)):
    rowcount = delete_creature(id, database)
    return {"message": f"Deleted {rowcount} row(s)"}
    

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id >= get_next_id() or item_id < 0:  
        raise HTTPException(status_code=404, detail=f"Bad id: {item_id}")
    return things[item_id]


@app.get("/list_items")
def list_items():
    """Lists all the items"""
    return things


@app.post("/additem")
def add_item(name: str = ""):
    newthing = Thing(id=get_next_id(), name=name)
    things.append(newthing)
    return {"message": f"Added: {newthing}"}


@app.put("/update_item")
def update_item(thing: Thing):
    if thing.id >= get_next_id() or thing.id < 0:  
        raise HTTPException(status_code=404, detail=f"Bad id: {thing.id}")
    things[thing.id] = thing
    return {"message": f"Updated: {thing}"}
