import React, { useState, useEffect } from 'react';
import './EnhancedAdminDashboard.css';

const EnhancedAdminDashboard = ({ employee, onLogout }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [books, setBooks] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [loading, setLoading] = useState(false);
  const [languageFilter, setLanguageFilter] = useState('all');
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showEmployeeModal, setShowEmployeeModal] = useState(false);
  const [realTimeData, setRealTimeData] = useState({});
  const [refreshInterval, setRefreshInterval] = useState(null);

  useEffect(() => {
    fetchDashboardData();

    // Set up real-time refresh every 30 seconds
    const interval = setInterval(() => {
      fetchDashboardData();
    }, 30000);

    setRefreshInterval(interval);

    return () => {
      if (interval) clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    calculateAnalytics();
  }, [books, employees]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch books
      const booksResponse = await fetch('http://localhost:5000/books');
      if (booksResponse.ok) {
        const booksData = await booksResponse.json();
        setBooks(booksData.books || []);
      }

      // Fetch employees
      const employeesResponse = await fetch('http://localhost:5000/employees');
      if (employeesResponse.ok) {
        const employeesData = await employeesResponse.json();
        setEmployees(employeesData.employees || []);
      }

      // Fetch feedback
      const feedbackResponse = await fetch('http://localhost:5000/feedback');
      if (feedbackResponse.ok) {
        const feedbackData = await feedbackResponse.json();
        setFeedback(feedbackData.feedback || []);
      }

      // Calculate analytics
      calculateAnalytics();
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateAnalytics = () => {
    if (!books.length || !employees.length) return;

    const totalBooks = books.length;
    const availableBooks = books.filter(book => book.status === 'available').length;
    const takenBooks = books.filter(book => book.status === 'taken').length;
    const overdueBooks = books.filter(book => book.status === 'overdue').length;

    const englishBooks = books.filter(book => book.language === 'English').length;
    const tamilBooks = books.filter(book => book.language === 'Tamil').length;

    const englishTaken = books.filter(book => book.status === 'taken' && book.language === 'English').length;
    const tamilTaken = books.filter(book => book.status === 'taken' && book.language === 'Tamil').length;

    const employeesWithBooks = new Set(
      books.filter(book => book.status === 'taken').map(book => book.taken_by_employee_id)
    ).size;

    // Department-wise analysis
    const departmentStats = {};
    employees.forEach(emp => {
      const dept = emp.department || 'Unknown';
      if (!departmentStats[dept]) {
        departmentStats[dept] = { total: 0, withBooks: 0, booksCount: 0 };
      }
      departmentStats[dept].total++;

      const empBooks = books.filter(book =>
        book.status === 'taken' && book.taken_by_employee_id === emp.employee_id
      );

      if (empBooks.length > 0) {
        departmentStats[dept].withBooks++;
        departmentStats[dept].booksCount += empBooks.length;
      }
    });

    // Genre analysis
    const genreStats = {};
    books.forEach(book => {
      const genre = book.genre || 'Unknown';
      if (!genreStats[genre]) {
        genreStats[genre] = { total: 0, taken: 0, language: book.language };
      }
      genreStats[genre].total++;
      if (book.status === 'taken') {
        genreStats[genre].taken++;
      }
    });

    // Most popular books
    const popularBooks = books
      .filter(book => book.times_taken > 0)
      .sort((a, b) => b.times_taken - a.times_taken)
      .slice(0, 10);

    // Due date analysis
    const today = new Date();
    const dueSoon = books.filter(book => {
      if (book.status === 'taken' && book.due_date) {
        const dueDate = new Date(book.due_date);
        const daysDiff = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
        return daysDiff <= 3 && daysDiff >= 0;
      }
      return false;
    });

    setAnalytics({
      totalBooks,
      availableBooks,
      takenBooks,
      overdueBooks,
      englishBooks,
      tamilBooks,
      englishTaken,
      tamilTaken,
      employeesWithBooks,
      totalEmployees: employees.length,
      departmentStats,
      genreStats,
      popularBooks,
      dueSoon: dueSoon.length,
      totalFeedback: feedback.length,
      utilizationRate: totalBooks > 0 ? ((takenBooks / totalBooks) * 100).toFixed(1) : 0
    });
  };

  const renderOverview = () => (
    <div className="admin-overview">
      {/* Real-time Status Header */}
      <div className="real-time-header">
        <div className="status-indicator">
          <span className="live-dot"></span>
          <span>Live Dashboard - Updates every 30 seconds</span>
        </div>
        <div className="last-updated">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Main Statistics Grid */}
      <div className="stats-grid">
        <div className="stat-card total-books premium">
          <div className="stat-icon">📚</div>
          <div className="stat-content">
            <h3>{analytics.totalBooks}</h3>
            <p>Total Library Collection</p>
            <div className="stat-breakdown">
              <span>🇬🇧 {analytics.englishBooks} English Books</span>
              <span>🇮🇳 {analytics.tamilBooks} தமிழ் நூல்கள்</span>
            </div>
            <div className="utilization-rate">
              <span>📊 {analytics.utilizationRate}% Utilization Rate</span>
            </div>
          </div>
        </div>

        <div className="stat-card books-in-circulation premium">
          <div className="stat-icon">🔄</div>
          <div className="stat-content">
            <h3>{analytics.takenBooks}</h3>
            <p>Books in Circulation</p>
            <div className="language-breakdown">
              <div className="lang-stat">
                <span className="lang-label">English:</span>
                <span className="lang-count">{analytics.englishTaken}</span>
              </div>
              <div className="lang-stat">
                <span className="lang-label">தமிழ்:</span>
                <span className="lang-count">{analytics.tamilTaken}</span>
              </div>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill taken"
                style={{width: `${(analytics.takenBooks / analytics.totalBooks) * 100}%`}}
              ></div>
            </div>
          </div>
        </div>

        <div className="stat-card available-books premium">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{analytics.availableBooks}</h3>
            <p>Available for Borrowing</p>
            <div className="availability-rate">
              <span>{Math.round((analytics.availableBooks / analytics.totalBooks) * 100)}% Available</span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill available"
                style={{width: `${(analytics.availableBooks / analytics.totalBooks) * 100}%`}}
              ></div>
            </div>
          </div>
        </div>

        <div className="stat-card active-readers premium">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>{analytics.employeesWithBooks}</h3>
            <p>Active Readers</p>
            <div className="reader-percentage">
              <span>{Math.round((analytics.employeesWithBooks / analytics.totalEmployees) * 100)}% of Staff</span>
            </div>
            <div className="stat-breakdown">
              <span>📊 {analytics.totalEmployees} Total Employees</span>
            </div>
          </div>
        </div>

        <div className="stat-card due-soon warning">
          <div className="stat-icon">⏰</div>
          <div className="stat-content">
            <h3>{analytics.dueSoon}</h3>
            <p>Due Within 3 Days</p>
            <div className="urgency-indicator">
              {analytics.dueSoon > 0 ? (
                <span className="urgent">🚨 Requires Attention</span>
              ) : (
                <span className="good">✅ All Current</span>
              )}
            </div>
          </div>
        </div>

        <div className="stat-card overdue danger">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>{analytics.overdueBooks}</h3>
            <p>Overdue Books</p>
            <div className="overdue-indicator">
              {analytics.overdueBooks > 0 ? (
                <span className="critical">📞 Contact Required</span>
              ) : (
                <span className="excellent">🎉 No Overdue</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Department Analytics */}
      <div className="department-analytics">
        <div className="section-header">
          <h3>🏢 Department-wise Reading Analytics</h3>
          <div className="analytics-summary">
            <span>📈 Engagement tracking across {Object.keys(analytics.departmentStats || {}).length} departments</span>
          </div>
        </div>
        <div className="department-grid">
          {Object.entries(analytics.departmentStats || {}).map(([dept, stats]) => (
            <div key={dept} className="department-card">
              <div className="dept-header">
                <h4>{dept}</h4>
                <div className="dept-stats-summary">
                  <span className="books-count">{stats.booksCount} books</span>
                </div>
              </div>
              <div className="dept-metrics">
                <div className="metric">
                  <span className="metric-label">Total Staff:</span>
                  <span className="metric-value">{stats.total}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Active Readers:</span>
                  <span className="metric-value">{stats.withBooks}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Engagement:</span>
                  <span className="metric-value">{Math.round((stats.withBooks / stats.total) * 100)}%</span>
                </div>
              </div>
              <div className="dept-progress">
                <div className="progress-bar">
                  <div
                    className="progress-fill dept"
                    style={{width: `${(stats.withBooks / stats.total) * 100}%`}}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Popular Books Section */}
      <div className="popular-books-section">
        <div className="section-header">
          <h3>🔥 Most Popular Books</h3>
          <div className="popularity-summary">
            <span>📊 Based on borrowing frequency</span>
          </div>
        </div>
        <div className="popular-books-grid">
          {analytics.popularBooks?.slice(0, 6).map((book, index) => (
            <div key={book.id} className="popular-book-card">
              <div className="book-rank">#{index + 1}</div>
              <div className="book-info">
                <h5>{book.title}</h5>
                <p>{book.author}</p>
                <div className="book-meta">
                  <span className={`language-tag ${book.language?.toLowerCase()}`}>
                    {book.language === 'Tamil' ? '🇮🇳 தமிழ்' : '🇬🇧 English'}
                  </span>
                  <span className="times-taken">📚 {book.times_taken} times</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderBooks = () => (
    <div className="admin-books">
      <div className="books-header">
        <h3>📚 Book Management</h3>
        <div className="book-filters">
          <select 
            value={languageFilter} 
            onChange={(e) => setLanguageFilter(e.target.value)}
            className="language-select"
          >
            <option value="all">All Languages</option>
            <option value="English">English Books</option>
            <option value="Tamil">Tamil Books</option>
          </select>
        </div>
      </div>
      
      <div className="books-table">
        <table>
          <thead>
            <tr>
              <th>Book ID</th>
              <th>Title</th>
              <th>Author</th>
              <th>Language</th>
              <th>Status</th>
              <th>Taken By</th>
              <th>Due Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {books
              .filter(book => languageFilter === 'all' || book.language === languageFilter)
              .map(book => (
                <tr key={book.id}>
                  <td>{book.book_no}</td>
                  <td className="book-title">{book.title}</td>
                  <td>{book.author}</td>
                  <td>
                    <span className={`language-badge ${book.language?.toLowerCase()}`}>
                      {book.language === 'Tamil' ? '🇮🇳 தமிழ்' : '🇬🇧 English'}
                    </span>
                  </td>
                  <td>
                    <span className={`status-badge ${book.status}`}>
                      {book.status}
                    </span>
                  </td>
                  <td>{book.taken_by_name || '-'}</td>
                  <td>{book.due_date || '-'}</td>
                  <td>
                    <button className="action-btn edit">✏️ Edit</button>
                    <button className="action-btn delete">🗑️ Delete</button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderEmployees = () => (
    <div className="admin-employees">
      <div className="employees-header">
        <h3>👥 Employee Management</h3>
        <div className="employees-summary">
          <span>📊 {employees.length} Total Employees</span>
          <span>📚 {analytics.employeesWithBooks} Currently Reading</span>
        </div>
      </div>

      <div className="employees-table">
        <table>
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Name</th>
              <th>Department</th>
              <th>Email</th>
              <th>Books Taken</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.map(emp => {
              const empBooks = books.filter(book =>
                book.status === 'taken' && book.taken_by_employee_id === emp.employee_id
              );
              const hasOverdue = empBooks.some(book => book.status === 'overdue');

              return (
                <tr key={emp.employee_id}>
                  <td>{emp.employee_id}</td>
                  <td className="employee-name-cell">
                    <strong>{emp.name}</strong>
                  </td>
                  <td>{emp.department}</td>
                  <td>{emp.email}</td>
                  <td>
                    <div className="books-taken-info">
                      <span className="books-count">{empBooks.length}</span>
                      {empBooks.length > 0 && (
                        <div className="books-details">
                          {empBooks.map(book => (
                            <div key={book.id} className="book-item">
                              <span className="book-title">{book.title}</span>
                              <span className={`due-date ${hasOverdue ? 'overdue' : ''}`}>
                                Due: {book.due_date}
                              </span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </td>
                  <td>
                    <span className={`employee-status ${empBooks.length > 0 ? 'active' : 'inactive'} ${hasOverdue ? 'overdue' : ''}`}>
                      {hasOverdue ? '⚠️ Overdue' : empBooks.length > 0 ? '📚 Reading' : '✅ Available'}
                    </span>
                  </td>
                  <td>
                    <button
                      className="action-btn view"
                      onClick={() => {
                        setSelectedEmployee(emp);
                        setShowEmployeeModal(true);
                      }}
                    >
                      👁️ View
                    </button>
                    <button className="action-btn edit">✏️ Edit</button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderFeedback = () => (
    <div className="admin-feedback">
      <div className="feedback-header">
        <h3>💬 Employee Feedback</h3>
        <div className="feedback-summary">
          <span>📝 {feedback.length} Total Feedback</span>
        </div>
      </div>
      <div className="feedback-list">
        {feedback.length === 0 ? (
          <div className="no-feedback">
            <div className="no-feedback-icon">📝</div>
            <h4>No Feedback Yet</h4>
            <p>Employee feedback will appear here when submitted</p>
          </div>
        ) : (
          feedback.map((item, index) => (
            <div key={index} className="feedback-item">
              <div className="feedback-header">
                <div className="feedback-employee">
                  <span className="employee-name">{item.employee_name}</span>
                  <span className="employee-id">ID: {item.employee_id}</span>
                </div>
                <span className="feedback-date">{item.date}</span>
              </div>
              <div className="feedback-content">
                <p>{item.message}</p>
              </div>
              <div className="feedback-type">
                <span className={`feedback-tag ${item.type}`}>
                  {item.type === 'suggestion' ? '💡 Suggestion' :
                   item.type === 'complaint' ? '⚠️ Complaint' :
                   '💬 General'}
                </span>
              </div>
              <div className="feedback-actions">
                <button className="action-btn reply">💬 Reply</button>
                <button className="action-btn mark-read">✅ Mark Read</button>
                <button className="action-btn priority">⭐ Priority</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );

  return (
    <div className="enhanced-admin-dashboard">
      {/* Header */}
      <div className="admin-header">
        <div className="admin-info">
          <div className="admin-avatar">👨‍💼</div>
          <div className="admin-details">
            <h2>{employee.name}</h2>
            <p>System Administrator</p>
          </div>
        </div>
        <button onClick={onLogout} className="logout-btn">
          🚪 Logout
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="admin-nav">
        <button
          className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button
          className={`nav-tab ${activeTab === 'books' ? 'active' : ''}`}
          onClick={() => setActiveTab('books')}
        >
          📚 Books
        </button>
        <button
          className={`nav-tab ${activeTab === 'employees' ? 'active' : ''}`}
          onClick={() => setActiveTab('employees')}
        >
          👥 Employees
        </button>
        <button
          className={`nav-tab ${activeTab === 'feedback' ? 'active' : ''}`}
          onClick={() => setActiveTab('feedback')}
        >
          💬 Feedback
        </button>
      </div>

      {/* Content */}
      <div className="admin-content">
        {loading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
            <h3>🔄 Loading Dashboard Data...</h3>
            <p>Fetching real-time library analytics</p>
          </div>
        ) : (
          <>
            {activeTab === 'overview' && renderOverview()}
            {activeTab === 'books' && renderBooks()}
            {activeTab === 'employees' && renderEmployees()}
            {activeTab === 'feedback' && renderFeedback()}
          </>
        )}
      </div>
    </div>
  );
};

export default EnhancedAdminDashboard;
