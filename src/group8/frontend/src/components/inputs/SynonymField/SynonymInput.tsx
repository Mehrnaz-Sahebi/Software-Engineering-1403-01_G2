import React, {
  ChangeEvent,
  Fragment,
  UIEvent,
  useEffect,
  useRef,
  useState,
} from "react";
import { debounceTime, Subject } from "rxjs";
import useApi from "../../../hooks/useApi";
import { Tooltip } from "react-tooltip";
import ReactDOMServer from "react-dom/server";
import SynonymSuggestion from "./SynonymSuggestion";

interface Props {
  value?: string;
  onChange?: (value: string) => void;
  defaultValue?: string;
  className?: string;
  onApplyWithTags: (
    word: string,
    tags: string[],
    cb: (tag?: string) => void
  ) => void;
}

const SynonymInput = ({
  value,
  onChange,
  defaultValue = "",
  className = "",
  onApplyWithTags,
  ...props
}: Props) => {
  const keyWordsRef = useRef<HTMLDivElement>(null);
  const [innerValue, setInnerValue] = useState(defaultValue);
  const [scrollValue, setScrollValue] = useState(0);
  const [selectedWord, setSelectedWord] = useState("");
  const [keys, setKeys] = useState<{ [key: string]: string[] }>({});
  const [ignored, setIgnored] = useState<string[]>([]);
  const { response, error, loading, fetchData } = useApi<{
    results: {
      token: string;
      meaning: string[];
    }[];
  }>({
    url: "/api/group8/submit-text/",
    method: "post", // Use POST to send a body
  });

  const inputValue = value !== undefined ? value : innerValue;

  const changeHandler = (e: ChangeEvent<HTMLTextAreaElement>) => {
    if (onChange) onChange(e.target.value);
    setInnerValue(e.target.value);
    inputSubject.current.next(e.target.value);
  };
  const scrollHandler = (e: UIEvent<HTMLTextAreaElement>) => {
    setScrollValue(e.currentTarget.scrollLeft);
  };

  useEffect(() => {
    if (keyWordsRef.current) {
      keyWordsRef.current.scrollLeft = scrollValue;
    }
  }, [scrollValue]);

  const inputSubject = useRef(new Subject());

  useEffect(() => {
    const subscription = inputSubject.current
      .pipe(debounceTime(500))
      .subscribe((debouncedValue) => {
        fetchData({ text: debouncedValue });
      });

    return () => subscription.unsubscribe();
  }, []);

  useEffect(() => {
    const newKeys = { ...keys };
    if (!response?.results) return;
    response?.results.forEach((data) => {
      newKeys[data.token] = data.meaning;
    });
    setKeys(newKeys);
  }, [response, error, loading]);

  return (
    <div className={`relative ${className}`} dir="auto">
      <div
        ref={keyWordsRef}
        className="absolute top-0 left-0 bottom-0 right-0 overflow-x-scroll whitespace-pre-wrap m-2 p-2 dark:text-white"
      >
        {inputValue.split("\n").map((line, lineIndex) => (
          <div key={lineIndex}>
            {line.split(/\s+/).map((word, wordIndex) => {
              if (
                keys[word] !== undefined &&
                keys[word].length > 0 &&
                !ignored.includes(word)
              )
                return (
                  <Fragment key={word + wordIndex}>
                    <span
                      data-tooltip-id="warning"
                      className="relative inline-block z-10 text-white cursor-pointer"
                      onClick={() => {
                        setSelectedWord(word);
                        console.log(`Clicked on: ${word}`);
                      }}
                    >
                      {word}
                      <span className="absolute inset-0 -z-10 rounded bg-red-600/20" />
                    </span>
                    &nbsp;
                  </Fragment>
                );
              else
                return (
                  <Fragment key={word + wordIndex}>
                    {word}
                    &nbsp;
                  </Fragment>
                );
            })}
          </div>
        ))}
      </div>
      <textarea
        {...props}
        className="w-full h-full relative outline-none resize-none bg-transparent text-transparent caret-black dark:caret-white p-2 placeholder-gray-500 whitespace-pre-wrap"
        value={inputValue}
        onChange={changeHandler}
        onScroll={scrollHandler}
        spellCheck={false}
      />
      <Tooltip
        id="warning"
        events={["click"]}
        className="!bg-tooltip cursor-pointer z-50"
      >
        <SynonymSuggestion
          suggestion={keys[selectedWord]?.join(", ")}
          word={selectedWord}
          onApply={() => {
            if (keys[selectedWord].length > 1) {
              onApplyWithTags(
                selectedWord,
                keys[selectedWord],
                (tag?: string) => {
                  if (!tag) {
                    setIgnored([...ignored, selectedWord]);
                    return;
                  }
                  const newValue = inputValue.replace(selectedWord, tag);
                  if (onChange) onChange(newValue);
                  setInnerValue(newValue);
                  setSelectedWord("");
                }
              );
            } else {
              const newValue = inputValue.replace(
                selectedWord,
                keys[selectedWord][0]
              );
              if (onChange) onChange(newValue);
              setInnerValue(newValue);
              setSelectedWord("");
            }
          }}
          onDiscard={() => setIgnored([...ignored, selectedWord])}
        />
      </Tooltip>
    </div>
  );
};

export default SynonymInput;
