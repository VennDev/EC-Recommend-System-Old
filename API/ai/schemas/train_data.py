from pydantic import BaseModel
from pandas import DataFrame


class TrainData(BaseModel):
    train_data: DataFrame

    class Config:
        arbitrary_types_allowed = True
