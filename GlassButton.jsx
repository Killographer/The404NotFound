import React from 'react';

const GlassButton = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  className = '',
  disabled = false,
  type = 'button',
  ...props 
}) => {
  const baseClasses = `
    relative px-6 py-4 rounded-xl font-bold text-white
    transition-all duration-300 ease-out
    overflow-hidden
    disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none
    ${className}
  `;

  const variantClasses = {
    primary: `
      glass-strong border-white/40
      shadow-xl glass-shadow
      hover:bg-white/35 hover:scale-105 hover:shadow-2xl
      active:scale-100
    `,
    secondary: `
      glass border-white/30
      shadow-lg
      hover:bg-white/25 hover:scale-105 hover:shadow-xl
      active:scale-100
    `,
    ghost: `
      glass-soft border-white/20
      hover:bg-white/20 hover:scale-105
      active:scale-100
    `,
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]}`}
      {...props}
    >
      <span className="relative z-10">{children}</span>
      <span 
        className="absolute inset-0 bg-white/20 rounded-xl opacity-0 hover:opacity-100 transition-opacity duration-300"
        aria-hidden="true"
      />
    </button>
  );
};

export default GlassButton;

