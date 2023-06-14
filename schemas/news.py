from pydantic import BaseModel
from typing import Union
from datetime import date

class NewsBase(BaseModel):
    title: Union[str, None] = None
    content: Union[str, None] = None
    author: Union[str, None] = None
    date_news: Union[date, str, None] = None
    thumbnail: Union[str, None] = None
    url: Union[str, None] = None

class NewsRead(NewsBase):
    news_id: int

class NewsReadSingle(NewsBase):
    pass

    class Config:
        orm_mode = True