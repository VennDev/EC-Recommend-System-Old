from prometheus_client import Counter, Gauge

# SVD
svd_precision_calculation_counter = Counter(
    "svd_precision_calculation_total",
    "Số lần Precision được tính toán",
    ['model_name']
)
svd_precision_value_gauge = Gauge(
    "svd_precision_value",
    "Giá trị Precision mới nhất",
    ['model_name']
)