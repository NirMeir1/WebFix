import React from 'react';

const Footer: React.FC = () => (
  <footer className="mt-auto flex justify-between items-center bg-gradient-to-r from-pink-500 to-yellow-500 p-6 text-white">
    <img src="/logo.png" alt="Logo" className="w-32 h-auto" />
    <div className="flex flex-col items-center">
      <span className="font-semibold">Aviv Meirman</span>
      <span>Aviv@bottomline.com</span>
    </div>
    <div className="border-l border-gray-300 h-16"></div>
    <div className="flex flex-col items-center">
      <span className="font-semibold">Nir Meir</span>
      <span>Nir@bottomline.com</span>
    </div>
    <div className="border-l border-gray-300 h-16"></div>
    <div className="flex flex-col items-center">
      <span className="font-semibold">Michal</span>
      <span>Michal@bottomline.com</span>
    </div>
    <nav className="flex gap-4">
      <img src="/icons/facebook.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/instagram.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/phone.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/email.svg" className="w-8 h-8 cursor-pointer" />
      <img src="/icons/share.svg" className="w-8 h-8 cursor-pointer" />
    </nav>
  </footer>
);

export default Footer;