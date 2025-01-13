import React from "react";
import SuggestionBox from "@/components/WordSuggestion";

export default function NextWord() {
    return (
        <div>
            <h1 className="text-2xl font-bold text-center mb-6">Next Word Suggestion</h1>
                <SuggestionBox/>
        </div>
    );
}
