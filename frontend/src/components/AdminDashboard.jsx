import React, { useState, useEffect } from 'react';
import './AdminDashboard.css';

const AdminDashboard = ({ employee }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [analytics, setAnalytics] = useState(null);
  const [books, setBooks] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [purchaseRequests, setPurchaseRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newBook, setNewBook] = useState({
    title: '',
    author: '',
    genre: '',
    rack_no: '',
    book_no: ''
  });

  // Security check: Only allow access to authenticated admin users
  if (!employee || employee.role !== 'admin') {
    return (
      <div className="access-denied">
        <div className="access-denied-content">
          <h2>🔒 Access Denied</h2>
          <p>You don't have permission to access the admin dashboard.</p>
          <p>Only authorized administrators can view this page.</p>
        </div>
      </div>
    );
  }

  useEffect(() => {
    fetchAnalytics();
    fetchBooks();
    fetchFeedback();
    fetchPurchaseRequests();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('http://localhost:5000/admin/analytics');
      const data = await response.json();
      if (data.status === 'success') {
        setAnalytics(data.analytics);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const fetchBooks = async () => {
    try {
      const response = await fetch('http://localhost:5000/admin/books');
      const data = await response.json();
      if (data.status === 'success') {
        setBooks(data.books);
      }
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  const fetchFeedback = async () => {
    try {
      const response = await fetch('http://localhost:5000/feedback');
      const data = await response.json();
      if (data.status === 'success') {
        setFeedback(data.feedback);
      }
    } catch (error) {
      console.error('Error fetching feedback:', error);
    }
  };

  const fetchPurchaseRequests = async () => {
    try {
      const response = await fetch('http://localhost:5000/purchase-requests');
      const data = await response.json();
      if (data.status === 'success') {
        setPurchaseRequests(data.purchase_requests);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching purchase requests:', error);
      setLoading(false);
    }
  };

  const addBook = async () => {
    try {
      const response = await fetch('http://localhost:5000/admin/books', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newBook),
      });

      const data = await response.json();
      if (data.status === 'success') {
        alert('Book added successfully!');
        setNewBook({ title: '', author: '', genre: '', rack_no: '', book_no: '' });
        fetchBooks();
        fetchAnalytics();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error adding book:', error);
      alert('Failed to add book');
    }
  };

  const deleteBook = async (bookId) => {
    if (!confirm('Are you sure you want to delete this book?')) return;

    try {
      const response = await fetch(`http://localhost:5000/admin/books/${bookId}`, {
        method: 'DELETE',
      });

      const data = await response.json();
      if (data.status === 'success') {
        alert('Book deleted successfully!');
        fetchBooks();
        fetchAnalytics();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error deleting book:', error);
      alert('Failed to delete book');
    }
  };

  const respondToFeedback = async (feedbackId, response, status) => {
    try {
      const apiResponse = await fetch(`http://localhost:5000/feedback/${feedbackId}/respond`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          response: response,
          status: status
        }),
      });

      const data = await apiResponse.json();
      if (data.status === 'success') {
        alert('Response sent successfully!');
        fetchFeedback();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error responding to feedback:', error);
      alert('Failed to send response');
    }
  };

  const updatePurchaseRequest = async (requestId, status, addToLibrary = false) => {
    try {
      const response = await fetch(`http://localhost:5000/purchase-requests/${requestId}/update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          status: status,
          add_to_library: addToLibrary,
          admin_notes: `Request ${status} by admin`
        }),
      });

      const data = await response.json();
      if (data.status === 'success') {
        alert(`Purchase request ${status} successfully!`);
        fetchPurchaseRequests();
        if (addToLibrary) {
          fetchBooks();
        }
        fetchAnalytics();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error updating purchase request:', error);
      alert('Failed to update purchase request');
    }
  };

  if (loading) {
    return <div className="loading">Loading admin dashboard...</div>;
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>🔧 Admin Dashboard</h1>
        <div className="admin-info">
          <span>Welcome, {employee.name}</span>
        </div>
      </div>

      <div className="admin-tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`tab ${activeTab === 'books' ? 'active' : ''}`}
          onClick={() => setActiveTab('books')}
        >
          📚 Book Management
        </button>
        <button 
          className={`tab ${activeTab === 'feedback' ? 'active' : ''}`}
          onClick={() => setActiveTab('feedback')}
        >
          💬 Feedback ({feedback.filter(f => f.status === 'pending').length})
        </button>
        <button
          className={`tab ${activeTab === 'purchases' ? 'active' : ''}`}
          onClick={() => setActiveTab('purchases')}
        >
          🛒 Purchase Requests ({purchaseRequests.filter(r => r.status === 'pending').length})
        </button>
        <button
          className={`tab ${activeTab === 'employees' ? 'active' : ''}`}
          onClick={() => setActiveTab('employees')}
        >
          👥 Employee Tracking
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'overview' && analytics && (
          <div className="overview-section">
            <h2>📊 Library Overview</h2>
            
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Books</h3>
                <div className="stat-number">{analytics.book_statistics.total_books}</div>
              </div>
              <div className="stat-card">
                <h3>Available</h3>
                <div className="stat-number available">{analytics.book_statistics.available_books}</div>
              </div>
              <div className="stat-card">
                <h3>Taken</h3>
                <div className="stat-number taken">{analytics.book_statistics.taken_books}</div>
              </div>
              <div className="stat-card">
                <h3>Overdue</h3>
                <div className="stat-number overdue">{analytics.book_statistics.overdue_books}</div>
              </div>
              <div className="stat-card">
                <h3>Utilization Rate</h3>
                <div className="stat-number">{analytics.book_statistics.utilization_rate}%</div>
              </div>
              <div className="stat-card">
                <h3>Pending Feedback</h3>
                <div className="stat-number">{analytics.feedback_statistics.pending}</div>
              </div>
              <div className="stat-card">
                <h3>Employees with Books</h3>
                <div className="stat-number">{analytics.employee_statistics.employees_with_books}</div>
              </div>
              <div className="stat-card">
                <h3>Total Employees</h3>
                <div className="stat-number">{analytics.employee_statistics.total_employees}</div>
              </div>
            </div>

            <div className="overview-grid">
              <div className="overview-card">
                <h3>🔥 Most Popular Books</h3>
                <div className="popular-list">
                  {analytics.popular_books.slice(0, 5).map((book, index) => (
                    <div key={book.id} className="popular-item">
                      <span className="rank">#{index + 1}</span>
                      <span className="title">{book.title}</span>
                      <span className="count">{book.times_taken} times</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="overview-card">
                <h3>⚠️ Books Due for Renewal</h3>
                <div className="due-list">
                  {analytics.due_for_renewal.map(book => (
                    <div key={book.id} className="due-item">
                      <span className="title">{book.title}</span>
                      <span className="borrower">{book.taken_by}</span>
                      <span className="days">{book.days_remaining} days left</span>
                    </div>
                  ))}
                  {analytics.due_for_renewal.length === 0 && (
                    <p>No books due for renewal</p>
                  )}
                </div>
              </div>

              <div className="overview-card">
                <h3>📖 Books by Genre</h3>
                <div className="genre-list">
                  {Object.entries(analytics.genre_statistics).map(([genre, stats]) => (
                    <div key={genre} className="genre-item">
                      <span className="genre-name">{genre}</span>
                      <span className="genre-count">{stats.total} books</span>
                      <span className="genre-available">{stats.available} available</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="overview-card">
                <h3>👑 Top Borrowers</h3>
                <div className="borrower-list">
                  {analytics.employee_statistics.top_borrowers.slice(0, 5).map((borrower, index) => (
                    <div key={borrower.employee_id} className="borrower-item">
                      <span className="rank">#{index + 1}</span>
                      <div className="borrower-info">
                        <span className="borrower-name">{borrower.employee_name}</span>
                        <span className="borrower-dept">{borrower.department}</span>
                      </div>
                      <span className="book-count">{borrower.books_count} books</span>
                    </div>
                  ))}
                  {analytics.employee_statistics.top_borrowers.length === 0 && (
                    <p>No books currently borrowed</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'books' && (
          <div className="books-section">
            <h2>📚 Book Management</h2>
            
            <div className="add-book-form">
              <h3>Add New Book</h3>
              <div className="form-grid">
                <input
                  type="text"
                  placeholder="Book Title"
                  value={newBook.title}
                  onChange={(e) => setNewBook({...newBook, title: e.target.value})}
                />
                <input
                  type="text"
                  placeholder="Author"
                  value={newBook.author}
                  onChange={(e) => setNewBook({...newBook, author: e.target.value})}
                />
                <input
                  type="text"
                  placeholder="Genre"
                  value={newBook.genre}
                  onChange={(e) => setNewBook({...newBook, genre: e.target.value})}
                />
                <input
                  type="text"
                  placeholder="Rack Number"
                  value={newBook.rack_no}
                  onChange={(e) => setNewBook({...newBook, rack_no: e.target.value})}
                />
                <input
                  type="text"
                  placeholder="Book Number"
                  value={newBook.book_no}
                  onChange={(e) => setNewBook({...newBook, book_no: e.target.value})}
                />
                <button onClick={addBook} className="btn btn-primary">
                  ➕ Add Book
                </button>
              </div>
            </div>

            <div className="books-table">
              <h3>All Books ({books.length})</h3>
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Title</th>
                      <th>Author</th>
                      <th>Genre</th>
                      <th>Rack</th>
                      <th>Status</th>
                      <th>Times Taken</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {books.map(book => (
                      <tr key={book.id}>
                        <td>{book.id}</td>
                        <td>{book.title}</td>
                        <td>{book.author}</td>
                        <td>{book.genre}</td>
                        <td>{book.rack_no}</td>
                        <td>
                          <span className={`status-badge ${book.status}`}>
                            {book.status}
                          </span>
                        </td>
                        <td>{book.times_taken || 0}</td>
                        <td>
                          <button 
                            onClick={() => deleteBook(book.id)}
                            className="btn btn-danger btn-sm"
                            disabled={book.status !== 'available'}
                          >
                            🗑️ Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'feedback' && (
          <div className="feedback-section">
            <h2>💬 Employee Feedback</h2>
            
            <div className="feedback-list">
              {feedback.map(item => (
                <div key={item.id} className="feedback-item">
                  <div className="feedback-header">
                    <h4>{item.title || `${item.type} feedback`}</h4>
                    <span className={`status-badge ${item.status}`}>{item.status}</span>
                  </div>
                  
                  <div className="feedback-details">
                    <p><strong>From:</strong> {item.employee_name}</p>
                    <p><strong>Type:</strong> {item.type}</p>
                    <p><strong>Date:</strong> {item.submitted_date}</p>
                    <p><strong>Message:</strong> {item.message}</p>
                    
                    {item.book_details && Object.keys(item.book_details).length > 0 && (
                      <div className="book-request-details">
                        <p><strong>Requested Book:</strong></p>
                        <ul>
                          {item.book_details.title && <li>Title: {item.book_details.title}</li>}
                          {item.book_details.author && <li>Author: {item.book_details.author}</li>}
                          {item.book_details.genre && <li>Genre: {item.book_details.genre}</li>}
                        </ul>
                      </div>
                    )}
                  </div>

                  {item.status === 'pending' && (
                    <div className="feedback-actions">
                      <textarea
                        placeholder="Admin response..."
                        id={`response-${item.id}`}
                        rows="3"
                      />
                      <div className="action-buttons">
                        <button 
                          onClick={() => {
                            const response = document.getElementById(`response-${item.id}`).value;
                            if (response.trim()) {
                              respondToFeedback(item.id, response, 'reviewed');
                            } else {
                              alert('Please enter a response');
                            }
                          }}
                          className="btn btn-primary"
                        >
                          📝 Send Response
                        </button>
                      </div>
                    </div>
                  )}

                  {item.admin_response && (
                    <div className="admin-response">
                      <p><strong>Admin Response:</strong> {item.admin_response}</p>
                      <p><small>Responded on: {item.admin_response_date}</small></p>
                    </div>
                  )}
                </div>
              ))}
              
              {feedback.length === 0 && (
                <p>No feedback received yet.</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'purchases' && (
          <div className="purchases-section">
            <h2>🛒 Book Purchase Requests</h2>
            
            <div className="purchase-list">
              {purchaseRequests.map(request => (
                <div key={request.id} className="purchase-item">
                  <div className="purchase-header">
                    <h4>{request.book_title}</h4>
                    <span className={`status-badge ${request.status}`}>{request.status}</span>
                  </div>
                  
                  <div className="purchase-details">
                    <p><strong>Requested by:</strong> {request.requested_by}</p>
                    <p><strong>Author:</strong> {request.book_author}</p>
                    <p><strong>Genre:</strong> {request.book_genre}</p>
                    <p><strong>Reason:</strong> {request.reason}</p>
                    <p><strong>Date:</strong> {request.requested_date}</p>
                  </div>

                  {request.status === 'pending' && (
                    <div className="purchase-actions">
                      <button 
                        onClick={() => updatePurchaseRequest(request.id, 'approved', true)}
                        className="btn btn-success"
                      >
                        ✅ Approve & Add to Library
                      </button>
                      <button 
                        onClick={() => updatePurchaseRequest(request.id, 'approved', false)}
                        className="btn btn-primary"
                      >
                        ✅ Approve Only
                      </button>
                      <button 
                        onClick={() => updatePurchaseRequest(request.id, 'rejected')}
                        className="btn btn-danger"
                      >
                        ❌ Reject
                      </button>
                    </div>
                  )}

                  {request.admin_notes && (
                    <div className="admin-notes">
                      <p><strong>Admin Notes:</strong> {request.admin_notes}</p>
                    </div>
                  )}
                </div>
              ))}
              
              {purchaseRequests.length === 0 && (
                <p>No purchase requests yet.</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'employees' && analytics && (
          <div className="employees-section">
            <h2>👥 Employee Book Tracking</h2>

            <div className="employee-stats-grid">
              <div className="stat-card">
                <h3>Total Employees</h3>
                <div className="stat-number">{analytics.employee_statistics.total_employees}</div>
              </div>
              <div className="stat-card">
                <h3>Employees with Books</h3>
                <div className="stat-number">{analytics.employee_statistics.employees_with_books}</div>
              </div>
              <div className="stat-card">
                <h3>Total Books Borrowed</h3>
                <div className="stat-number">{analytics.employee_statistics.total_books_borrowed}</div>
              </div>
              <div className="stat-card">
                <h3>Borrowing Rate</h3>
                <div className="stat-number">
                  {analytics.employee_statistics.total_employees > 0
                    ? Math.round((analytics.employee_statistics.employees_with_books / analytics.employee_statistics.total_employees) * 100)
                    : 0}%
                </div>
              </div>
            </div>

            <div className="employee-tracking-grid">
              <div className="tracking-card">
                <h3>🏆 Top Borrowers</h3>
                <div className="top-borrowers-list">
                  {analytics.employee_statistics.top_borrowers.map((borrower, index) => (
                    <div key={borrower.employee_id} className="top-borrower-item">
                      <div className="borrower-rank">#{index + 1}</div>
                      <div className="borrower-details">
                        <div className="borrower-name">{borrower.employee_name}</div>
                        <div className="borrower-id">ID: {borrower.employee_id}</div>
                        <div className="borrower-dept">{borrower.department}</div>
                        <div className="borrower-phone">📞 {borrower.phone}</div>
                      </div>
                      <div className="borrower-books">
                        <div className="book-count">{borrower.books_count} books</div>
                        <div className="book-list">
                          {borrower.books.map((book, idx) => (
                            <div key={idx} className="borrowed-book">
                              <span className="book-title">{book.title}</span>
                              <span className={`book-status ${book.status}`}>
                                {book.status === 'overdue' ? `Overdue` : `${book.days_remaining} days left`}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="tracking-card">
                <h3>🏢 Department Statistics</h3>
                <div className="department-stats">
                  {Object.entries(analytics.employee_statistics.department_book_stats).map(([dept, stats]) => (
                    <div key={dept} className="department-stat-item">
                      <div className="dept-header">
                        <h4>{dept}</h4>
                        <span className="dept-summary">
                          {stats.employees_with_books}/{stats.total_employees} employees
                        </span>
                      </div>
                      <div className="dept-details">
                        <div className="dept-metric">
                          <span>Books Taken:</span>
                          <span>{stats.total_books_taken}</span>
                        </div>
                        <div className="dept-metric">
                          <span>Overdue:</span>
                          <span className="overdue">{stats.overdue_books}</span>
                        </div>
                        <div className="dept-metric">
                          <span>Participation:</span>
                          <span>
                            {stats.total_employees > 0
                              ? Math.round((stats.employees_with_books / stats.total_employees) * 100)
                              : 0}%
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="all-borrowers-section">
              <h3>📋 All Current Borrowers ({analytics.employee_statistics.employees_with_books_details.length})</h3>
              <div className="borrowers-table">
                <table>
                  <thead>
                    <tr>
                      <th>Employee</th>
                      <th>Department</th>
                      <th>Book</th>
                      <th>Author</th>
                      <th>Taken Date</th>
                      <th>Due Date</th>
                      <th>Status</th>
                      <th>Days Left</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analytics.employee_statistics.employees_with_books_details.map((item, index) => (
                      <tr key={index} className={item.status === 'overdue' ? 'overdue-row' : ''}>
                        <td>
                          <div className="employee-cell">
                            <div className="emp-name">{item.employee_name}</div>
                            <div className="emp-id">{item.employee_id}</div>
                            <div className="emp-phone">📞 {item.phone}</div>
                          </div>
                        </td>
                        <td>{item.department}</td>
                        <td className="book-title-cell">{item.book_title}</td>
                        <td>{item.book_author}</td>
                        <td>{item.taken_date}</td>
                        <td>{item.due_date}</td>
                        <td>
                          <span className={`status-badge ${item.status}`}>
                            {item.status}
                          </span>
                        </td>
                        <td>
                          <span className={item.days_remaining <= 0 ? 'overdue-days' : item.days_remaining <= 3 ? 'warning-days' : 'normal-days'}>
                            {item.days_remaining <= 0 ? 'Overdue' : `${item.days_remaining} days`}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {analytics.employee_statistics.employees_with_books_details.length === 0 && (
                  <div className="no-borrowers">
                    <p>No books are currently borrowed by any employee.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
