import React from 'react';

const GlassCard = ({ 
  children, 
  className = '', 
  padding = 'default',
  hover = false,
  ...props 
}) => {
  const paddingClasses = {
    none: 'p-0',
    small: 'p-4',
    default: 'p-6',
    large: 'p-8',
  };

  const baseClasses = `
    rounded-xl glass glass-shadow
    transition-all duration-300
    ${paddingClasses[padding]}
    ${hover ? 'hover:bg-white/20 hover:shadow-2xl hover:-translate-y-1' : ''}
    ${className}
  `;

  return (
    <div className={baseClasses} {...props}>
      {children}
    </div>
  );
};

export default GlassCard;

