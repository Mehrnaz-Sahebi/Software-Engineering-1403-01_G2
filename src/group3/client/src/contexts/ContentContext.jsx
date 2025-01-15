import React, { createContext, useState } from 'react';
export const ContentContext = createContext();

export const ContentProvider = ({ children }) => {
    const [content , setContent] = useState([]);
    const [quill,setQuill] = useState();
    return (
        <ContentContext.Provider value={{ content, setContent, quill , setQuill }}>
            {children}
        </ContentContext.Provider>
    );
};
