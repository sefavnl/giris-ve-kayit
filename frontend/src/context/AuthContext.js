import React, { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/api';

// Create the auth context
const AuthContext = createContext();

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load user on initial render if token exists
  useEffect(() => {
    const loadUser = async () => {
      try {
        if (authService.isLoggedIn()) {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        }
      } catch (err) {
        console.error('Failed to load user:', err);
        authService.logout();
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  // Register a new user
  const register = async (userData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authService.register(userData);
      return response;
    } catch (err) {
      setError(err.detail || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Login a user
  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      await authService.login(email, password);
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (err) {
      setError(err.detail || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout the user
  const logout = () => {
    authService.logout();
    setUser(null);
  };

  // Auth context value
  const value = {
    user,
    loading,
    error,
    register,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext; 