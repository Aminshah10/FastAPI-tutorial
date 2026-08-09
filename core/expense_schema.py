from pydantic import BaseModel, Field

class ResponseExpenseSchema(BaseModel):
    id : int
    description : str
    amount : float
    

class CreateExpenseSchema(BaseModel):
    description : str = Field(..., max_length=100)
    amount : float = Field(..., gt=0)
    
class UpdateExpenseSchema(BaseModel):
    description: str | None = Field(default=None, max_length=100)
    amount: float | None = Field(default=None, gt=0)