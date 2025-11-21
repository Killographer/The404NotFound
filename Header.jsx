import React from 'react';

const Header = ({ title, subtitle }) => {
  return (
    <header className="glass glass-shadow rounded-3xl px-8 py-10 text-center mb-8 animate-fade-in">
      <h1 className="text-4xl md:text-5xl font-bold text-white mb-3 drop-shadow-lg tracking-tight">
        {title}
      </h1>
      {subtitle && (
        <p className="text-lg md:text-xl text-white/90 font-normal">
          {subtitle}
        </p>
      )}
    </header>
  );
};

export default Header;

