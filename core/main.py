from fastapi import FastAPI, status, HTTPException
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
# def names_list(q | None = Query(default=None, max_length=50)) imort Query class from fastapi
def names_list(search: Optional[str] = None):
    if search:
        filtered_names = [
            name for name in names_db if search.lower() in name["name"].lower()
        ]
        return filtered_names
    return names_db


@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name: str):
    new_obj = {"id": random.randint(4, 100), "name": name}
    names_db.append(new_obj)
    return names_db


@app.get("/names/{name_id}")
def retrive_name_detail(name_id: int):
    for names in names_db:
        if names["id"] == name_id:
            return names
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


@app.put("/names/{item_id}", status_code=status.HTTP_200_OK)
def names_update(item_id: int, name: str):
    for n in names_db:
        if n["id"] == item_id:
            n["name"] = name
            return {"message": f"Name with ID {item_id} updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


@app.delete("/names/{names_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name(name_id: int):
    for name in names_db:
        if name["id"] == name_id:
            names_db.remove(name)
            return {"detail": f"object with {name_id} removed successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")
