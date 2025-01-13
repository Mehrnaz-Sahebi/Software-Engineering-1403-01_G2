'use client'
import React, { useState } from "react";
import LinkLabel from "@/components/LinkLabel";
import FormRaw from "@/components/FormRaw";
import { fetchCSRF } from "../api/csrf";

const LoginPage: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const csrfToken = await fetchCSRF()

        const response = await fetch("/group10/api/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ username, "pass": password }),
        });

        if (response.ok) {
            window.location.href = "/group10/next-word.html";
        } else {
            console.log("Failed to login.");
        }
    };

    return (
        <div>
            <h2 className="m-4 text-2xl font-bold text-center mb-6">Login</h2>
            <form onSubmit={handleSubmit}>
                <FormRaw
                    htmlFor="username"
                    label="Username"
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <FormRaw
                    htmlFor="password"
                    label="Password"
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Login
                </button>
            </form>
            <LinkLabel text="Not a Member?" link="/group10/signup.html" linkText="Signup" />
            <LinkLabel text="Want to go home?" link="/group10/index.html" linkText="Home" />
        </div>
    );
};

export default LoginPage;