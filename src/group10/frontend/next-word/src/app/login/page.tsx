import React from "react";
import LinkLabel from "@/components/LinkLabel";
import FormRaw from "@/components/FormRaw";

const LoginPage: React.FC = () => {
    return (
        <div>
            <h2 className="m-4 text-2xl font-bold text-center mb-6">Login</h2>
            <form>
                <FormRaw htmlFor="username" label="Username" id="username" type="text"/>
                <FormRaw htmlFor="username" label="Password" id="password" type="password"/>
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Login
                </button>
            </form>
            <LinkLabel text="Not a Member?" link="/group10/signup" linkText="Signup"/>
            <LinkLabel text="Want to go home?" link="/group10/" linkText="Home"/>
        </div>
    );
};

export default LoginPage;
