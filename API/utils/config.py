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
        """Đọc lại file cấu hình"""
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
        """Lưu lại cấu hình vào file"""
        with open(self.config_path, "w") as file:
            self.yaml.dump(self.config, file)

    def get(self, key, default=None):
        """Lấy giá trị theo key, nếu không tồn tại thì trả về default"""
        return self.config.get(key, default)

    def get_nested_value(self, key, default=None):
        """Lấy giá trị lồng nhau (nested) theo chuỗi key dạng a.b.c"""
        keys = key.split(".")
        data = self.config

        for k in keys:
            if not isinstance(data, dict):  # Nếu data không phải dict, ngắt
                return default
            data = data.get(k, default)

        return data

    def set(self, key, value):
        """Đặt giá trị cho một key"""
        self.config[key] = value

    def set_nested_value(self, key, value):
        """Đặt giá trị cho key lồng nhau (nested) dạng a.b.c"""
        keys = key.split(".")
        data = self.config
        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
