from fastapi import FastAPI
import random
from typing import Optional

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
#def names_list(q | None = Query(default=None, max_length=50))
def names_list(search: Optional[str] = None):
    if search:
        filtered_names = [name for name in names_db if search.lower() in name["name"].lower()]
        return filtered_names
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

@app.put("/names/{item_id}")
def names_update(item_id: int, name: str):
    for n in names_db:
        if n["id"] == item_id:
            n["name"] = name
            return {"message": f"Name with ID {item_id} updated successfully"}
    return {"message": "Name not found"}

@app.delete("/names/{names_id}")
def delete_name(name_id:int):
    for name in names_db:
        if name["id"] == name_id:
            names_db.remove(name)
            return {"detail": f"object with {name_id} removed successfully"}
    return {"detail": "object not found"}