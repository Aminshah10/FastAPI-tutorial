from fastapi import FastAPI, HTTPException, Path, status, Depends
from expense_schema import CreateExpenseSchema, UpdateExpenseSchema, ResponseExpenseSchema
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from expense_database import Base, engine, get_db, Expense
from typing import Annotated

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Application startup")
    Base.metadata.create_all(bind=engine)
    yield
    print("Application shutdown")
    
app = FastAPI(lifespan=lifespan)

DbDependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/expenses", response_model=list[ResponseExpenseSchema])
def get_all_expenses(db: DbDependency):
    result = db.query(Expense).all()
    return result


@app.get("/expenses/{expense_id}", response_model=ResponseExpenseSchema)
def get_expense(expense_id: int, db: DbDependency = None):
    result = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )


@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ResponseExpenseSchema)
def add_expense(expense : CreateExpenseSchema, db: DbDependency):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@app.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_expense(
    expense_id: int = Path(description="The id of the expense to delete", gt=0), 
    db: DbDependency = None
):
    expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )
    
    db.delete(expense)
    db.commit()


@app.put("/expenses/{expense_id}", response_model=ResponseExpenseSchema)
def update_expense(expense : UpdateExpenseSchema, 
                   expense_id : int = Path(..., gt=0), 
                   db: DbDependency = None):
    result = db.query(Expense).filter(Expense.id == expense_id).one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expense found with this id"
        )
    update_data = expense.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(result, key, value)

    db.commit()
    db.refresh(result)
    return result

