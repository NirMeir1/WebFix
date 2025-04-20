import React from 'react';
import Header from '../Header';
import Footer from '../Footer';

interface PageLayoutProps {
  children: React.ReactNode;
}

const PageLayout: React.FC<PageLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header />
      <div className="flex justify-center mt-4 mb-2">
        <img src="/logo.png" alt="Logo" className="w-[300px] h-auto" />
      </div>
      <main className="flex-grow">{children}</main>
      <Footer />
    </div>
  );
};

export default PageLayout;