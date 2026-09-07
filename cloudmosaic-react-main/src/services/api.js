const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class ApiError extends Error {
  constructor(status, message, errors = {}) {
    super(message);
    this.status = status;
    this.errors = errors;
    this.name = 'ApiError';
  }
}

const handleResponse = async (response) => {
  let result;
  try {
    result = await response.json();
  } catch (e) {
    if (response.status === 401) throw new ApiError(401, 'Authentication required.');
    if (response.status === 403) throw new ApiError(403, 'You do not have permission to perform this action.');
    if (response.status === 404) throw new ApiError(404, 'The requested resource was not found.');
    if (response.status === 405) throw new ApiError(405, 'This action is not allowed.');
    if (response.status === 429) throw new ApiError(429, 'Too many requests. Please try again later.');
    if (response.status >= 500) throw new ApiError(response.status, 'Something went wrong on the server. Please try again later.');
    throw new ApiError(response.status, 'Unable to connect to the server. Please try again.');
  }

  if (!response.ok) {
    let safeMessage = result.message || 'An error occurred.';
    let errors = result.errors || {};

    if (safeMessage.toLowerCase().includes('traceback') || safeMessage.toLowerCase().includes('django')) {
        safeMessage = 'Something went wrong on the server. Please try again later.';
        errors = {};
    }

    if (response.status === 400) throw new ApiError(400, safeMessage, errors);
    if (response.status === 401) throw new ApiError(401, 'Authentication required.', errors);
    if (response.status === 403) throw new ApiError(403, 'You do not have permission to perform this action.', errors);
    if (response.status === 404) throw new ApiError(404, 'The requested resource was not found.', errors);
    if (response.status === 405) throw new ApiError(405, 'This action is not allowed.', errors);
    if (response.status === 429) throw new ApiError(429, 'Too many requests. Please try again later.', errors);
    if (response.status >= 500) throw new ApiError(response.status, 'Something went wrong on the server. Please try again later.', errors);
    
    throw new ApiError(response.status, safeMessage, errors);
  }
  return result;
};

const apiPost = async (endpoint, data, isMultipart = false) => {
  const options = {
    method: 'POST',
    headers: {}
  };
  
  if (isMultipart) {
    options.body = data;
    // Do not set Content-Type for multipart; browser handles boundary
  } else {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    return await handleResponse(response);
  } catch (err) {
    if (err instanceof ApiError) throw err;
    throw new ApiError(0, 'Unable to connect to the server. Please try again.');
  }
};

const apiGet = async (endpoint) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    return await handleResponse(response);
  } catch (err) {
    if (err instanceof ApiError) throw err;
    throw new ApiError(0, 'Unable to connect to the server. Please try again.');
  }
};

export const apiService = {
  submitContactForm: (data) => apiPost('/contact/', data),
  submitScheduleForm: (data) => apiPost('/meetings/', data),
  submitJobApplication: (formData) => apiPost('/careers/jobs/apply/', formData, true),
  subscribeNewsletter: (email) => apiPost('/newsletter/subscribe/', { email }),
  submitReviewForm: (data) => apiPost('/testimonials/', data),
  getJobs: () => apiGet('/careers/jobs/'),
  getServices: () => apiGet('/services/'),
  getTestimonials: () => apiGet('/testimonials/'),
};
