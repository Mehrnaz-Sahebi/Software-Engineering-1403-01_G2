import React from "react";
import LinkLabel from "@/components/LinkLabel";

export default function Home() {
    return (
        <div className="m-4 bg-white p-8 rounded-lg shadow-lg">
            <LinkLabel
                text="Welcome to Magical Next Word Suggestion Web!"
                link="/group10/login.html"
                linkText="Login"
            />
            <LinkLabel
                text="Do not have an account? No problem! Signup now!"
                link="/group10/signup.html"
                linkText="Signup"
            />
        </div>
    );
}
