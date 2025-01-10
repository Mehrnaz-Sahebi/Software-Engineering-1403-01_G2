import React from "react";
import LinkLabel from "@/components/LinkLabel";

export default function Home() {
  return (
      <div className="m-4 bg-white p-8 rounded-lg shadow-lg">
          <LinkLabel
              text="Welcome to Magical Next Word Suggestion Web!"
              link="/login"
              linkText="Login"
          />
      </div>
  );
}
