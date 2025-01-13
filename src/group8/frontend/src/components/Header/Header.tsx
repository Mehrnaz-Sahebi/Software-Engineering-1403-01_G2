import React, { useEffect } from "react";
import Logo from "../Logo/Logo";
import { Link, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import clsx from "clsx";
import DarkModeSwitch from "../inputs/DarkModeSwitch/DarkModeSwitch";
import { IoMdLogIn } from "react-icons/io";
import { MdLanguage } from "react-icons/md";
import DropdownMenu from "../inputs/DropdownMenu/DropdownMenu";

const Header = () => {
  const location = useLocation();
  const { t, i18n } = useTranslation();

  const languages = [
    {
      label: "فارسی",
      onClick: () => {
        i18n.changeLanguage("fa");
      },
    },
    {
      label: "English",
      onClick: () => {
        i18n.changeLanguage("en");
      },
    },
    {
      label: "Español",
      onClick: () => {
        i18n.changeLanguage("es");
      },
    },
    {
      label: "Français",
      onClick: () => {
        i18n.changeLanguage("fr");
      },
    },
    {
      label: "العربية",
      onClick: () => {
        i18n.changeLanguage("ar");
      },
    },
    {
      label: "中文",
      onClick: () => {
        i18n.changeLanguage("zh");
      },
    },
  ];

  return (
    <div className="flex justify-around items-center border-b-2 shadow-sm dark:shadow-2xl dark:border-teal">
      <Logo className="w-16 py-2 h-auto dark:invert" />

      <nav className="flex gap-8 text-black dark:text-white">
        <Link
          className={clsx({
            ["hover:text-coral transition-all"]: location.pathname !== "/",
            ["border-b-2 border-teal text-teal font-bold"]:
              location.pathname === "/",
          })}
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
          to={"/about"}
        >
          {t("aboutUs")}
        </Link>
        <Link
          className={clsx({
            ["hover:text-coral transition-all"]:
              location.pathname !== "/contact",
            ["border-b-2 border-teal text-teal font-bold"]:
              location.pathname === "/contact",
          })}
          to={"/contact"}
        >
          {t("contactUs")}
        </Link>
      </nav>

      {/* <Link
        to={"/signup"}
        className="p-2 text-2xl text-center bg-teal text-white rounded-full hover:bg-coral transition-all"
      >
        <IoMdLogIn />
      </Link>
      <DarkModeSwitch /> */}

      <div className="flex gap-2">
        <Link
          to={"/signup"}
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
