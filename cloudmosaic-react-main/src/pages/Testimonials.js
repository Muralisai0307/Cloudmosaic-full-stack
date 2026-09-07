import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Autoplay } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { apiService } from '../services/api';
import { useNotification } from '../context/NotificationContext';
import { validateEmail } from '../utils/helpers';
import '../styles/Testimonials.css';

const defaultTestimonials = [
  {
    id: 1,
    name: 'John Anderson',
    service: 'Cloud Migration',
    text: 'CloudMosaic transformed our infrastructure completely. Their cloud migration strategy was flawless, and we\'ve seen a 40% reduction in operational costs. The team\'s expertise in AWS is unmatched.',
    rating: 5,
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    date: 'March 2024'
  },
  {
    id: 2,
    name: 'Sarah Wilson',
    service: 'HR Consulting',
    text: 'The HR consulting team helped us build a high-performance culture. They redesigned our entire recruitment process and we\'ve hired 30+ top talent in just 3 months. Outstanding work!',
    rating: 5,
    image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80',
    date: 'February 2024'
  },
  {
    id: 3,
    name: 'Michael Chang',
    service: 'Security & Compliance',
    text: 'Achieved SOC2 compliance in record time thanks to CloudMosaic. Their automated compliance framework saved us months of work and hundreds of thousands in potential audit costs.',
    rating: 5,
    image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80',
    date: 'January 2024'
  }
];

function Testimonials() {
  const { success, error, warning } = useNotification();
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);

  // Form states
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [service, setService] = useState('');
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true,
      offset: 100,
      easing: 'ease-in-out'
    });
  }, []);

  const [testimonialsList, setTestimonialsList] = useState(defaultTestimonials);
  const [isLoadingTestimonials, setIsLoadingTestimonials] = useState(false);

  useEffect(() => {
    const fetchTestimonials = async () => {
      try {
        const response = await apiService.getTestimonials();
        if (response && response.success && Array.isArray(response.data) && response.data.length > 0) {
          const mapped = response.data.map(test => ({
            ...test,
            text: test.comment,
            image: test.image_url || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(test.name) + '&background=random',
            date: new Date(test.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
          }));
          setTestimonialsList(mapped);
        }
      } catch (err) {
        console.log('Using default testimonials:', err.message);
      }
    };
    fetchTestimonials();
  }, []);

  const handleReviewSubmit = async (e) => {
    e.preventDefault();

    if (!name.trim()) {
      warning('Please enter your name.');
      return;
    }
    if (!email.trim() || !validateEmail(email)) {
      warning('Please enter a valid email address.');
      return;
    }
    if (!service) {
      warning('Please select the service used.');
      return;
    }
    if (rating === 0) {
      warning('Please select a rating of 1 to 5 stars.');
      return;
    }
    if (!comment.trim() || comment.trim().length < 5) {
      warning('Please enter a review comment of at least 5 characters.');
      return;
    }

    setIsSubmitting(true);
    try {
      await apiService.submitReviewForm({ name, email, service, rating, comment });
      success('Thank you for your review! It has been submitted.');
      
      // Reset states
      setName('');
      setEmail('');
      setService('');
      setComment('');
      setRating(0);
      setHoverRating(0);
    } catch (err) {
      if (err.errors && Object.keys(err.errors).length > 0) {
        const errorMsgs = Object.values(err.errors).flat().join(' ');
        error(`Submission failed: ${errorMsgs}`);
      } else {
        error(err.message || 'Failed to submit review. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Helmet>
        <title>Client Testimonials - CloudMosaic</title>
        <meta name="description" content="Read feedback and reviews from clients who upgraded their cloud and enterprise setups with CloudMosaic." />
        <link rel="canonical" href="https://cloudmosaic.ai/testimonials" />
      </Helmet>
      <Header />
      
      <section className="page-header">
        <div className="container">
          <h1 data-aos="fade-up">Client Stories</h1>
          <p data-aos="fade-up" data-aos-delay="100">Real feedback from real clients</p>
        </div>
      </section>

      <section className="testimonials-carousel-section">
        <div className="container">
          {isLoadingTestimonials ? (
            <div className="text-center" style={{ padding: '3rem 0' }}>
              <i className="fas fa-spinner fa-pulse" style={{ fontSize: '2rem', color: 'var(--accent-color)' }} aria-hidden="true"></i>
              <p style={{ marginTop: '1rem' }}>Loading testimonials...</p>
            </div>
          ) : (
            <Swiper
              modules={[Navigation, Pagination, Autoplay]}
              spaceBetween={30}
              slidesPerView={1}
              navigation
              pagination={{ clickable: true }}
              autoplay={{ delay: 5000, disableOnInteraction: false }}
              breakpoints={{
                768: { slidesPerView: 2 },
                1024: { slidesPerView: 3 }
              }}
              className="testimonials-swiper"
            >
              {testimonialsList.map((testimonial) => (
                <SwiperSlide key={testimonial.id}>
                  <div className="testimonial-card">
                    <div className="testimonial-rating">
                      {[...Array(5)].map((_, i) => (
                        <i key={i} className={`${i < testimonial.rating ? 'fas' : 'far'} fa-star`} aria-hidden="true"></i>
                      ))}
                    </div>
                    <p className="testimonial-text">"{testimonial.text}"</p>
                    <div className="testimonial-author">
                      <img src={testimonial.image} alt={testimonial.name} className="author-image" loading="lazy" />
                      <div className="author-info">
                        <h4>{testimonial.name}</h4>
                        <p>{testimonial.title}</p>
                        <small className="review-date"><i className="far fa-calendar-alt" aria-hidden="true"></i> {testimonial.date}</small>
                      </div>
                    </div>
                  </div>
                </SwiperSlide>
              ))}
            </Swiper>
          )}
        </div>
      </section>

      <section className="review-form-section">
        <div className="container">
          <div className="review-form-container" data-aos="fade-up">
            <h3>Leave Your Review</h3>
            <form className="review-form" onSubmit={handleReviewSubmit}>
              <div className="form-row">
                <div className="form-group">
                  <input 
                    type="text" 
                    name="name" 
                    placeholder="Your Name" 
                    required 
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    aria-label="Your Name"
                  />
                  <i className="fas fa-user" aria-hidden="true"></i>
                </div>
                <div className="form-group">
                  <input 
                    type="email" 
                    name="email" 
                    placeholder="Your Email" 
                    required 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    aria-label="Your Email"
                  />
                  <i className="fas fa-envelope" aria-hidden="true"></i>
                </div>
              </div>
              <div className="form-group">
                <select 
                  name="service" 
                  required
                  value={service}
                  onChange={(e) => setService(e.target.value)}
                  aria-label="Select Service Used"
                >
                  <option value="">Select Service Used</option>
                  <option value="Cloud Services">Cloud Services</option>
                  <option value="HR Consulting">HR Consulting</option>
                  <option value="Web Development">Web Development</option>
                  <option value="Security">Security</option>
                </select>
                <i className="fas fa-tag" aria-hidden="true"></i>
              </div>
              <div className="rating-input">
                <span>Your Rating:</span>
                <div className="stars">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button 
                      type="button"
                      key={star}
                      className="star-btn"
                      onClick={() => setRating(star)}
                      onMouseEnter={() => setHoverRating(star)}
                      onMouseLeave={() => setHoverRating(0)}
                      aria-label={`Rate ${star} star${star > 1 ? 's' : ''}`}
                      style={{ 
                        background: 'none', 
                        border: 'none', 
                        padding: '0 2px',
                        cursor: 'pointer', 
                        color: 'var(--rating-color)',
                        fontSize: '1.25rem',
                        outline: 'none'
                      }}
                    >
                      <i className={`${star <= (hoverRating || rating) ? 'fas' : 'far'} fa-star`} aria-hidden="true"></i>
                    </button>
                  ))}
                </div>
              </div>
              <div className="form-group">
                <textarea 
                  name="comment" 
                  placeholder="Your Review" 
                  rows="4" 
                  required
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  aria-label="Your Review Comment"
                ></textarea>
                <i className="fas fa-comment" aria-hidden="true"></i>
              </div>
              <button type="submit" className="submit-review" disabled={isSubmitting}>
                {isSubmitting ? (
                  <>Submitting... <i className="fas fa-spinner fa-pulse" aria-hidden="true"></i></>
                ) : (
                  <>Submit Review <i className="fas fa-paper-plane" aria-hidden="true"></i></>
                )}
              </button>
            </form>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}

export default Testimonials;
