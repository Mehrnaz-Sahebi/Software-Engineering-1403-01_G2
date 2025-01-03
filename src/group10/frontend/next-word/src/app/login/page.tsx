import React from "react";
import LinkLabel from "@/components/LinkLabel";

const LoginPage: React.FC = () => {
    return (
        <div className="bg-white p-8 rounded-lg shadow-lg w-96">
            <h2 className="m-4 text-2xl font-bold text-center mb-6">Login</h2>
            <form>
                <div className="mb-4">
                    <label htmlFor="username" className="block text-gray-700 font-medium mb-2">
                        Username
                    </label>
                    <input
                        id="username"
                        type="text"
                        className="w-full border border-gray-300 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter your username"
                    />
                </div>
                <div className="mb-6">
                    <label htmlFor="password" className="block text-gray-700 font-medium mb-2">
                        Password
                    </label>
                    <input
                        id="password"
                        type="password"
                        className="w-full border border-gray-300 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter your password"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Login
                </button>
            </form>
            <LinkLabel text="Not a Member?" link="/signup" linkText="Signup"/>
            <LinkLabel text="Want to go home?" link="/" linkText="Home"/>
        </div>
    );
};

export default LoginPage;
