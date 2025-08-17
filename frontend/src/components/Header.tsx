import React from 'react';

const Header: React.FC = () => (
  <header className="w-full bg-gradient-to-r from-pink-400 to-yellow-300 px-6 py-3 flex justify-end items-center space-x-4">
  <img src="/icons/share.svg" className="w-6 h-6 cursor-pointer" />
  <img src="/icons/facebook.svg" className="w-6 h-6 cursor-pointer" />
  <img src="/icons/instagram.svg" className="w-6 h-6 cursor-pointer" />
  <img src="/icons/phone.svg" className="w-6 h-6 cursor-pointer" />
  <img src="/icons/email.svg" className="w-6 h-6 cursor-pointer" />
  </header>
);

export default Header;
