import React from "react";
import { Trans, useTranslation } from "react-i18next";

interface Props {
  word: string;
  suggestion: string;
  onApply: () => void;
  onDiscard: () => void;
}

const SynonymSuggestion = ({ word, suggestion, onApply, onDiscard }: Props) => {
  const { t } = useTranslation();
  return (
    <div className="flex flex-col gap-4 select-text z-[99] max-w-[400px] sm:max-w-screen-sm md:max-w-screen-md lg:max-w-screen-lg  xl:max-w-screen-xl  2xl:max-w-screen-2xl">
      <p className="w-max text-wrap">
        <Trans
          i18nKey="tooltip.suggestion"
          tOptions={{ word, word2: suggestion }}
        />
      </p>
      <div className="flex gap-2 text-white">
        <button
          className="bg-teal px-2 py-1 cursor-pointer !pointer-events-auto"
          onClick={onApply}
        >
          {t("tooltip.apply")}
        </button>
        <button
          className="bg-coral px-2 py-1 cursor-pointer !pointer-events-auto"
          onClick={onDiscard}
        >
          {t("tooltip.discard")}
        </button>
      </div>
    </div>
  );
};

export default SynonymSuggestion;
