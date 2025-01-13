import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./locales/en";
import fa from "./locales/fa";
import zh from "./locales/zh";
import ar from "./locales/ar";
import fr from "./locales/fr";
import es from "./locales/es";

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
  },
  lng: "fa",
  fallbackLng: "fa",
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
