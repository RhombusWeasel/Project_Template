import React from 'react';

const SiteContext = React.createContext();

export const SiteProvider = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = React.useState(false);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <SiteContext.Provider value={{ isDarkMode, toggleDarkMode }}>
      {children}
    </SiteContext.Provider>
  );
};

export default SiteContext;