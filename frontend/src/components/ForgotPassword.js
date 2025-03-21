import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { authService } from '../services/api';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resetToken, setResetToken] = useState('');

  const validateForm = () => {
    if (!email) {
      setError('Email is required');
      return false;
    }
    
    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      return false;
    }
    
    setError('');
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    setMessage('');
    setError('');
    
    try {
      const response = await authService.requestPasswordReset(email);
      setMessage('If your email is registered, you will receive a password reset link.');
      
      // In a real app, we would not show this token to the user
      // It would be sent via email with a link
      // For demo purposes, we'll display it here
      if (response.token) {
        setResetToken(response.token);
      }
    } catch (err) {
      setError('Something went wrong. Please try again later.');
      console.error('Password reset request error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form-container">
        <h2>Forgot Password</h2>
        
        {message && (
          <div className="success-message">
            {message}
            
            {resetToken && (
              <div className="reset-token-info">
                <p>For demo purposes, here is your reset token:</p>
                <code>{resetToken}</code>
                <p>Use this token to reset your password at:</p>
                <Link to={`/reset-password?token=${resetToken}`}>
                  Reset Password Page
                </Link>
              </div>
            )}
          </div>
        )}
        
        {error && <div className="error-message">{error}</div>}
        
        {!message && (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            
            <button 
              type="submit" 
              className="submit-button" 
              disabled={isLoading}
            >
              {isLoading ? 'Sending...' : 'Reset Password'}
            </button>
            
            <div className="auth-links">
              <Link to="/login">Back to Login</Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default ForgotPassword; 