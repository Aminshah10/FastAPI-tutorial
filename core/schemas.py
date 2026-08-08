from pydantic import BaseModel

class PersonBaseSchema(BaseModel):
    name : str
    
class PersonCreateSchema(PersonBaseSchema):
    pass

class PersonUpdateSchema(PersonBaseSchema):
    pass

class PersonResponseschema(PersonBaseSchema):
    id : int