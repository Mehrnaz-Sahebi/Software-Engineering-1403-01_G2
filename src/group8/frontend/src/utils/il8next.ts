import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./locales/en";
import fa from "./locales/fa";
import zh from "./locales/zh";
import ar from "./locales/ar";
import fr from "./locales/fr";
import es from "./locales/es";
import ko from "./locales/ko";
import de from "./locales/de";
import hi from "./locales/hi";
import ru from "./locales/ru";
import it from "./locales/it";

i18n.use(initReactI18next).init({
  resources: {
    fa: {
      translation: fa,
    },
    en: {
      translation: en,
    },
    es: {
      translation: es,
    },
    fr: {
      translation: fr,
    },
    ar: {
      translation: ar,
    },
    zh: {
      translation: zh,
    },
    ko: {
      translation: ko,
    },
    it: {
      translation: it,
    },
    de: {
      translation: de,
    },
    hi: {
      translation: hi,
    },
    ru: {
      translation: ru,
    },
  },
  lng: "fa",
  fallbackLng: "fa",
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
