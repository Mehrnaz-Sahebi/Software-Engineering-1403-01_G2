import React, { useState } from "react";
import Logo from "../Logo/Logo";
import { Link, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import clsx from "clsx";
import DarkModeSwitch from "../inputs/DarkModeSwitch/DarkModeSwitch";
import { IoMdLogIn } from "react-icons/io";
import { MdLanguage, MdMenu, MdClose } from "react-icons/md";
import DropdownMenu from "../inputs/DropdownMenu/DropdownMenu";

const Header = () => {
  const location = useLocation();
  const { t, i18n } = useTranslation();
  const [menuOpen, setMenuOpen] = useState(false);

  const languages = [
    {
      label: "🇮🇷 فارسی (ایران)", // Persian (Iran)
      onClick: () => {
        i18n.changeLanguage("fa");
      },
    },
    {
      label: "🇺🇸 English (United States)", // English (United States)
      onClick: () => {
        i18n.changeLanguage("en");
      },
    },
    {
      label: "🇪🇸 Español (España)", // Spanish (Spain)
      onClick: () => {
        i18n.changeLanguage("es");
      },
    },
    {
      label: "🇫🇷 Français (France)", // French (France)
      onClick: () => {
        i18n.changeLanguage("fr");
      },
    },
    {
      label: "🇸🇦 العربية (السعودية)", // Arabic (Saudi Arabia)
      onClick: () => {
        i18n.changeLanguage("ar");
      },
    },
    {
      label: "🇨🇳 中文 (中国)", // Chinese (China)
      onClick: () => {
        i18n.changeLanguage("zh");
      },
    },
    {
      label: "🇰🇷 한국어 (대한민국)", // Korean (South Korea)
      onClick: () => {
        i18n.changeLanguage("ko");
      },
    },
    {
      label: "🇮🇹 Italiano (Italia)", // Italian (Italy)
      onClick: () => {
        i18n.changeLanguage("it");
      },
    },
    {
      label: "🇩🇪 Deutsch (Deutschland)", // German (Germany)
      onClick: () => {
        i18n.changeLanguage("de");
      },
    },
    {
      label: "🇮🇳 हिन्दी (भारत)", // Hindi (India)
      onClick: () => {
        i18n.changeLanguage("hi");
      },
    },
    {
      label: "🇷🇺 Русский (Россия)", // Russian (Russia)
      onClick: () => {
        i18n.changeLanguage("ru");
      },
    },
  ];

  return (
    <div className="flex justify-between items-center border-b-2 shadow-sm dark:shadow-2xl dark:border-teal md:px-40">
      <Logo className="w-16 py-2 h-auto dark:invert" />

      <button
        className="text-2xl md:hidden text-teal"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        {menuOpen ? <MdClose /> : <MdMenu />}
      </button>

      <nav
        className={clsx(
          "flex-col md:flex-row md:flex gap-8 text-black dark:text-white",
          {
            ["flex absolute top-0 right-0 left-0 bottom-0 justify-center items-center bg-darkGray z-50"]:
              menuOpen,
            ["hidden md:flex"]: !menuOpen,
          }
        )}
      >
        <p
          className={clsx("cursor-pointer", { ["hidden"]: !menuOpen })}
          onClick={() => setMenuOpen(false)}
        >
          x
        </p>
        <Link
          className={clsx({
            ["hover:text-coral transition-all"]: location.pathname !== "/",
            ["border-b-2 border-teal text-teal font-bold"]:
              location.pathname === "/",
          })}
          draggable={false}
          to={"/"}
        >
          {t("home")}
        </Link>
        <Link
          className={clsx({
            ["hover:text-coral transition-all"]: location.pathname !== "/about",
            ["border-b-2 border-teal text-teal font-bold"]:
              location.pathname === "/about",
          })}
          draggable={false}
          to={"/about"}
        >
          {t("aboutUs")}
        </Link>
        {/* <Link
          className={clsx({
            ["hover:text-coral transition-all"]:
              location.pathname !== "/contact",
            ["border-b-2 border-teal text-teal font-bold"]:
              location.pathname === "/contact",
          })}
          draggable={false}
          to={"/contact"}
        >
          {t("contactUs")}
        </Link> */}
      </nav>

      <div className="flex gap-2">
        <Link
          to={"/signup"}
          draggable={false}
          className="text-2xl text-teal red text-center c-teal rounded-full hover:bg-teal hover:text-white transition-all duration-250 ease-in-out"
        >
          <IoMdLogIn />
        </Link>
        <DarkModeSwitch />
        <DropdownMenu items={languages}>
          <MdLanguage />
        </DropdownMenu>
      </div>
    </div>
  );
};

export default Header;
