/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        coral: "#F05D5E",
        teal: "#0F7173", 
        tealSecondary: "#305252", 
        lightGray: "#E7ECEF",
        littleLightGray: "#18191f",
        tooltip: "#484a5c",
        darkGray: "#272932", 
        darkGrayGlass: "#16171cb0", 
        tan: "#D8A47F",
      },
    },
  },
  plugins: [],
};
