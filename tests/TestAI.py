import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Đọc dữ liệu từ các file CSV
df_users = pd.read_csv("users.csv")
df_products = pd.read_csv("products.csv")
df_interactions = pd.read_csv("interactions.csv")

# Chuyển đổi dữ liệu categorical thành số
label_encoders = {}
for col in ['UserID', 'ProductID', 'Action', 'Timestamp', 'Clicks']:
    le = LabelEncoder()
    df_interactions[col] = le.fit_transform(df_interactions[col])
    label_encoders[col] = le

# Tạo dữ liệu huấn luyện và kiểm tra
X = df_interactions[['UserID', 'ProductID', 'Clicks']]
y = df_interactions['Action']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình phân loại
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Đánh giá mô hình
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")

# Hàm dự đoán gợi ý sản phẩm cho một người dùng
def recommend_products(user_id, num_recommendations=5):
    user_id_encoded = label_encoders['UserID'].transform([user_id])[0]
    user_data = df_interactions[df_interactions['UserID'] == user_id_encoded]

    # Dự đoán cho các sản phẩm khác chưa được mua bởi người dùng
    all_product_ids = df_products['ProductID'].unique()
    recommended_products = []

    for product_id in all_product_ids:
        product_id_encoded = label_encoders['ProductID'].transform([product_id])[0]
        pred = model.predict([[user_id_encoded, product_id_encoded, 1]])  # Giả định 1 click
        if pred == label_encoders['Action'].transform(['Purchase'])[0]:
            recommended_products.append(product_id)

    return recommended_products[:num_recommendations]

# Ví dụ: Gợi ý sản phẩm cho người dùng U001
user_id = 'U001'
recommended_products = recommend_products(user_id)
print(f"Recommended products for {user_id}: {recommended_products}")
