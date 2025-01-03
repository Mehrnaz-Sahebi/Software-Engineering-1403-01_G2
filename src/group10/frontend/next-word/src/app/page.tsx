import React from "react";

export default function Home() {
  return (
      <div className="m-4 bg-white p-8 rounded-lg shadow-lg">
          <p className="text-center text-gray-600 m-6">
              Welcome to Magical Next Word Suggestion Web!{" "}
              <br/>
              <a href="/login" className="text-blue-500 hover:underline">
                  Login
              </a>
          </p>
      </div>
  );
}
