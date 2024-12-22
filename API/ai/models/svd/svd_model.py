import threading
import pandas as pd
from typing import Optional, Any
from ai import utils
from ai.data.model_data import ModelData
from ai.models.i_model import IModel
from ai.utils.logger import LoggerAI
from ai.utils.pconfig import PConfig
from app.db.mysql import SQLProvider
from ai.schemas.train_data import TrainData
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy, dump
from sklearn.preprocessing import LabelEncoder
from app.metrics.counters import svd_precision_value_gauge, svd_precision_calculation_counter

class SVDModel(IModel):
    stop_event = threading.Event()
    data_model = ModelData()

    def __init__(self, model_name: str, data_config: Optional[dict] = None):
        if data_config is None:
            raise Exception("Thiếu cấu hình AI")
        self.get_data_model().model_name = model_name
        self.get_data_model().data_config = data_config
        self.get_data_model().training_time = PConfig().calculate_training_time(
            data_config["training_time"]
        )

    def get_data_model(self) -> ModelData:
        return self.data_model

    def get_type_model(self) -> str:
        return str(utils.TypesModel.SVD_TYPE.value)

    def get_name_model(self) -> str:
        return str(self.get_data_model().model_name)

    def logger(self):
        return LoggerAI(f"[{self.get_type_model()}] " + f"[{self.get_name_model()}]")

    # Training system
    def train(self):
        while not self.stop_event.is_set():
            data_model = self.get_data_model()
            try:
                # Cập nhật dữ liệu
                self.update_data()

                self.logger().log_line()

                config_matrix = self.get_data_config_matrix()
                index_m = config_matrix["index"]
                cols_m = config_matrix["columns"]
                value_m = config_matrix["values"]

                index = index_m if isinstance(index_m, list) else [index_m]
                cols = cols_m if isinstance(cols_m, list) else [cols_m]
                value = value_m if isinstance(value_m, list) else [value_m]

                merge_index = index + cols
                merge_index = list(set(merge_index))

                # Gộp tất cả thành một danh sách 1 chiều
                merge_all = index + cols + value
                merge_all = list(set(merge_all))

                self.logger().log_info(
                    f"Các cột có trong danh sách data_training: {data_model.data_training.columns}"
                )
                self.logger().log_info(f"Đã gộp tất cả các cột sau: {merge_all}")

                if not set(merge_all).issubset(data_model.data_training.columns):
                    self.logger().log_error(
                        "Một hoặc nhiều cột không có trong dữ liệu huấn luyện!"
                    )
                    return

                if len(data_model.data_training[merge_all]) == 0:
                    self.logger().log_error("Dữ liệu huấn luyện rỗng!")
                    return

                for col in merge_all:
                    if data_model.data_training[col].dtype == "object":
                        if col in merge_index:
                            le = LabelEncoder()
                            data_model.data_training[col] = le.fit_transform(
                                data_model.data_training[col]
                            )
                        else:
                            # Nếu không phải ID, kiểm tra và xử lý các giá trị chuỗi
                            data_model.data_training[col] = pd.to_numeric(
                                data_model.data_training[col], errors="coerce"
                            )

                self.logger().log_info(
                    f"Dữ liệu sau khi chuyển đổi: {data_model.data_training[merge_all].head()}"
                )

                reader = Reader(rating_scale=(1, 5))
                data = Dataset.load_from_df(
                    data_model.data_training[merge_all], reader=reader
                )

                trainset, testset = train_test_split(data, test_size=0.25)
                model = SVD()
                model.fit(trainset)

                # Đánh giá mô hình
                predictions = model.test(testset)
                self.logger().log_info(
                    f"Đánh giá mô hình (rmse): {accuracy.rmse(predictions)}"
                )

                # Lưu mô hình
                dump.dump(data_model.data_config["model_path"], algo=model)
                self.logger().log_info("Mô hình đã được lưu!")
                self.logger().log_line()

                # Cập nhật giá trị mô hình cho Prometheus
                svd_precision_value_gauge.labels(model_name=self.get_name_model()).set(accuracy.rmse(predictions))
                svd_precision_calculation_counter.labels(model_name=self.get_name_model()).inc()
            except Exception as e:
                self.logger().log_error(
                    f"Xảy ra lỗi khi đang huấn luyện mô hình {str(e)}"
                )
            self.stop_event.wait(data_model.training_time)

    def run(self):
        thread = threading.Thread(target=self.train, daemon=True)
        thread.start()
        self.logger().log_info("Việc huấn luyện đang được diễn ra!")

    def stop(self):
        self.stop_event.set()
        self.logger().log_info("Việc huấn luyện đã bị tạm dừng!")

    def get_data_config_matrix(self):
        config = self.get_data_model().data_config["matrix"]
        return {
            "index": config["index"],
            "columns": config["columns"],
            "values": config["values"],
        }

    """
    @param needed: ID người dùng
    @param num_recommendations: số mô hình gợi ý
    """

    async def recommend(self, needed: Any, num_recommendations: int = 5) -> Any:
        try:
            data_model = self.get_data_model()
            model_path = data_model.data_config["model_path"]

            import os

            if not os.path.exists(model_path):
                raise Exception(f"Không tìm thấy file mô hình tại {model_path}")

            _, model = dump.load(model_path)
            if model is None:
                raise Exception("Mô hình tải lên không hợp lệ hoặc bị thiếu!")

            if data_model.data_training is None or data_model.data_training.empty:
                raise Exception(
                    "Dữ liệu huấn luyện trống, cần cập nhật dữ liệu trước khi gợi ý."
                )

            config_matrix = self.get_data_config_matrix()
            user_col = (
                config_matrix["index"][0]
                if isinstance(config_matrix["index"], list)
                else config_matrix["index"]
            )
            item_col = (
                config_matrix["columns"][0]
                if isinstance(config_matrix["columns"], list)
                else config_matrix["columns"]
            )

            all_items = data_model.data_training[item_col].unique().tolist()
            user_rated_items = data_model.data_training[
                data_model.data_training[user_col] == needed
            ][item_col].tolist()
            items_to_predict = [
                item for item in all_items if item not in user_rated_items
            ]

            if not items_to_predict:
                return []

            predictions = []
            for item in items_to_predict:
                try:
                    pred = float(model.predict(uid=str(needed), iid=str(item)).est)
                    predictions.append((str(item), pred))
                except Exception as e:
                    self.logger().log_error(
                        f"Lỗi khi dự đoán cho item {item}: {str(e)}"
                    )
                    continue

            predictions.sort(key=lambda x: x[1], reverse=True)
            top_recommendations = predictions[:num_recommendations]

            self.logger().log_info(
                f"Gợi ý cho người dùng '{needed}': {top_recommendations}"
            )
            return top_recommendations
        except Exception as e:
            self.logger().log_error(f"Lỗi khi gợi ý: {str(e)}")
            return []

    def update_data(self):
        try:
            data_model = self.get_data_model()
            data_model.data_handle.clear_data()

            # Tương lai sử dụng Redis để phát triển phần này thêm
            learning_tables = data_model.data_config["learning_tables"]
            replace_cols_tables = data_model.data_config["replace_columns_tables"]

            for table, value in learning_tables.items():
                cols = value["columns"]
                query = f"SELECT {', '.join(cols)} FROM {table}"
                result_query = SQLProvider().execute_query(query)
                pd_result = pd.DataFrame(result_query, columns=cols)

                # Xử lý tên cột
                if table in replace_cols_tables:
                    for replace in replace_cols_tables[table]:
                        col = replace.split("->")
                        pd_result.rename(columns={col[0]: col[1]}, inplace=True)

                # Xử lý dữ liệu
                result = TrainData(train_data=pd_result)
                data_model.data_handle.insert_data(table, result)

            # Gộp các bảng lại
            data_model.data_training = data_model.data_handle.merge_data(
                data_model.data_config
            )

            # Xử lý dữ liệu Matrix
            config_matrix = self.get_data_config_matrix()
            data_model.data_matrix = data_model.data_training.pivot_table(
                index=config_matrix["index"],
                columns=config_matrix["columns"],
                values=config_matrix["values"],
            )
        except Exception as e:
            self.logger().log_error(f"Lỗi tại hàm update_data: {str(e)}")
