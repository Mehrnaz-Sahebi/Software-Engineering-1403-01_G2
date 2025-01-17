import React from "react";
import "../styles/Header.css";
import logo from "../assets/image.png";
import ProfileDropdown from "./ProfileDropdown";

const Header = ({toggleDarkMode, isDarkMode}) => {
  return (
    <header className="header">
      <div className="header-left">
        <img 
          src={logo}
          alt="SSP Union" 
          className="logo" 
        />
      </div>

      <div className="header-center">
        <h1 className="title">بهینه ساز متن</h1>
      </div>

      <div className="header-right">
        <ProfileDropdown toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode}></ProfileDropdown>

      </div>
    </header>
  );
};

export default Header;
