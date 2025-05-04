import os
from ruamel.yaml import YAML
from logger import Logger


class Config:
    def __init__(self, config_path="config.yml"):
        self.config_path = config_path
        self.yaml = YAML()
        self.config = {}
        self.reload()

    def reload(self):
        if not os.path.exists(self.config_path):
            Logger().log_error(f"Không tìm thấy file cấu hình: {self.config_path}")
            raise FileNotFoundError(f"Không tìm thấy file cấu hình: {self.config_path}")

        with open(self.config_path, "r") as file:
            try:
                self.config = self.yaml.load(file)
            except Exception as e:
                Logger().log_error(f"Không thể đọc file cấu hình: {str(e)}")
                raise ValueError(f"Không thể đọc file cấu hình: {str(e)}")

    def save(self):
        with open(self.config_path, "w") as file:
            self.yaml.dump(self.config, file)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_nested_value(self, key, default=None):
        keys = key.split(".")
        data = self.config

        for k in keys:
            if not isinstance(data, dict):
                return default
            data = data.get(k, default)

        return data

    def set(self, key, value):
        self.config[key] = value

    def set_nested_value(self, key, value):
        keys = key.split(".")
        data = self.config
        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
