import React, { useState } from 'react';
import './ProfessionalLogin.css';

const ProfessionalLogin = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    employee_id: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Attempting login with:', formData);

      // Try to connect to backend
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(formData),
        mode: 'cors',
      });

      console.log('Response status:', response.status);

      const data = await response.json();
      console.log('Response data:', data);

      if (response.ok && data.status === 'success') {
        console.log('Login successful, calling onLogin');
        onLogin(data.employee);
      } else {
        // Handle authentication errors
        if (response.status === 401) {
          setError(data.message || 'Invalid credentials. Please check your name and Employee ID.');
        } else if (response.status === 400) {
          setError(data.message || 'Please fill in all fields.');
        } else {
          setError(data.message || `Server error: ${response.status}`);
        }
      }
    } catch (error) {
      console.error('Login error:', error);

      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        setError('❌ Cannot connect to backend server. Please start the backend first:\n\n1. Open Command Prompt\n2. Go to: c:\\smart library\\backend\n3. Run: python app_with_admin_features.py');
      } else if (error.message.includes('CORS')) {
        setError('CORS error. Backend CORS configuration issue.');
      } else if (error.message.includes('NetworkError')) {
        setError('Network error. Check if backend is running on port 5000.');
      } else {
        setError(`Connection failed: ${error.message}\n\nPlease ensure backend is running.`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  return (
    <div className="professional-login">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <div className="company-logo">
              <div className="logo-icon">📚</div>
              <h1>Smart Library</h1>
            </div>
            <p className="login-subtitle">Enterprise Library Management System</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="name" className="form-label">
                Employee Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="form-input"
                placeholder="Enter your full name"
                required
                autoComplete="name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="employee_id" className="form-label">
                Employee ID
              </label>
              <input
                type="text"
                id="employee_id"
                name="employee_id"
                value={formData.employee_id}
                onChange={handleChange}
                className="form-input"
                placeholder="Enter your Employee ID"
                required
                autoComplete="username"
              />
            </div>

            {error && (
              <div className="error-message">
                <div className="error-icon">⚠️</div>
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary btn-login"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  Signing In...
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <span className="login-arrow">→</span>
                </>
              )}
            </button>
          </form>

          <div className="login-footer">
            <div className="login-help">
              <h4>Login Instructions</h4>
              <p>Enter your registered employee name and Employee ID to access the system.</p>
              <p><strong>Note:</strong> Use your exact name and Employee ID as registered in the employee database.</p>
            </div>
          </div>
        </div>


      </div>
    </div>
  );
};

export default ProfessionalLogin;
