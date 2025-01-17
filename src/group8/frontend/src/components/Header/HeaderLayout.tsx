import React, { ReactNode } from "react";
import Header from "./Header";
import { Outlet } from "react-router-dom";

const HeaderLayout = () => {
  return (
    <>
      <Header />
      <Outlet />
    </>
  );
};

export default HeaderLayout;
