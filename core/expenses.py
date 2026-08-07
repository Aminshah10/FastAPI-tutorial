from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

expenses_db = {
    1: {
        "description": "dinner",
        "amount": 22.5
    },
    2: {
        "description": "carwash",
        "amount": 9.99
    }
}

next_id = 3


@app.get("/expenses")
def get_all_expenses():
    return expenses_db


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )

    return expenses_db[expense_id]


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def add_expense(description: str, amount: float):
    global next_id

    expenses_db[next_id] = {
        "description": description,
        "amount": amount
    }

    next_id += 1

    return expenses_db[next_id - 1]


@app.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_expense(
    expense_id: int = Path(description="The id of the expense to delete", gt=0)
):
    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )

    del expenses_db[expense_id]


@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int = Path(description="The id of the expense to update", gt=0),
    description: str | None = None,
    amount: float | None = None
):
    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )

    if description is not None:
        expenses_db[expense_id]["description"] = description

    if amount is not None:
        expenses_db[expense_id]["amount"] = amount

    return expenses_db[expense_id]