from pydantic import BaseModel
class product(BaseModel):
    id:int
    name:str
    desc:str
    price:float
    
 
      