from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.config import Config
from .routes import search_hint, re_like_category_product

configData = Config().get("app_settings")
if configData is None:
    raise Exception("Dữ liệu cấu hình hệ thống không tồn tại")

configMiddleware = configData["middleware"]
app = FastAPI(title=configData["name"], version="1.0.0")
app.include_router(search_hint.router, tags=["Tìm kiếm"])
app.include_router(re_like_category_product.router, tags=["Danh sách sản phẩm theo loại"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=configMiddleware["origins"],
    allow_credentials=configMiddleware["credentials"],
    allow_methods=configMiddleware["methods"],
    allow_headers=configMiddleware["headers"],
)
