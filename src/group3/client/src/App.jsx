import { useState, useContext } from 'react'
import Header from './Components/Header'
import TextEditor from './Components/TextEditor'
import TextResult from './Components/TextResult'
import "./styles/App.css"
import { ContentProvider } from './contexts/ContentContext'

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [expandedIndex, setExpandedIndex] = useState();
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleSidebar = () => {
      setIsOpen(!isOpen);
  };
  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.body.classList.toggle('dark-mode');
  };

  return (
    <>
      <Header toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode}></Header>
      <div className={`button-container ${isOpen ? 'shifted' : ''}`}>
        <button className={`toggle-button`} onClick={toggleSidebar}>
                {isOpen ? '>>' : '<<'}
      </button>
      {isOpen && <h2 className='error'>خطاها و پیشنهادات</h2>}
      </div>
      <ContentProvider>
        <div className='container'>
          <TextEditor expandedIndex={expandedIndex} setExpandedIndex={setExpandedIndex} isOpen={isOpen} setIsOpen={setIsOpen} className="editor-container"></TextEditor>
          <TextResult toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} isOpen={isOpen} expandedIndex={expandedIndex} setExpandedIndex={setExpandedIndex} className='result-container'></TextResult>
        </div> 
      </ContentProvider>
    </>
  )
}

export default App
