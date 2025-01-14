import React, { useState, useEffect, useRef } from 'react';

const AutocompleteInterface = () => {
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [selectedTheme, setSelectedTheme] = useState('default');
  const [fontSize, setFontSize] = useState('medium');
  const [savedTexts, setSavedTexts] = useState([]);
  const [customWords, setCustomWords] = useState([]);
  const textareaRef = useRef(null);

  const themes = {
    default: {
      primary: '#007bff',
      bg: isDarkMode ? '#1a1a1a' : '#f8f9fa',
      secondary: isDarkMode ? '#333' : '#fff',
      text: isDarkMode ? '#fff' : '#000',
    },
    nature: {
      primary: '#28a745',
      bg: isDarkMode ? '#155724' : '#e8f5e9',
      secondary: isDarkMode ? '#1b5e20' : '#fff',
      text: isDarkMode ? '#fff' : '#155724',
    },
    ocean: {
      primary: '#17a2b8',
      bg: isDarkMode ? '#0c5460' : '#e0f7fa',
      secondary: isDarkMode ? '#0d47a1' : '#fff',
      text: isDarkMode ? '#fff' : '#004085',
    },
  };

  const fontSizes = {
    small: '14px',
    medium: '16px',
    large: '18px',
  };

  useEffect(() => {
    const handleKeyboard = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        handleSaveText();
      }
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        setShowSettings(!showSettings);
      }
      if (e.key === 'Tab' && suggestions.length > 0) {
        e.preventDefault();
        handleSuggestionClick(suggestions[0]);
      }
    };

    document.addEventListener('keydown', handleKeyboard);
    return () => document.removeEventListener('keydown', handleKeyboard);
  }, [suggestions, showSettings]);

  const fetchSuggestions = async (text) => {
    try {
      const response = await fetch(`/api/suggestions?q=${encodeURIComponent(text)}`);
      const data = await response.json();
      setSuggestions(data);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      setSuggestions([]);
    }
  };

  useEffect(() => {
    if (input.trim()) {
      const lastChar = input.slice(-1);
      if (lastChar === ' ') {
        const lastWord = input.trim().split(' ').pop();
        fetchSuggestions(lastWord);
      } else {
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
    }
  }, [input]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
    setIsTyping(true);
    setTimeout(() => setIsTyping(false), 1000);
  };

  const handleSuggestionClick = (suggestion) => {
    const words = input.trim().split(' ');
    words.pop();
    words.push(suggestion);
    setInput(words.join(' ') + ' ');
    textareaRef.current.focus();
  };

  const handleSaveText = () => {
    if (input.trim()) {
      const newSavedText = {
        id: Date.now(),
        text: input,
        date: new Date().toLocaleDateString('fa-IR'),
      };
      setSavedTexts([newSavedText, ...savedTexts]);
      alert('متن با موفقیت ذخیره شد!');
    }
  };

  const handleLoadText = (text) => {
    setInput(text);
    textareaRef.current.focus();
  };

  const exportSavedTexts = () => {
    const data = JSON.stringify(savedTexts);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'saved-texts.json';
    a.click();
  };

  const addCustomWord = (word) => {
    setCustomWords([...customWords, word]);
    alert('کلمه جدید با موفقیت اضافه شد!');
  };

  const currentTheme = themes[selectedTheme];

  return (
    <div style={{ minHeight: '100vh', padding: '20px', backgroundColor: currentTheme.bg, color: currentTheme.text }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold' }}>Autocomplete Interface</h1>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={() => setShowSettings(!showSettings)}
              style={{ padding: '10px', borderRadius: '50%', backgroundColor: currentTheme.secondary }}
              title="تنظیمات (Ctrl + /)"
            >
              ⚙️
            </button>
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              style={{ padding: '10px', borderRadius: '50%', backgroundColor: currentTheme.secondary }}
            >
              {isDarkMode ? '☀️' : '🌙'}
            </button>
          </div>
        </div>

        {showSettings && (
          <div style={{ marginBottom: '20px', padding: '20px', borderRadius: '10px', backgroundColor: currentTheme.secondary }}>
            <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '10px' }}>settings</h2>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
              <div>
                <h3 style={{ fontWeight: 'bold' }}>theme</h3>
                <div style={{ display: 'flex', gap: '10px' }}>
                  {Object.keys(themes).map((theme) => (
                    <button
                      key={theme}
                      onClick={() => setSelectedTheme(theme)}
                      style={{
                        padding: '10px',
                        borderRadius: '5px',
                        backgroundColor: selectedTheme === theme ? currentTheme.primary : '#ddd',
                        color: selectedTheme === theme ? '#fff' : '#000',
                      }}
                    >
                      {theme}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <h3 style={{ fontWeight: 'bold' }}>text size </h3>
                <div style={{ display: 'flex', gap: '10px' }}>
                  {Object.keys(fontSizes).map((size) => (
                    <button
                      key={size}
                      onClick={() => setFontSize(size)}
                      style={{
                        padding: '10px',
                        borderRadius: '5px',
                        backgroundColor: fontSize === size ? currentTheme.primary : '#ddd',
                        color: fontSize === size ? '#fff' : '#000',
                      }}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            <div>
              <h3 style={{ fontWeight: 'bold', marginBottom: '10px' }}> shortcuts </h3>
              <ul>
                <li>Ctrl + S: save </li>
                <li>Ctrl + /: show /hide settings </li>
                <li>Tab: choose first recom </li>
              </ul>
            </div>
            <div>
              <h3 style={{ fontWeight: 'bold', marginBottom: '10px' }}>add new word:</h3>
              <input
                type="text"
                placeholder="new word "
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    addCustomWord(e.target.value);
                    e.target.value = '';
                  }
                }}
                style={{
                  padding: '10px',
                  borderRadius: '5px',
                  border: '1px solid #ccc',
                  width: '100%',
                }}
              />
            </div>
          </div>
        )}

        <div style={{ position: 'relative', padding: '20px', borderRadius: '10px', backgroundColor: currentTheme.secondary }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>⌨️</span>
              <span style={{ fontSize: '14px' }}> start typing here  ...</span>
            </div>
            <button
              onClick={handleSaveText}
              style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '10px', borderRadius: '5px', backgroundColor: currentTheme.primary, color: '#fff' }}
              title="save  (Ctrl + S)"
            >
              💾 save
            </button>
          </div>

          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            style={{
              width: '100%',
              height: '100px',
              padding: '10px',
              borderRadius: '5px',
              fontSize: fontSizes[fontSize],
              backgroundColor: currentTheme.secondary,
              color: currentTheme.text,
              border: '1px solid #ccc',
            }}
            dir="rtl"
            placeholder="typing here"
          />

          {isTyping && (
            <div style={{ position: 'absolute', bottom: '10px', left: '10px', display: 'flex', gap: '5px' }}>
              <div style={{ width: '5px', height: '5px', backgroundColor: currentTheme.primary, borderRadius: '50%', animation: 'bounce 1s infinite' }} />
              <div style={{ width: '5px', height: '5px', backgroundColor: currentTheme.primary, borderRadius: '50%', animation: 'bounce 1s infinite', animationDelay: '0.1s' }} />
              <div style={{ width: '5px', height: '5px', backgroundColor: currentTheme.primary, borderRadius: '50%', animation: 'bounce 1s infinite', animationDelay: '0.2s' }} />
            </div>
          )}
        </div>

        {suggestions.length > 0 && (
          <div style={{ marginTop: '20px', padding: '20px', borderRadius: '10px', backgroundColor: currentTheme.secondary }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
              <span>🔍</span>
              <span style={{ fontSize: '14px' }}>پیشنهادات:</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                  style={{
                    padding: '10px',
                    borderRadius: '20px',
                    fontSize: '14px',
                    backgroundColor: isDarkMode ? '#444' : '#f1f1f1',
                    color: currentTheme.text,
                    border: '1px solid #ccc',
                  }}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {savedTexts.length > 0 && (
          <div style={{ marginTop: '30px', padding: '20px', borderRadius: '10px', backgroundColor: currentTheme.secondary }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ fontSize: '20px', fontWeight: 'bold' }}>saved texts</h2>
              <button
                onClick={exportSavedTexts}
                style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '10px', borderRadius: '5px', backgroundColor: currentTheme.primary, color: '#fff' }}
              >
                ⬇️ خروجی
              </button>
            </div>
            <div>
              {savedTexts.map((item) => (
                <div
                  key={item.id}
                  style={{ marginBottom: '10px', padding: '10px', borderRadius: '5px', backgroundColor: isDarkMode ? '#555' : '#f8f8f8', border: '1px solid #ccc' }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '5px' }}>
                    <span style={{ fontSize: '12px' }}>{item.date}</span>
                    <button
                      onClick={() => handleLoadText(item.text)}
                      style={{ fontSize: '12px', color: currentTheme.primary, textDecoration: 'underline' }}
                    >
                      بازیابی
                    </button>
                  </div>
                  <p style={{ fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AutocompleteInterface;