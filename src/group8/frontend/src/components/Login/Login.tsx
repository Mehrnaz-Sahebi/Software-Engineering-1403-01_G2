import React from "react";
import { useTranslation } from "react-i18next";

const Login = () => {
  const { t } = useTranslation();

  return (
    <div className="flex items-center justify-center min-h-screen bg-lightGray dark:bg-darkGray">
      <div className="bg-white dark:bg-darkGrayGlass dark:text-white p-8 rounded shadow-md w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">
          {t("login.title")}
        </h2>
        <form>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2 dark:text-white"
              htmlFor="username"
            >
              {t("login.username")}
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline dark:bg-darkGray dark:text-white border-teal"
              id="username"
              type="text"
              placeholder={t("login.username")}
            />
          </div>
          <div className="mb-6">
            <label
              className="block text-gray-700 text-sm font-bold mb-2 dark:text-white"
              htmlFor="password"
            >
              {t("login.pass")}
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline dark:bg-darkGray dark:text-white border-teal"
              id="password"
              type="password"
              placeholder="********"
            />
          </div>
          <div className="flex items-center justify-between">
            <button
              className="bg-teal hover:bg-tealSecondary text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
            >
              {t("login.title")}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
