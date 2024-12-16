from pandas import DataFrame
from ai.handle.data_handle import DataHandler


class ModelData:
    def __init__(self, model_name=""):
        self.model_name = model_name
        self.last_time_update = None
        self.data_config = {}
        self.data_handle = DataHandler()
        self.data_training = DataFrame()
        self.data_matrix = DataFrame()
        self.training_time = 60 * 60  # 1 giờ