import { useTranslation } from "react-i18next";

export const useUtils = () => {
  const { i18n } = useTranslation();

  const digitsToHindi = (text: string) => {
    if (i18n.language !== "fa") return text;
    return text.replace(/\d/g, (d: string) => "۰۱۲۳۴۵۶۷۸۹"[Number(d)]);
  };

  return { digitsToHindi };
};
