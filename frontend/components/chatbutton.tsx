"use client"
import React, { createContext, useContext, useState, useEffect } from 'react';
import { IconGitHub } from './ui/icons';

type OnChangeCallback = (newValue: string) => void;

// 定义一个上下文来存储 selectedValue 和 setSelectedValue
const SelectedValueContext = createContext<{
  selectedValue: string;
  setSelectedValue: (value: string) => void;
} | undefined>(undefined);

// 提供一个 Provider 来包装你的应用
export const SelectedValueProvider = ({ children }: { children: React.ReactNode }) => {
  const [selectedValue, setSelectedValue] = useState<string>('ChainMind');

  return (
    <SelectedValueContext.Provider value={{ selectedValue, setSelectedValue }}>
      {children}
    </SelectedValueContext.Provider>
  );
};

// 自定义 Hook 来使用 selectedValue
export const useSelectedValue = (onChange?: OnChangeCallback) => {
  const context = useContext(SelectedValueContext);
  if (!context) {
    throw new Error('useSelectedValue must be used within a SelectedValueProvider');
  }

  const { selectedValue, setSelectedValue } = context;

  useEffect(() => {
    if (onChange) {
      onChange(selectedValue);
    }
  }, [selectedValue, onChange]);

  return { selectedValue, setSelectedValue };
};


const ChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  // 使用共享状态，并传递 onChange 回调函数
  const { selectedValue, setSelectedValue } = useSelectedValue();

  const items: string[] = ['ChainMind', 'MetaAgent', 'NeoGraph', 'Video parser', 'Web parser', 'File parser'];

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleSelect = (value: string) => {
    setSelectedValue(value);
    setIsOpen(false);
  };

  return (
    <div className="relative flex items-center gap-0 overflow-visible">
      <div className="flex items-center">
        <button
          type="button"
          id="radix-:r42:"
          aria-haspopup="menu"
          aria-expanded={isOpen}
          data-state={isOpen ? 'open' : 'closed'}
          className="group flex cursor-pointer items-center gap-1 rounded-lg py-1.5 px-3 text-lg font-semibold hover:bg-token-main-surface-secondary text-token-text-secondary overflow-hidden whitespace-nowrap"
          onClick={toggleDropdown}
        >
          <div className="text-sm">
            {selectedValue} <span className="text-sm"></span>
          </div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
            className={`icon-md text-token-text-tertiary transition-transform ${isOpen ? "rotate-180" : ""}`}
          >
            <path
              fill="currentColor"
              fillRule="evenodd"
              d="M5.293 9.293a1 1 0 0 1 1.414 0L12 14.586l5.293-5.293a1 1 0 1 1 1.414 1.414l-6 6a1 1 0 0 1-1.414 0l-6-6a1 1 0 0 1 0-1.414"
              clipRule="evenodd"
            />
          </svg>
        </button>
        {isOpen && (
          <div className="absolute bottom-full right-70% mb-2 flex flex-col space-y-2 bg-background border-gray-300 rounded-lg shadow-lg z-50 p-1">
            {items.map((item) => (
              <button
                key={item}
                onClick={() => handleSelect(item)}
                className="group flex cursor-pointer items-center gap-1 rounded-lg py-1.5 px-3 font-semibold hover:bg-token-main-surface-secondary text-sm overflow-hidden whitespace-nowrap"
              >
                {item}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export { ChatButton };
