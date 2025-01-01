"use client";
import ProductItem from "./ProductItem";
import Heading from "./Heading";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

interface RecommendResponse {
  suggestions: string[];
}

const ProductsLike = ({ idCategory }: { idCategory: string }) => {
  const router = useRouter();
  const [error, setError] = useState("");
  const [listProducts, setListProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch(`http://localhost:9999/recommend-like-category/${idCategory}/5`, {
      method: "GET",
      headers: {
        Authorization: "Bearer valid-token", // Token phù hợp với backend
        "Content-Type": "application/json", // Loại dữ liệu bạn gửi
      },
    })
      .then((response) => response.json())
      .then((data: RecommendResponse) => {
        if (!data?.suggestions || !Array.isArray(data.suggestions)) {
          console.error("Invalid data format:", data);
          return;
        }
        setListProducts(data.suggestions);
      })
      .catch((error) => {
        setError("Error fetching products: " + error);
      });
  }, [idCategory, router]);

  return (
    <div className="bg-blue-500 border-t-4 border-white">
      <div className="max-w-screen-2xl mx-auto pt-20">
        <Heading title="RECOMMEND PRODUCTS" />
        <div className="grid grid-cols-4 justify-items-center max-w-screen-2xl mx-auto py-10 gap-x-2 px-10 gap-y-8 max-xl:grid-cols-3 max-md:grid-cols-2 max-sm:grid-cols-1">
          {listProducts.map((product: Product) => (
            <ProductItem key={product.id} product={product} color="white" />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductsLike;
