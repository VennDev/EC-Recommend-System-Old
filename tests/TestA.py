import numpy as np
import tensorflow as tf
from tensonflow.keras.layers import Input, Embedding, Flatten, Dense
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Giả sử bạn đã có dữ liệu người dùng và sản phẩm
user_ids = np.array([0, 1, 2, 1, 0])  # User IDs
product_ids = np.array([10, 15, 13, 10, 14])  # Product IDs
ratings = np.array([5, 4, 3, 4, 2])  # Ratings

# Số lượng người dùng và sản phẩm (tính từ ID lớn nhất + 1)
num_users = np.max(user_ids) + 1
num_products = np.max(product_ids) + 1

# Kích thước của các embedding vector
embedding_dim = 10

# Mô hình Neural Collaborative Filtering (NCF)
user_input = Input(shape=(1,), dtype=tf.int32, name='user_input')
product_input = Input(shape=(1,), dtype=tf.int32, name='product_input')

# Embedding layers
user_embedding = Embedding(input_dim=num_users, output_dim=embedding_dim)(user_input)
product_embedding = Embedding(input_dim=num_products, output_dim=embedding_dim)(product_input)

# Flatten the embeddings
user_flat = Flatten()(user_embedding)
product_flat = Flatten()(product_embedding)

# Concatenate the user and product embeddings
merged = tf.keras.layers.concatenate([user_flat, product_flat])

# Fully connected layers
fc1 = Dense(128, activation='relu')(merged)
fc2 = Dense(64, activation='relu')(fc1)
output = Dense(1, activation='linear')(fc2)  # Dự đoán rating (sử dụng activation linear)

# Tạo và biên dịch mô hình
model = Model(inputs=[user_input, product_input], outputs=output)
model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mae'])

# Xem tóm tắt mô hình
model.summary()

# Huấn luyện mô hình
model.fit([user_ids, product_ids], ratings, epochs=10, batch_size=2, verbose=1)
