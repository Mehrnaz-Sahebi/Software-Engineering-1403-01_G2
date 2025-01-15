import React, { useState } from "react";

interface TouchKeyboardProps {
    onKeyPress: (key: string) => void;
    onClose: () => void;
}

const TouchKeyboard: React.FC<TouchKeyboardProps> = ({ onKeyPress, onClose }) => {
    const [isShiftActive, setIsShiftActive] = useState(false);
    const [isCapsLockActive, setIsCapsLockActive] = useState(false);

    const handleKeyPress = (key: string) => {
        if (key === "Shift") {
            setIsShiftActive((prev) => !prev);
        } else if (key === "Caps") {
            setIsCapsLockActive((prev) => !prev);
        } else if (key === "Space") {
            onKeyPress(" ");
        } else if (key === "Enter") {
            onKeyPress("\n");
        } else if (key === "Tab") {
            onKeyPress("\t");
        } else {
            let transformedKey = key;
            if (isCapsLockActive && !isShiftActive) {
                transformedKey = key.toUpperCase();
            } else if (isCapsLockActive && isShiftActive) {
                transformedKey = key.toLowerCase();
                setIsShiftActive(false);
            } else if (!isCapsLockActive && isShiftActive) {
                transformedKey = key.toUpperCase();
                setIsShiftActive(false);
            }
            onKeyPress(transformedKey);
        }
    };

    const keys = [
        ["Esc", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
        ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
        ["Caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Enter"],
        ["Shift-Left", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Shift-Right"],
        ["Space"],
    ];

    return (
        <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 bg-gray-200 border-t border-gray-400 shadow-lg p-4 z-50">
            <div className="flex justify-end mb-4">
                <button
                    onClick={onClose}
                    className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 focus:outline-none"
                >
                    Close
                </button>
            </div>
            <div className="space-y-2">
                {keys.map((row, rowIndex) => (
                    <div
                        key={rowIndex}
                        className="flex justify-center space-x-1"
                        style={{ display: "grid", gridTemplateColumns: `repeat(${row.length}, 1fr)` }}
                    >
                        {row.map((key) => (
                            <button
                                key={key}
                                onClick={() => handleKeyPress(key.replace("-Left", "").replace("-Right", ""))}
                                className={`px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none ${
                                    key === "Caps" && isCapsLockActive
                                        ? "bg-green-500 text-white"
                                        : key.startsWith("Shift") && isShiftActive
                                            ? "bg-green-500 text-white"
                                            : ["Backspace", "Tab", "Caps", "Enter", "Shift-Left", "Shift-Right"].includes(
                                                key
                                            )
                                                ? "bg-gray-400 text-black"
                                                : key === "Space"
                                                    ? "bg-gray-300 flex-grow text-black"
                                                    : "bg-blue-500 text-white"
                                }`}
                            >
                                {key.replace("-Left", "").replace("-Right", "")}
                            </button>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TouchKeyboard;
