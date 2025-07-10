from sqlmodel import SQLModel, Field

class Item(SQLModel,table=True):
    id:int = Field(default=None, primary_key=True)
    name:str = Field(max_length=100, nullable=False)
    description:str = Field(max_length=500, nullable=True)