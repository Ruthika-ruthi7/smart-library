import React from 'react';
import './ProfessionalNavbar.css';

const ProfessionalNavbar = ({ employee, onLogout }) => {
  return (
    <nav className="professional-navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="brand-logo">📚</div>
          <div className="brand-text">
            <h1>Smart Library</h1>
            <span>Enterprise Management System</span>
          </div>
        </div>

        <div className="navbar-center">
          <div className="breadcrumb">
            <span className="breadcrumb-item">Dashboard</span>
            {employee.role === 'admin' && (
              <span className="breadcrumb-separator">›</span>
            )}
            {employee.role === 'admin' && (
              <span className="breadcrumb-item active">Administration</span>
            )}
          </div>
        </div>

        <div className="navbar-user">
          <div className="user-profile">
            <div className="user-avatar">
              {employee.name.charAt(0).toUpperCase()}
            </div>
            <div className="user-info">
              <div className="user-name">{employee.name}</div>
              <div className="user-role">
                {employee.role === 'admin' ? 'Administrator' : employee.department}
              </div>
            </div>
          </div>
          
          <div className="navbar-actions">
            <button className="btn btn-outline" onClick={onLogout}>
              <span className="logout-icon">⏻</span>
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default ProfessionalNavbar;
