import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Header.css';

function Header() {
  const [isDark, setIsDark] = useState(() => {
    const stored = localStorage.getItem('cloudmosaic-theme');
    if (stored === 'dark' || stored === 'light') return stored === 'dark';
    // Fallback to prefers-color-scheme or body class
    return document.body.classList.contains('dark-theme') || 
           window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 100);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    document.body.classList.toggle('dark-theme', isDark);
    localStorage.setItem('cloudmosaic-theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  return (
    <header className={`header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="logo-left">
        <Link to="/">
          <img src={process.env.PUBLIC_URL + "/images/logo.png"} alt="CloudMosaic Logo" className="logo" />
        </Link>
      </div>

      <nav className="nav">
        <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>Home</Link>
        <Link to="/about" className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}>About</Link>
        <Link to="/services" className={`nav-link ${location.pathname === '/services' ? 'active' : ''}`}>Services</Link>
        <Link to="/products" className={`nav-link ${location.pathname === '/products' ? 'active' : ''}`}>Products</Link>
        <Link to="/projects" className={`nav-link ${location.pathname === '/projects' ? 'active' : ''}`}>Projects</Link>
        {/* <Link to="/testimonials" className={`nav-link ${location.pathname === '/testimonials' ? 'active' : ''}`}>Testimonials</Link> */}
        <Link to="/team" className={`nav-link ${location.pathname === '/team' ? 'active' : ''}`}>Team</Link>
        <Link to="/careers" className={`nav-link ${location.pathname === '/careers' ? 'active' : ''}`}>Careers</Link>
        <Link to="/contact" className={`nav-link ${location.pathname === '/contact' ? 'active' : ''}`}>Contact</Link>
        
        <button 
          className="theme-toggle" 
          onClick={() => setIsDark(!isDark)}
          aria-label={`Switch to ${isDark ? 'light' : 'dark'} theme`}
          aria-pressed={isDark}
        >
          <div className="toggle-track">
            <div className="toggle-thumb" aria-hidden="true"></div>
            <i className="fas fa-sun toggle-sun" aria-hidden="true"></i>
            <i className="fas fa-moon toggle-moon" aria-hidden="true"></i>
          </div>
          <span className="toggle-text">{isDark ? 'Light' : 'Dark'}</span>
        </button>
      </nav>

      <div className="logo-right">
        <img src={process.env.PUBLIC_URL + "/images/wmb-logo.png"} alt="WMB Logo" className="logo" />
      </div>
    </header>
  );
}

export default Header;