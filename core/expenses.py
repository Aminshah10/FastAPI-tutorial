from fastapi import FastAPI, HTTPException, Path, status
from expense_schema import CreateExpenseSchema, UpdateExpenseSchema, ResponseExpenseSchema

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


@app.get("/expenses", response_model=list[ResponseExpenseSchema])
def get_all_expenses():
    return [
    {"id": expense_id, **expense}
    for expense_id, expense in expenses_db.items()
    ]


@app.get("/expenses/{expense_id}", response_model=ResponseExpenseSchema)
def get_expense(expense_id: int):
    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )

    return {"id": expense_id, **expenses_db[expense_id]}


@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ResponseExpenseSchema)
def add_expense(expense : CreateExpenseSchema):
    global next_id

    expenses_db[next_id] = {
        "description": expense.description,
        "amount": expense.amount
    }

    next_id += 1

    return {"id": next_id - 1, **expenses_db[next_id-1]}


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


@app.put("/expenses/{expense_id}", response_model=ResponseExpenseSchema)
def update_expense(expense : UpdateExpenseSchema, expense_id : int = Path(..., gt=0)):
    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )

    if expense.description is not None:
        expenses_db[expense_id]["description"] = expense.description

    if expense.amount is not None:
        expenses_db[expense_id]["amount"] = expense.amount

    return {"id": expense_id, **expenses_db[expense_id]}