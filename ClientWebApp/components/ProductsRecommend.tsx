"use client";
import ProductItem from "./ProductItem";
import Heading from "./Heading";
import { signIn, useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

interface Product {
    id: string;
    name: string;
    price: number;
    description?: string;
    image?: string;
    gender?: string;
}

interface UserData {
    id: string;
    email: string;
}

interface RecommendResponse {
    suggestions: string[];
}

const ProductsRecommend = React.memo(() => {
    const router = useRouter();
    const [error, setError] = useState("");
    const [listProducts, setListProducts] = useState<Product[]>([]);
    const { data: session, status: sessionStatus } = useSession();
    const [userData, setUserData] = useState<UserData | null>(null);

    useEffect(() => {
        if (sessionStatus === "unauthenticated") {
            router.replace("/");
            return;
        }
        if (sessionStatus === "authenticated" && session?.user?.email) {
            const email = session.user.email;
            fetch(`http://localhost:3001/api/users/email/${email}`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error(`API error: ${res.status}`);
                    }
                    return res.json();
                })
                .then((data: UserData) => {
                    setUserData(data);
                    fetch(`http://localhost:9999/recommend-ai/svd/model_a/${data.id}/5`, {
                        method: "GET",
                        headers: {
                            "Authorization": "Bearer valid-token", // Token phù hợp với backend
                            "Content-Type": "application/json",   // Loại dữ liệu bạn gửi
                        },
                    })
                        .then((res) => {
                            if (!res.ok) {
                                throw new Error(`API error: ${res.status}`);
                            }
                            return res.json();
                        })
                        .then((data: RecommendResponse) => {
                            console.log("Received recommendations:", data);
                            if (!data?.suggestions || !Array.isArray(data.suggestions)) {
                                console.error("Invalid data format:", data);
                                return;
                            }

                            // Reset the products list before adding new ones
                            setListProducts([]);
                            
                            const fetchPromises = data.suggestions.map((data) => {
                                console.log("Fetching product with ID:", data);
                                return fetch(`http://localhost:3001/api/products/${data[0]}`)
                                    .then((res) => {
                                        if (!res.ok) {
                                            throw new Error(`API error: ${res.status}`);
                                        }
                                        return res.json();
                                    })
                                    .then((productData: Product) => {
                                        console.log("Received product data:", productData);
                                        setListProducts(currentProducts => [...currentProducts, productData]);
                                    })
                                    .catch(err => {
                                        console.error("Error in fetching product data:", err);
                                    });
                            });

                            Promise.all(fetchPromises)
                                .catch(err => {
                                    console.error("Error in fetching products:", err);
                                    setError("Failed to fetch product data");
                                });
                        })
                        .catch((err) => {
                            console.error("Failed to fetch recommend data:", err);
                            setError("Failed to fetch recommend data");
                        });
                })
                .catch((err) => {
                    console.error("Failed to fetch user data:", err);
                    setError("Failed to fetch user data");
                });
        }
    }, [sessionStatus, session, router]);

    if (sessionStatus === "loading") {
        return <h1>Loading...</h1>;
    }

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
});

export default ProductsRecommend;