"use client";
import { CustomButton, SectionTitle } from "@/components";
import { isValidEmailAddressFormat } from "@/lib/utils";
import { signIn, useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { FcGoogle } from "react-icons/fc";
import { object, set } from "zod";

class User {
    id?: string;
    email?: string;
    password?: string;
    role?: string;
    birthday?: string;
    name?: string;
    lastName?: string;
    phone?: string;
    location?: string;
    gender?: string;
}

const ProfilePage = () => {
    const router = useRouter();
    const [error, setError] = useState("");
    const { data: session, status: sessionStatus } = useSession();
    const [userData, setUserData] = useState(new User());

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
                .then((data) => {
                    setUserData(data);
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

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        // Your form submission logic here
    };

    return (
        <div className="bg-white">
            <SectionTitle title="Profile" path="Home | Profile" />
            <div className="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8 bg-white">
                <div className="sm:mx-auto sm:w-full sm:max-w-md">
                    <h2 className="mt-6 text-center text-2xl font-normal leading-9 tracking-tight text-gray-900">
                        Your Profile
                    </h2>
                </div>
                <section className="mt-8 sm:mx-auto sm:w-full">
                    <div className="container py-5">
                        <div className="col-lg-8">
                            <form className="space-y-6" onSubmit={handleSubmit}>
                                <div>
                                    <label
                                        htmlFor="email"
                                        className="block text-sm font-medium leading-6 text-gray-900"
                                    >
                                        Email address
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            id="email"
                                            name="email"
                                            type="email"
                                            autoComplete="email"
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                            value={session?.user?.email || ""}
                                            onChange={(e) =>
                                                setUserData((prev) => ({ ...prev, email: e.target.value }))
                                            }
                                            readOnly
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label
                                        htmlFor="gender"
                                        className="block text-sm font-medium leading-6 text-gray-900"
                                    >
                                        Birthday
                                    </label>
                                    <div className="mt-2">
                                        <select className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                                            <option value="Male">
                                                Male
                                            </option>
                                            <option value="Female">
                                                Female
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div>
                                    <label
                                        htmlFor="location"
                                        className="block text-sm font-medium leading-6 text-gray-900"
                                    >
                                        Location
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            id="location"
                                            name="location"
                                            type="text"
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                            value={userData?.location || ""}
                                            onChange={(e) => setUserData((prev) => ({ ...prev, location: e.target.value }))}
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label
                                        htmlFor="birthday"
                                        className="block text-sm font-medium leading-6 text-gray-900"
                                    >
                                        Birthday
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            id="birthday"
                                            name="birthday"
                                            type="date"
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                            value={new Date(userData?.birthday || "1000-10-10T00:00:00.000Z").toISOString().split("T")[0]}
                                            onChange={(e) =>
                                                setUserData((prev) => ({ ...prev, birthday: e.target.value }))
                                            }
                                        />
                                    </div>
                                </div>
                                <div>
                                    <CustomButton
                                        buttonType="submit"
                                        text="Save"
                                        paddingX={3}
                                        paddingY={1.5}
                                        customWidth="full"
                                        textSize="sm"
                                    />
                                    <p className="text-red-600 text-center text-[16px] my-4">
                                        {error && error}
                                    </p>
                                </div>
                            </form>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default ProfilePage;