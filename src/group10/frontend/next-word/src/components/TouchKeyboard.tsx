import React from "react";

interface TouchKeyboardProps {
    onKeyPress: (key: string) => void;
    onClose: () => void;
}

const TouchKeyboard: React.FC<TouchKeyboardProps> = ({ onKeyPress, onClose }) => {
    const keys = [
        ["Esc", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
        ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
        ["Caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Enter"],
        ["Shift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Shift"],
        [ "Ctrl", "Alt", " ", "Alt", "Ctrl", "←", "↑", "↓", "→"],
    ];

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-gray-200 border-t border-gray-400 shadow-lg p-4 z-50">
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
                    <div key={rowIndex} className="flex justify-center space-x-2">
                        {row.map((key) => (
                            <button
                                key={key}
                                onClick={() => onKeyPress(key === " " ? " " : key)}
                                className={`px-4 py-2 ${
                                    ["Backspace", "Tab", "Caps", "Enter", "Shift", "Ctrl", "Alt", "Fn"].includes(key)
                                        ? "bg-gray-400 text-black"
                                        : key === " "
                                            ? "bg-gray-300 flex-grow text-black"
                                            : "bg-blue-500 text-white"
                                } rounded-md hover:bg-blue-600 focus:outline-none ${
                                    key === " " ? "flex-grow" : ""
                                }`}
                                style={{ minWidth: key === " " ? "200px" : "auto" }}
                            >
                                {key}
                            </button>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TouchKeyboard;
