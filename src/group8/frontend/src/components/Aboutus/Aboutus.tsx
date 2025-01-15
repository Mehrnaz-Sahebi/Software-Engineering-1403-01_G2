import React from "react";
import image from "../../assets/group.jpg";
import me from "../../assets/me.jpg";
// import dance from "../../assets/dance.mp4";
import { useUtils } from "../../hooks/useUtils";
import { useTranslation } from "react-i18next";

const Aboutus = () => {
  const { t } = useTranslation();
  const { digitsToHindi } = useUtils();

  return (
    <div className="flex flex-col items-center p-4 md:px-16 dark:text-white gap-10 md:py-4">
      <div
        className="w-full flex flex-col md:flex-row-reverse justify-between items-center md:items-start gap-4 text-justify"
        dir="rtl"
      >
        <img src={image} alt="group" className="w-1/2 rounded-md" />
        <div className="flex flex-col items-center w-full md:w-1/2 gap-4">
          <h1 className="text-center text-3xl font-bold">
            {digitsToHindi(t("groupName"))}
          </h1>
          <p className="text-xl">{t("aboutus.summary")}</p>
        </div>
      </div>
      {[...Array(7).keys()].map((_, index) => (
        <div key={index} className="flex flex-col items-center w-full gap-4">
          <h2 className="text-2xl font-bold">
            {t(`aboutus.khan${index + 1}.title`)}
          </h2>
          <p className="text-xl w-full md:w-3/4 leading-8">
            {t(`aboutus.khan${index + 1}.text`)}
          </p>
          {index === 3 && <img src={me} className="w-1/4 rounded-2xl"></img>}
        </div>
      ))}
      {/* <video src={video} autoPlay loop className="w-1/4 rounded-2xl"></video> */}
    </div>
  );
};

export default Aboutus;
