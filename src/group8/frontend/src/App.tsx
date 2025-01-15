import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Outlet } from "react-router-dom";

function App() {
  const { i18n } = useTranslation();

  useEffect(() => {
    const updateDir = () => {
      const direction =
        i18n.language === "fa" || i18n.language === "ar" ? "rtl" : "ltr";
      document.documentElement.dir = direction;
    };

    updateDir();

    i18n.on("languageChanged", updateDir);

    return () => {
      i18n.off("languageChanged", updateDir);
    };
  }, [i18n]);

  return (
    <div className="dark:bg-darkGray min-h-screen transition-all select-none">
      <Outlet />
    </div>
  );
}

export default App;
