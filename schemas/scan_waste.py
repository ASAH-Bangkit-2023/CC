from pydantic import BaseModel, Field
from typing import Optional, Union
import datetime

class WasteScanCreate(BaseModel):
    username: str
    prediction_waste: Union[str, None] = None
    accuracy_percentage: Union[float, str, int, None] = None
    message: Union[str, None] = None
    recycle_recommendation: Union[str, None] = None
    action: Union[str, None] = None
    gcs_image_path: Optional[str]
    date_scan: Optional[datetime.datetime | str]

    class Config:
        orm_mode = True