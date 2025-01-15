import React, { ReactNode } from "react";

interface Props {
  children: ReactNode;
  active: boolean;
  onClick: () => void;
}

const SynonymTag = ({ children, active, onClick }: Props) => {
  return (
    <p
      className={`px-2 py-1 bg-darkGray rounded text-white cursor-pointer transition-all ease-in-out ${
        active && "bg-teal font-bold"
      }`}
      onClick={onClick}
    >
      {children}
    </p>
  );
};

export default SynonymTag;
