import { ReactNode, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface Props {
  items: { label: string; onClick: () => void }[];
  children: ReactNode;
}

const DropdownMenu = ({ items, children }: Props) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen((prev) => !prev);

  const menuVariants = {
    hidden: { opacity: 0, y: -10 },
    visible: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -10 },
  };

  return (
    <div className="relative inline-block text-left">
      <button
        onClick={toggleMenu}
        className="px-4 py-2 text-sm font-medium text-white focus:outline-none"
      >
        {children}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial="hidden"
            animate="visible"
            exit="exit"
            variants={menuVariants}
            transition={{ duration: 0.2 }}
            className="absolute -right-40 md:right-0 z-10 mt-2 w-48 origin-top-right bg-white dark:bg-darkGrayGlass rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
          >
            <div className="py-1">
              {items.map((item, index) => (
                <button
                  key={index}
                  className={`block w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-white hover:bg-gray-900`}
                  onClick={() => {
                    item.onClick();
                    setIsOpen(false);
                  }}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default DropdownMenu;
