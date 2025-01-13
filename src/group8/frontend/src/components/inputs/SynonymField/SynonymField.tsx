import React from "react";
import { useTranslation } from "react-i18next";

const SynonymField = () => {
  const { t } = useTranslation();

  return (
    <div className="flex w-full justify-center items-stretch">
      <div className="bg-gray-100 dark:bg-littleLightGray w-1/4 rounded-s-xl select-none p-4 flex flex-col items-center text-center border-2 border-gray-400 border-e-0">
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
        <button className="mt-auto w-full py-2 bg-teal text-lg rounded-md hover:bg-tealSecondary transition-all text-white">
          {t("signUpOrSignIn")}
        </button>
      </div>
      <div className="min-h-[400px] w-1/2 dark:bg-darkGrayGlass p-2 rounded-e-xl outline-none border-2 border-gray-400">
        <div
          className="w-full h-full outline-none p-2"
          dir="auto"
          contentEditable
        >
          test
        </div>
      </div>
    </div>
  );
};

export default SynonymField;
