import React, { createContext, useState } from 'react';
export const SuggestionsContext = createContext();

export const SuggestionsProvider = ({ children }) => {
    const [suggestions , setSuggestions] = useState([]);
      const deleteSuggestion = (indexToDelete) => {
        const updatedSuggestions = suggestions.filter((_, index) => index !== indexToDelete);
        setSuggestions(updatedSuggestions); // Updates the context
    };

    return (
        <SuggestionsContext.Provider value={{ suggestions, setSuggestions, deleteSuggestion }}>
            {children}
        </SuggestionsContext.Provider>
    );
};
