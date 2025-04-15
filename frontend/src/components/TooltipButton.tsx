import React from 'react';

interface TooltipButtonProps {
  text: string;
  tooltip: string;
  onClick: () => void;
  disabled: boolean;
  isLoading: boolean;
  isActive: boolean;
  gradientClass: string;
}

const TooltipButton: React.FC<TooltipButtonProps> = ({
  text,
  tooltip,
  onClick,
  disabled,
  isLoading,
  isActive,
  gradientClass,
}) => (
  <div className="relative inline-block">
    <button
      type="submit"
      onClick={onClick}
      disabled={disabled}
      className={`relative w-64 py-3 px-4 rounded-full text-white font-bold text-lg shadow-lg text-center
        ${disabled ? (isActive ? 'bg-gray-400' : 'bg-gray-200 cursor-not-allowed') : gradientClass}`}
    >
      {isLoading && isActive ? 'Just A Sec...' : text}

      <div className="absolute right-3 top-1/2 -translate-y-1/2 group">
        <span className="w-5 h-5 flex items-center justify-center rounded-full bg-white text-gray-800 text-xs font-bold cursor-default hover:bg-gray-100">
          ?
        </span>
        <div className="absolute bottom-full right-0 mb-2 hidden group-hover:flex w-72 bg-white text-gray-800 text-sm p-3 rounded-lg shadow-xl border z-10">
          <span>{tooltip}</span>
        </div>
      </div>
    </button>
  </div>
);

export default TooltipButton;