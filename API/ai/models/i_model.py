from abc import ABC, abstractmethod
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

    def recommend(self, needed: any, num_recommendations: int = 5):
        pass 

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass
