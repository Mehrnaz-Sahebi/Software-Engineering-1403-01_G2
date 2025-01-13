'use client'
import React, { useState } from "react";
import LinkLabel from "@/components/LinkLabel";
import FormRaw from "@/components/FormRaw";
import { fetchSignup } from "../api/signup";

const SignupPage: React.FC = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");
    const [name, setName] = useState("");
    const [age, setAge] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const result = await fetchSignup(
            JSON.stringify({
                username,
                email,
                password1,
                password2,
                name,
                age,
            }),
        );

        if (result) {
            window.location.href = "/group10/login.html";
        }
    };

    return (
        <div>
            <h2 className="text-2xl font-bold text-center mb-6">Signup</h2>
            <form onSubmit={handleSubmit}>
                <FormRaw
                    htmlFor="username"
                    label="Username"
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)} />
                <FormRaw
                    htmlFor="email"
                    label="Email"
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)} />
                <FormRaw
                    htmlFor="password"
                    label="Password"
                    id="password"
                    type="password"
                    value={password1}
                    onChange={(e) => setPassword1(e.target.value)} />
                <FormRaw
                    htmlFor="password"
                    label="Confirm Password"
                    id="password2"
                    type="password"
                    value={password2}
                    onChange={(e) => setPassword2(e.target.value)} />
                <FormRaw
                    htmlFor="name"
                    label="Name"
                    id="name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)} />
                <FormRaw
                    htmlFor="age"
                    label="Age"
                    id="name"
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)} />
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Signup
                </button>
            </form>
            <LinkLabel text="Already have an account?" link="/group10/login.html" linkText="Login" />
            <LinkLabel text="Do not want to signup?" link="/group10/index.html" linkText="Home" />
        </div>
    );
};

export default SignupPage;
