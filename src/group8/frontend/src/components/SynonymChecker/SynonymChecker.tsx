import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import SynonymField from "../inputs/SynonymField/SynonymField";

const SynonymChecker = () => {
  const { t } = useTranslation();

  return (
    <div className="dark:text-white w-full flex justify-center items-center h-100 pt-20 flex-col gap-5">
      <h1 className="text-3xl font-bold">{t("synonym_title")}</h1>
      <h2>{t("synonym_desc")}</h2>
      <SynonymField />
    </div>
  );
};

export default SynonymChecker;
