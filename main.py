from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

names_db = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "maryam"},
    {"id": 3, "name": "arousha"},
]

@app.get("/names")
def names_list():
    return names_db

@app.post("/names")
def create_name(name:str):
    new_obj = {"id": random.randint(4, 100), "name": name}
    names_db.append(new_obj)
    return names_db

@app.get("/names/{name_id}")
def retrive_name_detail(name_id:int):
    for names in names_db:
        if names["id"] ==  name_id:
            return names
    return {"detail": "object not found"}