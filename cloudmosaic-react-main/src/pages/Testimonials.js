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

  const [testimonialsList, setTestimonialsList] = useState([]);
  const [isLoadingTestimonials, setIsLoadingTestimonials] = useState(true);
  const [testimonialsError, setTestimonialsError] = useState(null);

  useEffect(() => {
    const fetchTestimonials = async () => {
      try {
        const response = await apiService.getTestimonials();
        if (response.success && response.data) {
          const mapped = response.data.map(test => ({
            ...test,
            text: test.comment,
            image: test.image_url || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(test.name) + '&background=random',
            date: new Date(test.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
          }));
          setTestimonialsList(mapped);
        }
      } catch (err) {
        setTestimonialsError(err.message || 'Failed to load testimonials.');
        error(err.message || 'Failed to load testimonials.');
      } finally {
        setIsLoadingTestimonials(false);
      }
    };
    fetchTestimonials();
  }, [error]);

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
          ) : testimonialsError ? (
            <div className="text-center" style={{ padding: '3rem 0', color: 'var(--error-color)' }}>
              <i className="fas fa-exclamation-circle" style={{ fontSize: '2rem' }} aria-hidden="true"></i>
              <p style={{ marginTop: '1rem' }}>{testimonialsError}</p>
            </div>
          ) : testimonialsList.length === 0 ? (
            <div className="text-center" style={{ padding: '3rem 0' }}>
              <i className="fas fa-comment-slash" style={{ fontSize: '2rem', color: 'var(--text-secondary)' }} aria-hidden="true"></i>
              <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>No testimonials available at this time.</p>
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
