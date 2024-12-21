from abc import ABC, abstractmethod
from typing import Any
from ai.data.model_data import ModelData
from logger import Logger


class IModel(ABC):
    @abstractmethod
    def get_data_model(self) -> ModelData:
        pass

    @abstractmethod
    def get_type_model(self) -> str:
        pass

    @abstractmethod
    def get_name_model(self) -> str:
        pass

    @abstractmethod
    def logger(self) -> Logger:
        pass

    @abstractmethod
    def train(self):
        pass

    async def recommend(self, needed: Any, num_recommendations: int = 5) -> Any:
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass
