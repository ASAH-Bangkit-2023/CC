from pydantic import BaseModel
from datetime import date

class PointSystemBase(BaseModel):
    username: str
    total_points: int
    date_point: date

class PointSystemCreate(PointSystemBase):
    pass

class PointSystem(PointSystemBase):
    id: int

    class Config:
        orm_mode = True
