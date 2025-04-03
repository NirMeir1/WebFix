import React from 'react';

const Header: React.FC = () => (
  <header className="flex justify-between items-center px-8 py-4">
    <img src="/logo.png" alt="Logo" className="w-32 h-auto" />
    <nav className="flex gap-4">
      <img src="/icons/share.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/facebook.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/instagram.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/phone.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/email.svg" className="w-8 h-8 cursor-pointer" />
    </nav>
  </header>
);

export default Header;