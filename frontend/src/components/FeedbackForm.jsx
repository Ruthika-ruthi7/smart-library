import React, { useState } from 'react';
import './FeedbackForm.css';

const FeedbackForm = ({ employee, onClose }) => {
  const [feedbackType, setFeedbackType] = useState('general');
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');
  const [bookDetails, setBookDetails] = useState({
    title: '',
    author: '',
    genre: '',
    priority: 'medium'
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim()) {
      alert('Please enter your feedback message');
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch('http://localhost:5000/submit-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          employee_name: employee.name,
          employee_id: employee.employee_id,
          type: feedbackType,
          title: title,
          message: message,
          book_details: feedbackType === 'book_request' ? bookDetails : {}
        }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        alert('Feedback submitted successfully! Admin will review and respond soon.');
        // Reset form
        setTitle('');
        setMessage('');
        setBookDetails({ title: '', author: '', genre: '', priority: 'medium' });
        setFeedbackType('general');
        if (onClose) onClose();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="feedback-overlay">
      <div className="feedback-form">
        <div className="feedback-header">
          <h2>💬 Submit Feedback</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Feedback Type:</label>
            <select 
              value={feedbackType} 
              onChange={(e) => setFeedbackType(e.target.value)}
              className="form-select"
            >
              <option value="general">General Feedback</option>
              <option value="book_request">Book Purchase Request</option>
              <option value="complaint">Complaint</option>
              <option value="suggestion">Suggestion</option>
            </select>
          </div>

          <div className="form-group">
            <label>Title (Optional):</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Brief title for your feedback"
              className="form-input"
            />
          </div>

          {feedbackType === 'book_request' && (
            <div className="book-request-section">
              <h3>📚 Book Request Details</h3>
              
              <div className="form-group">
                <label>Book Title: *</label>
                <input
                  type="text"
                  value={bookDetails.title}
                  onChange={(e) => setBookDetails({...bookDetails, title: e.target.value})}
                  placeholder="Enter book title"
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label>Author:</label>
                <input
                  type="text"
                  value={bookDetails.author}
                  onChange={(e) => setBookDetails({...bookDetails, author: e.target.value})}
                  placeholder="Enter author name"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Genre:</label>
                <select 
                  value={bookDetails.genre} 
                  onChange={(e) => setBookDetails({...bookDetails, genre: e.target.value})}
                  className="form-select"
                >
                  <option value="">Select genre</option>
                  <option value="Fiction">Fiction</option>
                  <option value="Non-Fiction">Non-Fiction</option>
                  <option value="Science">Science</option>
                  <option value="Technology">Technology</option>
                  <option value="Business">Business</option>
                  <option value="Self Help">Self Help</option>
                  <option value="Biography">Biography</option>
                  <option value="History">History</option>
                  <option value="Cooking">Cooking</option>
                  <option value="Health">Health</option>
                  <option value="Finance">Finance</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label>Priority:</label>
                <select 
                  value={bookDetails.priority} 
                  onChange={(e) => setBookDetails({...bookDetails, priority: e.target.value})}
                  className="form-select"
                >
                  <option value="low">Low - Nice to have</option>
                  <option value="medium">Medium - Would be useful</option>
                  <option value="high">High - Really needed</option>
                </select>
              </div>
            </div>
          )}

          <div className="form-group">
            <label>
              {feedbackType === 'book_request' ? 'Why do you need this book?' : 'Your Message:'} *
            </label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={
                feedbackType === 'book_request' 
                  ? "Explain why this book would be valuable for the library and how it would help you or other employees..."
                  : "Share your feedback, suggestions, or concerns..."
              }
              className="form-textarea"
              rows="5"
              required
            />
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              onClick={onClose}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={submitting}
            >
              {submitting ? 'Submitting...' : 'Submit Feedback'}
            </button>
          </div>
        </form>

        <div className="feedback-info">
          <h4>📋 Feedback Guidelines:</h4>
          <ul>
            <li><strong>General Feedback:</strong> Share your thoughts about the library system</li>
            <li><strong>Book Requests:</strong> Suggest books you'd like to see in our library</li>
            <li><strong>Complaints:</strong> Report any issues or problems</li>
            <li><strong>Suggestions:</strong> Ideas for improving the library</li>
          </ul>
          <p><em>All feedback is reviewed by the admin team and you'll receive a response soon!</em></p>
        </div>
      </div>
    </div>
  );
};

export default FeedbackForm;
