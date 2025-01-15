import React from "react";
import image from "../../assets/404.png";

const NotFound = () => {
  return (
    <div className="overflow-hidden flex justify-center">
      <img src={image} className="h-[80vh]" />
    </div>
  );
};

export default NotFound;
