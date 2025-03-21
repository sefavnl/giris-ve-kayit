import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout, loading } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    navigate('/login');
    return null;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome to Your Dashboard</h1>
        <button onClick={handleLogout} className="btn-logout">
          Logout
        </button>
      </div>
      
      <div className="user-profile">
        <h2>Your Profile</h2>
        <div className="profile-details">
          <div className="profile-item">
            <span className="label">Name:</span>
            <span className="value">{user.first_name} {user.last_name}</span>
          </div>
          <div className="profile-item">
            <span className="label">Email:</span>
            <span className="value">{user.email}</span>
          </div>
        </div>
      </div>
      
      <div className="dashboard-content">
        <h2>Dashboard Content</h2>
        <p>
          This is a protected dashboard page that can only be accessed by authenticated users.
          You can add your application features here.
        </p>
      </div>
    </div>
  );
};

export default Dashboard; 