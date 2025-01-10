import React from "react";
import LinkLabel from "@/components/LinkLabel";
import FormRaw from "@/components/FormRaw";

const SignupPage: React.FC = () => {
    return (
        <div>
            <h2 className="text-2xl font-bold text-center mb-6">Signup</h2>
            <form>
                <FormRaw htmlFor="username" label="Username" id="username" type="text"/>
                <FormRaw htmlFor="email" label="Email" id="email" type="email"/>
                <FormRaw htmlFor="password" label="Password" id="password" type="password"/>
                <FormRaw htmlFor="password" label="Confirm Password" id="password2" type="password"/>
                <FormRaw htmlFor="name" label="Name" id="name" type="text"/>
                <FormRaw htmlFor="age" label="Age" id="name" type="number"/>
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Signup
                </button>
            </form>
            <LinkLabel text="Already have an account?" link="/login" linkText="Login"/>
            <LinkLabel text="Do not want to signup?" link="/" linkText="Home"/>
        </div>
    );
};

export default SignupPage;
