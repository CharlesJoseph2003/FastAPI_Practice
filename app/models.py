from fastapi import FastAPI
from pydantic import BaseModel

#this is defining a pydantic model
#any object created from it will have an id and an item
#BaseModel is a class in pydantic that is used for data validation
#serialization
class Todo(BaseModel):
    # id: int
    item: str