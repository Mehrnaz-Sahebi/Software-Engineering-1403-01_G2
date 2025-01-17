import React, { useState,useContext,useEffect } from 'react';
import '../styles/TextResult.css'
import { ContentContext } from '../contexts/ContentContext';
import { SuggestionsContext } from '../contexts/SuggestionsContext';
import SuggestionBox from './SuggestionBox';

const TextResult = ({isOpen,expandedIndex,setExpandedIndex, toggleDarkMode , isDarkMode}) => {
    const { suggestions, setSuggestions } = useContext(SuggestionsContext);
    const {content , setContent, quill, setQuill} = useContext(ContentContext);
    const [result , setResult] = useState(<></>)
    
    return (
        <div className={`sidebar-container ${isOpen ? 'sidebar-open' : ''}`}
        >
            <div className={`sidebar-content ${isOpen ? 'content-open' : ''}`}>
                {content.length===0 && <p className='no-content'>!هنوز چیزی برای بررسی وجود نداره <br/><span className='option'>&#40;: شروع به نوشتن کن تا نتایج رو ببینی</span></p>}
                {suggestions.length == 0&& content.length!=0 && <p className='congrats' dir='rtl'>تبریک! <br/><span className='good-to-go'>  مشکلی نداری :&#41; </span></p>}
                {suggestions.length>0 &&content.length>0 && suggestions.map((suggestion , index)=>(
                    <SuggestionBox toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} content = {content} suggestion={suggestion} index={index} key={index} expandedIndex={expandedIndex} setExpandedIndex={setExpandedIndex} quill={quill} setContent={setContent} setQuill={setQuill}></SuggestionBox>
                ))}
            </div>
        </div>
       
    );
};

export default TextResult;
