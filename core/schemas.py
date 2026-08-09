from pydantic import BaseModel, field_validator

class PersonBaseSchema(BaseModel):
    name : str
    
    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError("name must not exceed 32 characters")
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value
    
class PersonCreateSchema(PersonBaseSchema):
    pass

class PersonUpdateSchema(PersonBaseSchema):
    pass

class PersonResponseschema(PersonBaseSchema):
    id : int
