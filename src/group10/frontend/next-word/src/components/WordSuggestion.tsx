'use client';

import React, {useState, useRef, useEffect} from "react";
import {fetchSuggestions} from "@/app/api/suggest";
import TouchKeyboard from "@/components/TouchKeyboard";
import {sendWordsToLearn} from "@/app/api/learn";
import {logout} from "@/app/api/logout";

const SuggestionBox: React.FC = () => {
    const [username, setUsername] = useState("");
    const [inputValue, setInputValue] = useState("");
    const [suggestions, setSuggestions] = useState<string[]>([]);
    const [position, setPosition] = useState<{ top: number; left: number } | null>(null);
    const [enterPosition, setEnterPosition] = useState<number>(0);
    const [activeIndex, setActiveIndex] = useState<number | null>(null);
    const [autoSuggest, setAutoSuggest] = useState<boolean>(false);
    const [showKeyboard, setShowKeyboard] = useState<boolean>(false);
    const textAreaRef = useRef<HTMLTextAreaElement | null>(null);

    // Load saved content when the component mounts and username is available
    useEffect(() => {
        setUsername(localStorage.getItem("username") || "")

        if (username) {
            const savedContent = localStorage.getItem(username);
            if (savedContent) {
                setInputValue(savedContent);
            }
        }
    }, [username]);

    const handleInputChange = async (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const value = e.target.value;
        setInputValue(value);

        if (value === '\n') {
            setEnterPosition((prevState) => prevState + 1);
        }

        if (autoSuggest) {
            const lastWord = value.split(/\s+/).pop();
            if (lastWord) {
                const fetchedSuggestions = await fetchSuggestions(username, lastWord);
                setSuggestions(fetchedSuggestions);
                setActiveIndex(null);
            } else {
                setSuggestions([]);
                setActiveIndex(null);
            }
        }
    };

    const handleKeyUp = () => {
        if (textAreaRef.current) {
            const textarea = textAreaRef.current;
            const {selectionStart} = textarea;

            // Create a hidden mirror div to calculate cursor position
            const hiddenDiv = document.createElement("div");
            const style = getComputedStyle(textarea);

            // Copy textarea styles to the hidden div
            hiddenDiv.style.position = "absolute";
            hiddenDiv.style.visibility = "hidden";
            hiddenDiv.style.whiteSpace = "pre-wrap";
            hiddenDiv.style.wordWrap = "break-word";
            hiddenDiv.style.font = style.font;
            hiddenDiv.style.padding = style.padding;
            hiddenDiv.style.lineHeight = style.lineHeight;
            hiddenDiv.style.width = `${textarea.clientWidth}px`;

            // Add content up to the cursor
            hiddenDiv.textContent = textarea.value.substring(0, selectionStart).replace(/\n/g, "\u200B\n");

            document.body.appendChild(hiddenDiv);

            const cursorPos = textarea.selectionStart;

            setPosition({
                top: hiddenDiv.scrollTop + textarea.scrollTop + 50 + enterPosition * 10,
                left: hiddenDiv.scrollWidth - 280 - cursorPos * 6,
            });

            document.body.removeChild(hiddenDiv);
        }
    };

    const handleKeyPress = (key: string) => {
        if (key === "Backspace") {
            setInputValue((prev) => prev.slice(0, -1));
        }
        if (key === "\n") {
            setInputValue((prev) => prev + key);
            setEnterPosition((prevState) => prevState + 1);
        } else {
            setInputValue((prev) => prev + key);
        }
    };

    const toggleKeyboard = () => {
        setShowKeyboard((prev) => !prev);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (suggestions.length > 0) {
            if (e.key === "ArrowDown") {
                setActiveIndex((prev) => (prev === null || prev === suggestions.length - 1 ? 0 : prev + 1));
                e.preventDefault();
            } else if (e.key === "ArrowUp") {
                setActiveIndex((prev) => (prev === null || prev === 0 ? suggestions.length - 1 : prev - 1));
                e.preventDefault();
            } else if (e.key === "Enter" && activeIndex !== null) {
                handleSuggestionClick(suggestions[activeIndex]);
                e.preventDefault();
            } else if (e.key === "Escape") {
                setSuggestions([]);
                setActiveIndex(null);
            }
        }
    };

    const handleSuggestionClick = (suggestion: string) => {
        const words = inputValue.split(/\s+/);
        const newValue = [...words, suggestion].join(" ");
        setInputValue(newValue + " ");
        setSuggestions([]);
        setActiveIndex(null); // Reset active index
    };

    const handleFetchSuggestionsManually = async () => {
        const lastWord = inputValue.split(/\s+/).pop(); // Get the last word
        if (lastWord) {
            const fetchedSuggestions = await fetchSuggestions(username, lastWord);
            setSuggestions(fetchedSuggestions);
            setActiveIndex(null); // Reset active index
        }
    };

    const toggleAutoSuggest = () => {
        setAutoSuggest((prev) => !prev);
    };

    const clearTextArea = async () => {
        const words = inputValue.split(/\s+/).filter((word) => word);
        localStorage.setItem(username, "");
        setInputValue("");
        if (words.length > 0) {
            await sendWordsToLearn(username, words);
        }
    };

    const handleLogout = async () => {
        try {
            // Save content in localStorage before logout
            if (username) {
                localStorage.setItem(username, inputValue);
            }
            await logout();
            localStorage.setItem("username", "");
            window.location.href = "/group10/index.html";
        } catch (error) {
            console.error("Logout failed:", error);
        }
    };

    return (
        <div className="relative">
            <div className="flex justify-end">
                <button
                    onClick={handleLogout}
                    className="mx-1 bg-red-500 text-white px-4 py-2 rounded-md mb-2 hover:bg-red-600 focus:outline-none mr-auto"
                >
                    Logout
                </button>
                <button
                    onClick={handleFetchSuggestionsManually}
                    className="mx-1 bg-blue-500 text-white px-4 py-2 rounded-md mb-2 hover:bg-blue-600 focus:outline-none"
                >
                    Suggestion Words
                </button>
                <button
                    onClick={toggleAutoSuggest}
                    className={`mx-1 px-4 py-2 rounded-md mb-2 hover:bg-blue-600 focus:outline-none ${autoSuggest ? "bg-green-500 text-white hover:bg-green-600" : "bg-gray-500 text-white hover:bg-gray-600"
                    }`}
                >
                    {autoSuggest ? "Auto Suggest On" : "Auto Suggest Off"}
                </button>
                <button
                    onClick={toggleKeyboard}
                    className="mx-1 bg-gray-500 text-white px-4 py-2 rounded-md mb-2 hover:bg-gray-600 focus:outline-none"
                >
                    <span role="img" aria-label="keyboard">
                        ⌨️
                    </span>
                </button>
                <button
                    onClick={clearTextArea}
                    className="mx-1 bg-red-500 text-white px-4 py-2 rounded-md mb-2 hover:bg-red-600 focus:outline-none"
                >
                    Clear Text Area
                </button>
            </div>
            <textarea
                ref={textAreaRef}
                value={inputValue}
                onChange={handleInputChange}
                onKeyUp={handleKeyUp}
                onKeyDown={handleKeyDown}
                className="w-full h-40 border border-gray-300 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="متن خود را وارد نمایید..."
                dir="rtl"
            ></textarea>
            {suggestions.length > 0 && position && (
                <ul
                    style={{
                        position: "absolute",
                        top: position.top,
                        left: position.left,
                        zIndex: 1000,
                    }}
                    className="border border-gray-300 rounded-lg bg-white shadow-lg w-64"
                >
                    {suggestions.map((suggestion, index) => (
                        <li
                            key={index}
                            className={`px-4 py-2 cursor-pointer ${activeIndex === index ? "bg-blue-100" : "hover:bg-blue-50"
                            }`}
                            onClick={() => handleSuggestionClick(suggestion)}
                        >
                            {suggestion}
                        </li>
                    ))}
                </ul>
            )}
            {showKeyboard && <TouchKeyboard onKeyPress={handleKeyPress} onClose={toggleKeyboard}/>}
        </div>
    );
};

export default SuggestionBox;
