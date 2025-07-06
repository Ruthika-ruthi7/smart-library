import React, { useState, useEffect } from 'react';
import './AdvancedEmployeeDashboard.css';
import FeedbackForm from './FeedbackForm.jsx';

const AdvancedEmployeeDashboard = ({ employee, onLogout }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [allBooks, setAllBooks] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [languageFilter, setLanguageFilter] = useState('all');
  const [myBooks, setMyBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);
  const [bookStats, setBookStats] = useState({
    totalTaken: 0,
    dueForRenewal: 0,
    returned: 0,
    monthlyLimit: 2,
    currentlyHolding: 0
  });

  useEffect(() => {
    fetchMyBooks();
    fetchAllBooks();
  }, []);

  const fetchAllBooks = async (language = 'all') => {
    try {
      const url = language === 'all'
        ? 'http://localhost:5000/books'
        : `http://localhost:5000/books?language=${language}`;
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setAllBooks(data.books || []);
      }
    } catch (error) {
      console.error('Error fetching all books:', error);
    }
  };

  const fetchMyBooks = async () => {
    try {
      const response = await fetch(`http://localhost:5000/employee/${employee.id}/books`);
      if (response.ok) {
        const data = await response.json();
        setMyBooks(data.books || []);
        calculateBookStats(data.books || []);
      }
    } catch (error) {
      console.error('Error fetching my books:', error);
    }
  };

  const calculateBookStats = (books) => {
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();

    // Count ALL book taking instances this month (including re-taken books)
    let monthlyTaken = 0;
    const currentlyHolding = books.filter(book => book.status === 'taken').length;

    // Count each book taking instance this month
    books.forEach(book => {
      // Count current book if taken this month
      if (book.taken_date && book.status === 'taken') {
        const takenDate = new Date(book.taken_date);
        if (takenDate.getMonth() === currentMonth && takenDate.getFullYear() === currentYear) {
          monthlyTaken++;
        }
      }

      // Count from monthly history (for re-taken books)
      if (book.monthly_history && Array.isArray(book.monthly_history)) {
        book.monthly_history.forEach(history => {
          if (history.month === (currentMonth + 1) && history.year === currentYear) {
            monthlyTaken++;
          }
        });
      }
    });

    const dueForRenewal = books.filter(book => {
      if (!book.due_date || book.status !== 'taken') return false;
      const dueDate = new Date(book.due_date);
      const daysDiff = Math.ceil((dueDate - currentDate) / (1000 * 60 * 60 * 24));
      return daysDiff <= 3 && daysDiff >= 0;
    }).length;

    const totalReturned = books.filter(book =>
      book.status === 'available' && (book.return_date || book.last_taken_by_employee_id === employee.employee_id)
    ).length;

    setBookStats({
      totalTaken: monthlyTaken,
      dueForRenewal,
      returned: totalReturned,
      monthlyLimit: 2,
      currentlyHolding
    });
  };

  const handleSearchChange = (value) => {
    setSearchQuery(value);

    if (!value.trim()) {
      setFilteredBooks([]);
      setShowDropdown(false);
      setSearchResults([]);
      return;
    }

    // Enhanced search with better matching
    const searchTerm = value.toLowerCase().trim();
    const filtered = allBooks.filter(book => {
      const titleMatch = book.title.toLowerCase().includes(searchTerm);
      const authorMatch = book.author.toLowerCase().includes(searchTerm);
      const idMatch = book.book_no.toLowerCase().includes(searchTerm);
      const genreMatch = book.genre.toLowerCase().includes(searchTerm);

      return titleMatch || authorMatch || idMatch || genreMatch;
    })
    .sort((a, b) => {
      // Sort by relevance: exact matches first, then starts-with, then contains
      const aExact = a.title.toLowerCase() === searchTerm || a.author.toLowerCase() === searchTerm;
      const bExact = b.title.toLowerCase() === searchTerm || b.author.toLowerCase() === searchTerm;
      const aStarts = a.title.toLowerCase().startsWith(searchTerm) || a.author.toLowerCase().startsWith(searchTerm);
      const bStarts = b.title.toLowerCase().startsWith(searchTerm) || b.author.toLowerCase().startsWith(searchTerm);

      if (aExact && !bExact) return -1;
      if (!aExact && bExact) return 1;
      if (aStarts && !bStarts) return -1;
      if (!aStarts && bStarts) return 1;
      return a.title.localeCompare(b.title);
    })
    .slice(0, 8); // Limit to 8 most relevant results

    setFilteredBooks(filtered);
    setShowDropdown(value.length >= 2); // Show dropdown only after 2 characters
  };

  const selectBook = (book) => {
    setSearchQuery(book.title);
    setSearchResults([book]);
    setShowDropdown(false);
  };

  const searchBooks = async () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    setLoading(true);
    try {
      const url = `http://localhost:5000/books/search?q=${encodeURIComponent(searchQuery)}&language=${languageFilter}`;
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.books || []);
        setShowDropdown(false);
      } else {
        setError('Failed to search books');
      }
    } catch (error) {
      setError('Error searching books');
    } finally {
      setLoading(false);
    }
  };

  const takeBook = async (bookId) => {
    // Check restrictions
    if (bookStats.currentlyHolding >= 2) {
      setError('You can only hold 2 books at a time. Please return a book first.');
      return;
    }

    if (bookStats.totalTaken >= bookStats.monthlyLimit) {
      setError('You have reached your monthly limit of 2 books. Please wait for next month.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/take-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          book_id: bookId,
          employee_id: employee.id,
          employee_name: employee.name
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(`📚 Book taken successfully! Due date: ${data.book?.due_date || 'N/A'}`);
        fetchMyBooks();
        searchBooks(); // Refresh search results
        setTimeout(() => setSuccess(''), 5000);
      } else {
        const data = await response.json();
        setError(data.message || 'Failed to take book');
      }
    } catch (error) {
      setError('Error taking book');
    } finally {
      setLoading(false);
    }
  };

  const returnBook = async (bookId) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/return-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          book_id: bookId,
          employee_id: employee.id
        }),
      });

      if (response.ok) {
        setSuccess('Book returned successfully!');
        fetchMyBooks();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        const data = await response.json();
        setError(data.message || 'Failed to return book');
      }
    } catch (error) {
      setError('Error returning book');
    } finally {
      setLoading(false);
    }
  };

  const renewBook = async (bookId) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/renew-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          book_id: bookId,
          employee_id: employee.id
        }),
      });

      if (response.ok) {
        setSuccess('Book renewed successfully!');
        fetchMyBooks();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        const data = await response.json();
        setError(data.message || 'Failed to renew book');
      }
    } catch (error) {
      setError('Error renewing book');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="advanced-employee-dashboard">
      {/* Header with Employee Details */}
      <div className="dashboard-header">
        <div className="employee-info-card">
          <div className="employee-avatar">
            {employee.name.charAt(0).toUpperCase()}
          </div>
          <div className="employee-details">
            <h2>{employee.name}</h2>
            <div className="employee-table-container">
              <table className="employee-info-table">
                <tbody>
                  <tr>
                    <td className="table-label">Employee Name:</td>
                    <td className="table-value">{employee.name}</td>
                  </tr>
                  <tr>
                    <td className="table-label">Employee ID:</td>
                    <td className="table-value">{employee.employee_id}</td>
                  </tr>
                  <tr>
                    <td className="table-label">Mobile Number:</td>
                    <td className="table-value">{employee.phone}</td>
                  </tr>
                  <tr>
                    <td className="table-label">Department:</td>
                    <td className="table-value">{employee.department}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div className="header-actions">
            <button className="feedback-btn" onClick={() => setShowFeedback(true)}>
              <span>💬</span>
              <span>Feedback</span>
            </button>
            <button className="logout-btn" onClick={onLogout}>
              <span>Sign Out</span>
              <span className="logout-icon">⏻</span>
            </button>
          </div>
        </div>
      </div>

      {/* Professional Book Statistics Dashboard */}
      <div className="stats-dashboard">
        <div className="stats-header">
          <h3>📊 Library Usage Statistics</h3>
          <p>Real-time tracking of your book borrowing activity</p>
        </div>

        <div className="book-stats-grid">
          {/* Currently Holding - Priority Card */}
          <div className="stat-card currently-holding priority">
            <div className="stat-header">
              <div className="stat-icon">📚</div>
              <div className="stat-title">Currently Holding</div>
            </div>
            <div className="stat-content">
              <div className="stat-number-large">{bookStats.currentlyHolding}<span className="stat-unit">/2</span></div>
              <div className="stat-progress">
                <div className="progress-bar professional">
                  <div
                    className="progress-fill blue-primary"
                    style={{width: `${(bookStats.currentlyHolding / 2) * 100}%`}}
                  ></div>
                </div>
                <div className="progress-label">Books in possession</div>
              </div>
              <div className="stat-status">
                {bookStats.currentlyHolding >= 2 ? (
                  <span className="status-warning">⚠️ Maximum capacity reached</span>
                ) : (
                  <span className="status-available">✅ {2 - bookStats.currentlyHolding} slot{2 - bookStats.currentlyHolding !== 1 ? 's' : ''} available</span>
                )}
              </div>
            </div>
          </div>

          {/* Monthly Limit - Priority Card */}
          <div className="stat-card monthly-limit priority">
            <div className="stat-header">
              <div className="stat-icon">📖</div>
              <div className="stat-title">Monthly Usage</div>
            </div>
            <div className="stat-content">
              <div className="stat-number-large">{bookStats.totalTaken}<span className="stat-unit">/2</span></div>
              <div className="stat-progress">
                <div className="progress-bar professional">
                  <div
                    className="progress-fill blue-secondary"
                    style={{width: `${(bookStats.totalTaken / bookStats.monthlyLimit) * 100}%`}}
                  ></div>
                </div>
                <div className="progress-label">Books taken this month</div>
              </div>
              <div className="stat-status">
                {bookStats.totalTaken >= bookStats.monthlyLimit ? (
                  <span className="status-warning">⚠️ Monthly limit reached</span>
                ) : (
                  <span className="status-available">✅ {bookStats.monthlyLimit - bookStats.totalTaken} more book{bookStats.monthlyLimit - bookStats.totalTaken !== 1 ? 's' : ''} this month</span>
                )}
              </div>
            </div>
          </div>

          {/* Due for Renewal */}
          <div className="stat-card due-renewal">
            <div className="stat-header">
              <div className="stat-icon">🔄</div>
              <div className="stat-title">Due for Renewal</div>
            </div>
            <div className="stat-content">
              <div className="stat-number-medium">{bookStats.dueForRenewal}</div>
              <div className="stat-description">
                {bookStats.dueForRenewal > 0 ? (
                  <span className="status-warning">📅 {bookStats.dueForRenewal} book{bookStats.dueForRenewal !== 1 ? 's' : ''} due soon</span>
                ) : (
                  <span className="status-success">✅ All books current</span>
                )}
              </div>
            </div>
          </div>

          {/* Books Returned */}
          <div className="stat-card books-returned">
            <div className="stat-header">
              <div className="stat-icon">✅</div>
              <div className="stat-title">Total Returns</div>
            </div>
            <div className="stat-content">
              <div className="stat-number-medium">{bookStats.returned}</div>
              <div className="stat-description">
                <span className="status-info">📚 Lifetime returns</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Search Section with Language Filter */}
      <div className="search-section">
        <div className="search-header">
          <h3>🔍 Find Your Perfect Book</h3>
          <p>Search in English and Tamil books with smart suggestions</p>
          <div className="search-tips">
            <span className="tip">💡 Try: Book title, Author name, or Book ID</span>
          </div>
        </div>

        {/* Language Filter */}
        <div className="language-filter">
          <div className="filter-buttons">
            <button
              className={`filter-btn ${languageFilter === 'all' ? 'active' : ''}`}
              onClick={() => {
                setLanguageFilter('all');
                fetchAllBooks('all');
                setSearchResults([]);
                setSearchQuery('');
              }}
            >
              🌐 All Books
            </button>
            <button
              className={`filter-btn ${languageFilter === 'english' ? 'active' : ''}`}
              onClick={() => {
                setLanguageFilter('english');
                fetchAllBooks('english');
                setSearchResults([]);
                setSearchQuery('');
              }}
            >
              🇬🇧 English
            </button>
            <button
              className={`filter-btn ${languageFilter === 'tamil' ? 'active' : ''}`}
              onClick={() => {
                setLanguageFilter('tamil');
                fetchAllBooks('tamil');
                setSearchResults([]);
                setSearchQuery('');
              }}
            >
              🇮🇳 தமிழ்
            </button>
          </div>
        </div>

        <div className="search-container">
          <div className="search-bar">
            <input
              type="text"
              placeholder={languageFilter === 'tamil' ? "🔍 தலைப்பு, ஆசிரியர் அல்லது புத்தக எண்..." : "🔍 Search by title, author, or book ID..."}
              value={searchQuery}
              onChange={(e) => handleSearchChange(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && searchBooks()}
              className="search-input enhanced"
              onFocus={() => searchQuery && setShowDropdown(filteredBooks.length > 0)}
              onBlur={() => setTimeout(() => setShowDropdown(false), 200)}
            />
            <button
              onClick={searchBooks}
              className="search-btn"
              disabled={loading}
            >
              {loading ? '🔄' : '🔍'}
            </button>
          </div>

          {/* Dropdown Results */}
          {showDropdown && (
            <div className="search-dropdown">
              <div className="dropdown-header">
                <span>📚 Found {filteredBooks.length} books</span>
              </div>
              {filteredBooks.map((book) => (
                <div
                  key={book.id}
                  className="dropdown-item"
                  onClick={() => selectBook(book)}
                >
                  <div className="dropdown-book-info">
                    <div className="dropdown-title">{book.title}</div>
                    <div className="dropdown-details">
                      <span className="dropdown-author">by {book.author}</span>
                      <span className="dropdown-id">ID: {book.book_no}</span>
                      <span className={`dropdown-status ${book.status}`}>
                        {book.status === 'available' ? '✅ Available' : '❌ Taken'}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Messages */}
      {error && (
        <div className="message error-message">
          <span className="message-icon">⚠️</span>
          <span>{error}</span>
          <button onClick={() => setError('')} className="close-btn">×</button>
        </div>
      )}

      {success && (
        <div className="message success-message">
          <span className="message-icon">✅</span>
          <span>{success}</span>
          <button onClick={() => setSuccess('')} className="close-btn">×</button>
        </div>
      )}

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="search-results">
          <h4>Search Results ({searchResults.length} books found)</h4>
          <div className="books-grid">
            {searchResults.map((book) => (
              <div key={book.id} className="book-card">
                <div className="book-header">
                  <h5>{book.title}</h5>
                  <span className={`book-status ${book.status}`}>
                    {book.status === 'available' ? '✅ Available' : '❌ Taken'}
                  </span>
                </div>
                <div className="book-details">
                  <p><strong>Author:</strong> {book.author}</p>
                  <p><strong>Genre:</strong> {book.genre}</p>
                  <p><strong>Book ID:</strong> {book.book_no}</p>
                  <p><strong>Rack:</strong> {book.rack_no}</p>
                  {book.status === 'taken' && book.taken_by_name && (
                    <p><strong>Taken by:</strong> {book.taken_by_name}</p>
                  )}
                </div>
                {book.status === 'available' && (
                  <button 
                    onClick={() => takeBook(book.id)}
                    className="take-book-btn"
                    disabled={loading || bookStats.currentlyHolding >= 2 || bookStats.totalTaken >= bookStats.monthlyLimit}
                  >
                    Take Book
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* My Books */}
      {myBooks.length > 0 && (
        <div className="my-books-section">
          <h4>My Books History ({myBooks.length})</h4>
          <div className="books-grid">
            {myBooks.map((book) => (
              <div key={book.id} className={`book-card my-book ${book.status}`}>
                <div className="book-header">
                  <h5>{book.title}</h5>
                  <span className={`book-status ${book.status}`}>
                    {book.status === 'taken' ? '📖 Currently Borrowed' : '✅ Previously Returned'}
                  </span>
                </div>
                <div className="book-details">
                  <p><strong>Author:</strong> {book.author}</p>
                  <p><strong>Book ID:</strong> {book.book_no}</p>
                  {book.taken_date && (
                    <p><strong>Last Taken:</strong> {new Date(book.taken_date).toLocaleDateString()}</p>
                  )}
                  {book.return_date && book.status !== 'taken' && (
                    <p><strong>Returned:</strong> {new Date(book.return_date).toLocaleDateString()}</p>
                  )}
                  {book.due_date && book.status === 'taken' && (
                    <div className="due-date-info">
                      <p><strong>Due:</strong> {new Date(book.due_date).toLocaleDateString()}</p>
                      <div className="days-remaining">
                        {(() => {
                          const dueDate = new Date(book.due_date);
                          const today = new Date();
                          const diffTime = dueDate - today;
                          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

                          if (diffDays < 0) {
                            return <span className="overdue">⚠️ {Math.abs(diffDays)} days overdue</span>;
                          } else if (diffDays <= 3) {
                            return <span className="due-soon">🔔 Due in {diffDays} days</span>;
                          } else {
                            return <span className="due-later">📅 {diffDays} days remaining</span>;
                          }
                        })()}
                      </div>
                    </div>
                  )}
                </div>

                {/* Action buttons based on book status */}
                {book.status === 'taken' ? (
                  <div className="book-actions">
                    <button
                      onClick={() => returnBook(book.id)}
                      className="return-book-btn"
                      disabled={loading}
                    >
                      Return Book
                    </button>
                    <button
                      onClick={() => renewBook(book.id)}
                      className="renew-book-btn"
                      disabled={loading}
                    >
                      Renew
                    </button>
                  </div>
                ) : (
                  <div className="book-actions">
                    <button
                      onClick={() => takeBook(book.id)}
                      className="retake-book-btn"
                      disabled={loading || bookStats.currentlyHolding >= 2 || bookStats.totalTaken >= bookStats.monthlyLimit}
                    >
                      Take Again
                    </button>
                    <div className="retake-info">
                      <span>📚 You can borrow this book again!</span>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}



      {/* Feedback Modal */}
      {showFeedback && (
        <div className="feedback-modal-overlay">
          <div className="feedback-modal">
            <div className="feedback-header">
              <h3>Submit Feedback</h3>
              <button
                className="close-feedback-btn"
                onClick={() => setShowFeedback(false)}
              >
                ×
              </button>
            </div>
            <FeedbackForm
              employee={employee}
              onClose={() => setShowFeedback(false)}
              onSuccess={(message) => {
                setSuccess(message);
                setShowFeedback(false);
                setTimeout(() => setSuccess(''), 3000);
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedEmployeeDashboard;
