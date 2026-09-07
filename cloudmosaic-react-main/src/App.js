import React, { useEffect, lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import AOS from 'aos';
import 'aos/dist/aos.css';
import './styles/global.css';

// Import Context Providers
import { NotificationProvider } from './context/NotificationContext';

// Import Error Boundary
import ErrorBoundary from './components/ErrorBoundary';

// Import Common Components
import Loading from './components/common/Loading';
import ContactHub from './components/ContactHub';

// Lazy load pages for performance optimization
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Services = lazy(() => import('./pages/Services'));
const Products = lazy(() => import('./pages/Products'));
const Projects = lazy(() => import('./pages/Projects'));
// const Testimonials = lazy(() => import('./pages/Testimonials'));
const Team = lazy(() => import('./pages/Team'));
const Careers = lazy(() => import('./pages/Careers'));
const Contact = lazy(() => import('./pages/Contact'));
const ErpComparison = lazy(() => import('./pages/ErpComparison'));
const Privacy = lazy(() => import('./pages/Privacy'));
const Terms = lazy(() => import('./pages/Terms'));
const NotFound = lazy(() => import('./pages/NotFound'));

// Scroll restoration component
function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
    setTimeout(() => {
      AOS.refresh();
    }, 100);
  }, [pathname]);

  return null;
}

function App() {
  useEffect(() => {
    AOS.init({
      duration: 400,
      once: true,
      offset: 50,
      easing: 'ease-in-out'
    });
  }, []);

  return (
    <ErrorBoundary>
      <HelmetProvider>
        <NotificationProvider>
          <Router basename={process.env.PUBLIC_URL}>
            <ScrollToTop />
            <Suspense fallback={<Loading fullPage={true} />}>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/services" element={<Services />} />
                <Route path="/products" element={<Products />} />
                <Route path="/projects" element={<Projects />} />
                {/* <Route path="/testimonials" element={<Testimonials />} /> */}
                <Route path="/team" element={<Team />} />
                <Route path="/careers" element={<Careers />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/erp-comparison" element={<ErpComparison />} />
                <Route path="/privacy" element={<Privacy />} />
                <Route path="/terms" element={<Terms />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </Suspense>
            <ContactHub />
          </Router>
        </NotificationProvider>
      </HelmetProvider>
    </ErrorBoundary>
  );
}

export default App;