"use client"
import React, { useState } from 'react';

const ChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState('Switch');

  const items: string[] = ['A', 'B', 'C', 'D'];

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
          <div className="text-token-text-secondary">
            {selectedValue} <span className="text-token-text-secondary"></span>
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
          <div className="absolute top-0 right-full mt-0 mr-2 flex space-x-2 bg-white border border-gray-300 rounded-lg shadow-lg z-50 p-1">
            {items.map((item) => (
              <button
                key={item}
                onClick={() => handleSelect(item)}
                className="group flex cursor-pointer items-center gap-1 rounded-lg py-1.5 px-3 text-lg font-semibold hover:bg-token-main-surface-secondary text-token-text-secondary overflow-hidden whitespace-nowrap"
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
