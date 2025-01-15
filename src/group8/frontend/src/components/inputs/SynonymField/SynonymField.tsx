import React, { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { Tooltip } from "react-tooltip";
import { debounceTime, Subject } from "rxjs";
import SynonymSuggestion from "./SynonymSuggestion";
import ReactDOMServer from "react-dom/server";
import SynonymInput from "./SynonymInput";
import { useNavigate } from "react-router-dom";
import SynonymTag from "./SynonymTag";

const SynonymField = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [tags, setTags] = useState<string[] | undefined>();
  const [selectedWord, setSelectedWord] = useState("");
  const [selectTags, setSelectTags] =
    useState<(tag?: string) => void | undefined>();
  const [selectedSynonym, setSelectedSynonym] = useState<string | undefined>();

  const onApplyWithTags = (
    word: string,
    tags: string[],
    onSelect: (tag?: string) => void
  ) => {
    setSelectedWord(word);
    setTags(tags);
    setSelectTags(() => onSelect);
  };

  const doneWithTags = () => {
    setTags(undefined);
    setSelectTags(undefined);
    setSelectedSynonym(undefined);
  };

  return (
    <div className="flex flex-col md:flex-row w-full justify-center items-center md:items-stretch">
      <div className="bg-gray-100 dark:bg-littleLightGray w-full md:w-1/4 rounded-t-xl md:rounded-tl-none md:rounded-s-xl select-none p-4 flex flex-col items-center text-center border-2 border-gray-400 border-b-0 md:border-2 md:border-e-0">
        {tags === undefined ? (
          <>
            <h2>{t("systemReady")}</h2>
            <h1 className="mt-2">{t("startNow")}</h1>
            <div className="flex flex-col mt-4 text-start gap-2">
              <h3>
                <strong>{t("step1.title")}: </strong>
                <span>{t("step1.description")}</span>
              </h3>
              <h3>
                <strong>{t("step2.title")}: </strong>
                <span>{t("step2.description")}</span>
              </h3>
              <h3>
                <strong>{t("step3.title")}: </strong>
                <span>{t("step3.description")}</span>
              </h3>
            </div>
            <button
              className="mt-4 md:mt-auto w-full py-2 bg-teal text-lg rounded-md hover:bg-tealSecondary transition-all text-white"
              onClick={() => navigate("/login")}
            >
              {t("signUpOrSignIn")}
            </button>
          </>
        ) : (
          <>
            <h1 className="text-start">
              {t("tags.selectTag", { word: selectedWord })}
            </h1>
            <div className="mt-4 flex flex-wrap gap-2">
              {tags.map((tag) => (
                <SynonymTag
                  onClick={() => setSelectedSynonym(tag)}
                  active={selectedSynonym === tag}
                >
                  {tag}
                </SynonymTag>
              ))}
            </div>
            <div className="mt-auto flex justify-between w-full flex-wrap">
              <button
                className="bg-teal disabled:bg-gray-400 disabled:cursor-not-allowed text-white py-2 rounded-md w-full mb-2 transition-all"
                disabled={!selectedSynonym}
                onClick={() => {
                  if (!selectedSynonym) return;
                  selectTags?.(selectedSynonym);
                  doneWithTags();
                }}
              >
                {t("tooltip.apply")}
              </button>
              <button
                className="bg-tan text-white py-2 w-[45%] rounded-md"
                onClick={() => {
                  doneWithTags();
                }}
              >
                {t("tags.cancel")}
              </button>
              <button
                className="bg-coral text-white py-2 w-[45%] rounded-md"
                onClick={() => {
                  selectTags?.(undefined);
                  doneWithTags();
                }}
              >
                {t("tooltip.discard")}
              </button>
            </div>
          </>
        )}
      </div>
      <div className="min-h-[400px] w-full md:w-1/2 dark:bg-darkGrayGlass p-2 rounded-b-xl md:rounded-none md:rounded-e-xl outline-none border-2 border-gray-400">
        <SynonymInput
          className="w-full h-full outline-none p-2 whitespace-pre-wrap"
          onApplyWithTags={onApplyWithTags}
        ></SynonymInput>
      </div>
    </div>
  );
};

export default SynonymField;
