import React, { useState,useRef,useEffect,useContext } from 'react';
import "../styles/SuggestionBox.css"
import { SuggestionsContext } from '../contexts/SuggestionsContext';

const SuggestionBox = ({ toggleDarkMode,isDarkMode,content,suggestion, index, expandedIndex, setExpandedIndex , quill,setContent,setQuill}) => {
    const {deleteSuggestion, setSuggestions, suggestions} = useContext(SuggestionsContext);
    const [isHovered, setIsHovered] = useState(false);
    const contentRef = useRef(null);
    const [contentHeight, setContentHeight] = useState('0px');
    const fixRTLText = (text) => {
        if(!text) return;
        return text.replace(/([^\p{L}\d\s])/gu, '\u200F$1');  
    };
    

    const handleContent = () => {
        if (expandedIndex !== index) {
            setContentHeight('0px');
        } else {
            setContentHeight(`${contentRef.current.scrollHeight}px`);
        }
    }
    const handleExpandClick = () => {
        if (expandedIndex === index) {
            setExpandedIndex(null);
            handleContent();
        } else {
            setExpandedIndex(index);
            handleContent();
        }
    };
    useEffect(()=>{
        handleContent();
    },[expandedIndex])
    const { start, end, suggest } = suggestion;
    const errorPart = content.slice(start, end+1);

    const handleReplaceText = () => {
        if (quill) {
            const originalLength = end - start + 1;
            let difference = 0;
            if(!suggest) difference = -originalLength
            else difference = suggest.length - originalLength;

            const currentFormat = quill.getFormat(start);

            quill.deleteText(start, originalLength); 
            quill.insertText(start, suggest); 

            quill.formatText(0, quill.getLength(), {
                align: currentFormat.align || 'right',
                direction: currentFormat.direction || 'rtl'
            });

            setContent(quill.getText().trim());
            setSuggestions((prevSuggestions) =>
                {return prevSuggestions.map((item, idx) => {
                    if (idx === index) {
                        const updatedItem = {
                        ...item,
                        start: start, 
                        end: start + suggest.length - 1 
                    };
                    return updatedItem;
                    }
                    else if (idx > index) {
                        const updatedItem = {
                            ...item,
                            start: item.start + difference,
                            end: item.end + difference
                        };
                        return updatedItem;
                    }
                    return item;
                })
                
        });
            setSuggestions((prevSuggestions) => prevSuggestions.filter((_, idx) => idx !== index));
        }
    };
    return (
        <div
            className={`suggestion-box ${expandedIndex === index ? 'expanded' : ''}`}
            dir="rtl" 
            style={{ unicodeBidi: "plaintext" }}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            {/* Buttons: Shown Only on Hover */}
            {isHovered && (
                <div className="button-group">
                    {/* Expand Button */}
                    <button className="icon-button" title="توضیح بیشتر میخوای؟" onClick={handleExpandClick}>
                        {expandedIndex === index ? 
                        <svg fill="#434343" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fontSize="16px"><path fillRule="evenodd" d="M15 6a1 1 0 1 0-2 0v4a1 1 0 0 0 1 1h4a1 1 0 1 0 0-2h-3zm-4 8v4a1 1 0 1 1-2 0v-3H6a1 1 0 1 1 0-2h4a1 1 0 0 1 1 1" clipRule="evenodd"></path></svg> : <svg fill="#434343" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fontSize="16px"><path d="M6 19a1 1 0 0 1-1-1v-4a1 1 0 1 1 2 0v3h3a1 1 0 1 1 0 2zm12-8a1 1 0 0 1-1-1V7h-3a1 1 0 1 1 0-2h4a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1"></path></svg>}
                    </button>
                    {/* Trash Button */}
                    <button className="icon-button trash-icon" title="این پیشنهاد رو نمیخوای؟" onClick={()=>deleteSuggestion(index)}>
                    <svg fill="#434343" cursor="pointer" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fontSize="16px"><path d="M7 21c-.55 0-1.02-.196-1.412-.587A1.926 1.926 0 0 1 5 19V6a.968.968 0 0 1-.713-.287A.968.968 0 0 1 4 5c0-.283.096-.52.287-.713A.968.968 0 0 1 5 4h4a.97.97 0 0 1 .287-.712A.968.968 0 0 1 10 3h4a.97.97 0 0 1 .713.288A.968.968 0 0 1 15 4h4a.97.97 0 0 1 .712.287c.192.192.288.43.288.713s-.096.52-.288.713A.968.968 0 0 1 19 6v13c0 .55-.196 1.02-.587 1.413A1.926 1.926 0 0 1 17 21zM7 6v13h10V6zm2 10c0 .283.096.52.287.712.192.192.43.288.713.288s.52-.096.713-.288A.968.968 0 0 0 11 16V9a.967.967 0 0 0-.287-.713A.968.968 0 0 0 10 8a.968.968 0 0 0-.713.287A.968.968 0 0 0 9 9zm4 0c0 .283.096.52.287.712.192.192.43.288.713.288s.52-.096.713-.288A.968.968 0 0 0 15 16V9a.967.967 0 0 0-.287-.713A.968.968 0 0 0 14 8a.968.968 0 0 0-.713.287A.967.967 0 0 0 13 9z"></path></svg>
                    </button>
                </div>
            )}
            <div className='text-content' onClick={()=>{
                handleReplaceText();
            }}>
                <div className="suggestion-text" onClick={handleExpandClick}>
                    <span className="highlight-error">{errorPart}</span>
                    &nbsp;
                    &nbsp;
                    {fixRTLText(suggest)}
                </div>
                
                <div className="expanded-content" ref={contentRef}
                    style={{
                        maxHeight: expandedIndex === index ? contentHeight : '0px'
                    }}>
                    <p dir='rtl'><strong>توضیحات:</strong></p>
                    <p>&#34;{fixRTLText(suggest)}&#34; فرمت درستشه.</p>
                    <p>اگه این پیشنهاد رو میخوای رو من کلیک کن!</p>
                </div>
            </div>
            
            
        </div>
    );
};

export default SuggestionBox;
