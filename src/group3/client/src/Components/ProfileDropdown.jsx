import React, { useState, useEffect,useRef } from "react";
import { FaUser , FaMoon} from "react-icons/fa";
import '../styles/ProfileDropdown.css';

const ProfileDropdown = ({toggleDarkMode,isDarkMode}) => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsDropdownOpen(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    return (
        <div className="profile-container" ref={dropdownRef}>
            <button type="button" onClick={toggleDropdown} className="profile-button">
                <FaUser />
            </button>

            {isDropdownOpen && (
                <div className="dropdown-menu">
                <div className="dark-mode-toggle">
                    
                    <FaMoon className="toggle-icon" />
                    <span>Dark mode</span>

                    <label className="switch">
                        <input
                            type="checkbox"
                            checked={isDarkMode}
                            onChange={toggleDarkMode}
                        />
                        <span className="slider round"></span>
                    </label>
                </div>
            </div>
            )}
        </div>
    );
};

export default ProfileDropdown;
