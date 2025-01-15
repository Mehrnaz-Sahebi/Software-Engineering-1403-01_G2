import React, { useEffect,useContext,useState,useRef } from "react";
import { useQuill } from "react-quilljs";
import "quill/dist/quill.snow.css";
import "../styles/TextEditor.css";
import Quill from "quill";
import ReactDOMServer from 'react-dom/server'; 
import { FaTrash } from 'react-icons/fa';
import { SuggestionsContext } from "../contexts/SuggestionsContext";
import { ContentContext } from "../contexts/ContentContext";
import axios from "axios";
const Inline = Quill.import('blots/inline');
const Align = Quill.import('formats/align');
const Direction = Quill.import('formats/direction');
const Font = Quill.import('formats/font');
const Size = Quill.import('formats/size');

Font.whitelist = [
    'arial', 
    'courier', 
    'tahoma', 
    'b-nazanin' 
];
Quill.register(Font, true);

Quill.register(Align, true);
Quill.register(Direction, true);

class RedUnderlineBlot extends Inline {
    static create(value) {
        const node = super.create();
        node.classList.add('protected-red-underline');
        node.style.textDecoration = 'underline wavy red';
        node.setAttribute("data-suggestion-index", String(value));
        return node;
    }

    static formats(node) {
        return node.getAttribute('data-suggestion-index');
    }
}

RedUnderlineBlot.blotName = 'redUnderline';
RedUnderlineBlot.tagName = 'span';
Quill.register(RedUnderlineBlot, true);



Size.whitelist = ['16px', '18px', '20px', '24px'];
Quill.register(Size, true);

const TextEditor = ({expandedIndex,setExpandedIndex,isOpen , setIsOpen}) => {
    const { suggestions, setSuggestions } = useContext(SuggestionsContext);
    const {content , setContent, setQuill} = useContext(ContentContext);
    const debounceTimerRef = useRef(null);
    const isFormattingRef = useRef(false);
    const [apiContent,setApiContent] = useState();
    const modules = {
        toolbar: {
            container: [
                [{ size: Size.whitelist }],
                [{ font: Font.whitelist }],
                ['bold', 'italic', 'underline'],
                [{ 'color': [] }, { 'background': [] }],
                [{ align: [] }],
                [{ 'direction': 'rtl' }],
                [{ list: 'ordered' }, { list: 'bullet' }],
            ],
        },
    };

    const formats = [
        'size', 'font',
        'bold', 'italic', 'underline',
        'color', 'background',
        'align',
        'direction',
        'list',
        'redUnderline'
    ];

    const { quill, quillRef } = useQuill({ modules, formats });
    useEffect(()=>{
        setQuill(quill);
    },[quill])
    

    useEffect(() => {
        if (quill) {
            quill.format('align', 'right');
            quill.format('direction', 'rtl');
            quill.format('font', 'b-nazanin');
            quill.getModule('toolbar').container.querySelector('.ql-font').value = 'b-nazanin';

            quill.root.dataset.placeholder
            = "  متن خود را اینجا بنویسید...";
            const toolbar = quill.getModule('toolbar');
            const button = document.createElement('button');
            button.innerHTML = ReactDOMServer.renderToString(<FaTrash />);
            button.classList.add('ql-customTrash');
            button.onclick = () => {
                quill.setContents([]);
                quill.format('align', 'right');
                quill.format('direction', 'rtl')
                quill.root.dataset.placeholder 
                = "  متن خود را اینجا بنویسید...";
                button.blur();  
            };

            // Attach the button to the toolbar
            toolbar.container.appendChild(button);
            quill.on('text-change', () => {
                if(isFormattingRef.current) return;

                const text = quill.getText().trim();
                setContent(text);
                setApiContent(text);
                if (quill.getLength() > 1) {
                    quill.root.dataset.placeholder =''
                } else {
                    quill.root.dataset.placeholder
                     = "  متن خود را اینجا بنویسید...";
                }
        });
        }
    }, [quill]);
    useEffect(()=>{
        if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
        debounceTimerRef.current=setTimeout(() => {
            fetchSuggestions(apiContent);
        }, 500);
    },[apiContent]);
    useEffect(() => {
        if (quill) {
            quill.root.setAttribute('spellcheck', 'false');  // Directly disabling spellcheck
        }
    }, [quill]);
    useEffect(() => {
        if (!quill) return;
        isFormattingRef.current=true;
        
        quill.formatText(0, quill.getLength(), 'redUnderline', false);
        quill.root.querySelectorAll('.protected-red-underline').forEach(el => {
            el.outerHTML = el.innerHTML;  // Remove the span but keep the text
        });

        suggestions.forEach((suggestion , index) => {
            quill.formatText(suggestion.start, suggestion.end-suggestion.start+1, 'redUnderline', String(index));
            
        });
        quill.updateContents([
            { retain: quill.getLength() }, // Retain all content
            { insert: '\u200B' }, // Insert zero-width space
        ], 'silent');
    
        quill.deleteText(quill.getLength() - 1, 1, 'silent');
        quill.update('silent');
        quill.root.style.display = 'none';  
        quill.root.offsetHeight;  // Force a reflow by accessing the height
        quill.root.style.display = '';

        isFormattingRef.current=false;

        const handleClick = (event) => {
            const clickedElement = event.target.closest('.protected-red-underline');
            if (clickedElement) {
                const clickedIndex = clickedElement.getAttribute('data-suggestion-index');
                setExpandedIndex(Number(clickedIndex));
                if (!isOpen) {
                    setIsOpen(!isOpen);
                }
            }
        };
        quill.root.addEventListener('click', handleClick);
        return () => {
            quill.root.removeEventListener('click', handleClick);
        };
    }, [suggestions, quill]);
    useEffect(()=>{
        setExpandedIndex(-1);
    },[suggestions])
    useEffect(()=>{
        if(!quill) return;

        quill.root.querySelectorAll('.protected-red-underline').forEach(el => {
            el.classList.remove('active');
        });

        const activeElement = quill.root.querySelector(
            `.protected-red-underline[data-suggestion-index="${expandedIndex}"]`
        );
        if (activeElement) {
            activeElement.classList.add('active');
        }
    },[expandedIndex])

    const fetchSuggestions = async (text) => {
        if (!text||text.length===0) return;
        try {
            const response = await axios.post("http://127.0.0.1:9000/group3/optimize/", {
             text
            });
            setSuggestions(response.data.suggestions);
            quill.update('silent');
        } catch (error) {
            console.error("Error fetching suggestions:", error);
        }
    };
        
    if ((suggestions.length === 0|| content.length===0) && quill ){
        quill.formatText(0, quill.getLength(), 'redUnderline', false);
        quill.root.querySelectorAll('.protected-red-underline').forEach(el => {
            el.outerHTML = el.innerHTML;  // Remove the span but keep the text
        });
    }

        
    return (
        <div className="text-editor">
            <div ref={quillRef} className="editor-textarea"></div>
        </div>
    );
};

export default TextEditor;
