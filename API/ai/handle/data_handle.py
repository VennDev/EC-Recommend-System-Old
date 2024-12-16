from ai.schemas.train_data import TrainData
from typing import Dict


class DataHandler:
    data: Dict[str, TrainData] = {}

    def __init__(self):
        pass

    def insert_data(self, key: str, data: TrainData):
        self.data[key] = data
        return True

    def get_data(self, key):
        return self.data.get(key)

    def get_all_data(self):
        return self.data

    def remove_data(self, key):
        if key in self.data:
            del self.data[key]
            return True
        return False

    def clear_data(self):
        self.data.clear()
        return True

    def merge_data(self, data_config: dict):
        try:
            config_data = data_config["rules_merge_data"] 
            if config_data is None:
                raise Exception("Thiếu cấu hình merge data")

            start_target = config_data["start_target"]
            target_data = self.data[start_target].train_data

            # Lặp qua merge_columns bằng .items() nếu merge_columns là một dictionary
            for table, value in config_data["merge_columns"].items():
                target_data = target_data.merge(
                    self.data[table].train_data, on=value, how="left"
                )

            return target_data
        except Exception as e:
            raise Exception(f"Lỗi merge data: {str(e)}")
