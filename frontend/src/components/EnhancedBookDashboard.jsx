import React, { useState, useEffect } from 'react';
import './EnhancedBookDashboard.css';

const EnhancedBookDashboard = ({ employee }) => {
  const [books, setBooks] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('title');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedBook, setSelectedBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    fetchBooks();
    fetchAnalytics();
  }, [searchTerm, sortBy, filterStatus]);

  const fetchBooks = async () => {
    try {
      const params = new URLSearchParams({
        search: searchTerm,
        sort: sortBy,
        status: filterStatus
      });
      
      const response = await fetch(`http://localhost:5000/books?${params}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setBooks(data.books);
      }
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('http://localhost:5000/book-analytics');
      const data = await response.json();
      
      if (data.status === 'success') {
        setAnalytics(data.analytics);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setLoading(false);
    }
  };

  const takeBook = async (book) => {
    try {
      const response = await fetch('http://localhost:5000/take-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          employee_id: employee.employee_id,
          book_id: book.id,
          employee_name: employee.name
        }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        alert(`Book "${book.title}" taken successfully!\nDue date: ${data.book.due_date}`);
        fetchBooks();
        fetchAnalytics();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error taking book:', error);
      alert('Failed to take book');
    }
  };

  const returnBook = async (book) => {
    try {
      const response = await fetch('http://localhost:5000/return-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          book_id: book.id
        }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        alert(`Book "${book.title}" returned successfully!`);
        fetchBooks();
        fetchAnalytics();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error returning book:', error);
      alert('Failed to return book');
    }
  };

  const renewBook = async (book) => {
    try {
      const response = await fetch('http://localhost:5000/renew-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          book_id: book.id
        }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        alert(`Book "${book.title}" renewed successfully!\nNew due date: ${data.new_due_date}`);
        fetchBooks();
        fetchAnalytics();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error renewing book:', error);
      alert('Failed to renew book');
    }
  };

  const getStatusColor = (status, daysRemaining) => {
    if (status === 'available') return '#28a745';
    if (status === 'overdue') return '#dc3545';
    if (status === 'taken') {
      if (daysRemaining <= 3) return '#ffc107';
      return '#17a2b8';
    }
    return '#6c757d';
  };

  const getStatusText = (book) => {
    if (book.status === 'available') return 'Available';
    if (book.status === 'overdue') return `Overdue (${book.days_overdue} days)`;
    if (book.status === 'taken') {
      const days = book.days_remaining;
      if (days <= 0) return 'Due today';
      if (days <= 3) return `Due in ${days} day${days > 1 ? 's' : ''}`;
      return `Due in ${days} days`;
    }
    return book.status;
  };

  const filteredBooks = books.filter(book => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      book.title.toLowerCase().includes(search) ||
      book.author.toLowerCase().includes(search) ||
      book.genre.toLowerCase().includes(search)
    );
  });

  if (loading) {
    return <div className="loading">Loading book dashboard...</div>;
  }

  return (
    <div className="enhanced-book-dashboard">
      <h2>📚 Smart Library - Enhanced Book Dashboard</h2>
      
      {/* Analytics Section */}
      {analytics && (
        <div className="analytics-section">
          <h3>📊 Library Analytics</h3>
          <div className="analytics-grid">
            <div className="analytics-card">
              <h4>Total Books</h4>
              <div className="analytics-number">{analytics.total_books}</div>
            </div>
            <div className="analytics-card">
              <h4>Available</h4>
              <div className="analytics-number available">{analytics.available_books}</div>
            </div>
            <div className="analytics-card">
              <h4>Taken</h4>
              <div className="analytics-number taken">{analytics.taken_books}</div>
            </div>
            <div className="analytics-card">
              <h4>Overdue</h4>
              <div className="analytics-number overdue">{analytics.overdue_books}</div>
            </div>
          </div>

          {/* Most Popular Books */}
          {analytics.most_popular_books.length > 0 && (
            <div className="popular-books">
              <h4>🔥 Most Popular Books</h4>
              <div className="popular-books-list">
                {analytics.most_popular_books.slice(0, 5).map((book, index) => (
                  <div key={book.id} className="popular-book-item">
                    <span className="rank">#{index + 1}</span>
                    <span className="title">{book.title}</span>
                    <span className="times-taken">{book.times_taken} times</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Genre Distribution */}
          <div className="genre-distribution">
            <h4>📖 Books by Genre</h4>
            <div className="genre-grid">
              {Object.entries(analytics.genre_distribution).map(([genre, stats]) => (
                <div key={genre} className="genre-card">
                  <h5>{genre}</h5>
                  <div className="genre-stats">
                    <span>Total: {stats.total}</span>
                    <span>Available: {stats.available}</span>
                    <span>Taken: {stats.taken}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Search and Filter Section */}
      <div className="search-filter-section">
        <div className="search-bar">
          <input
            type="text"
            placeholder="🔍 Search books by title, author, or genre..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-controls">
          <select 
            value={sortBy} 
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="title">Sort by Title (A-Z)</option>
            <option value="author">Sort by Author</option>
            <option value="genre">Sort by Genre</option>
            <option value="popularity">Sort by Popularity</option>
          </select>

          <select 
            value={filterStatus} 
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Books</option>
            <option value="available">Available Only</option>
            <option value="taken">Taken Only</option>
            <option value="overdue">Overdue Only</option>
          </select>
        </div>
      </div>

      {/* Books Display */}
      <div className="books-section">
        <h3>📚 Books ({filteredBooks.length} found)</h3>
        
        {/* Dropdown Toggle */}
        <button 
          className="dropdown-toggle"
          onClick={() => setShowDropdown(!showDropdown)}
        >
          {showDropdown ? '📋 Show Grid View' : '📋 Show Dropdown View'}
        </button>

        {showDropdown ? (
          /* Dropdown Format */
          <div className="books-dropdown">
            <select 
              className="books-select"
              onChange={(e) => {
                const bookId = parseInt(e.target.value);
                const book = filteredBooks.find(b => b.id === bookId);
                setSelectedBook(book);
              }}
            >
              <option value="">Select a book...</option>
              {filteredBooks.map(book => (
                <option key={book.id} value={book.id}>
                  {book.title} - {book.author} ({getStatusText(book)})
                </option>
              ))}
            </select>

            {selectedBook && (
              <div className="selected-book-details">
                <h4>{selectedBook.title}</h4>
                <p><strong>Author:</strong> {selectedBook.author}</p>
                <p><strong>Genre:</strong> {selectedBook.genre}</p>
                <p><strong>Rack:</strong> {selectedBook.rack_no}</p>
                <p><strong>Status:</strong> 
                  <span 
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(selectedBook.status, selectedBook.days_remaining) }}
                  >
                    {getStatusText(selectedBook)}
                  </span>
                </p>
                
                {selectedBook.taken_by && (
                  <div className="book-taken-info">
                    <p><strong>Taken by:</strong> {selectedBook.taken_by}</p>
                    <p><strong>Taken date:</strong> {selectedBook.taken_date}</p>
                    <p><strong>Due date:</strong> {selectedBook.due_date}</p>
                  </div>
                )}

                <div className="book-actions">
                  {selectedBook.status === 'available' && (
                    <button 
                      className="btn btn-primary"
                      onClick={() => takeBook(selectedBook)}
                    >
                      📖 Take Book
                    </button>
                  )}
                  
                  {selectedBook.status === 'taken' && selectedBook.taken_by === employee.name && (
                    <>
                      <button 
                        className="btn btn-success"
                        onClick={() => returnBook(selectedBook)}
                      >
                        ↩️ Return Book
                      </button>
                      <button 
                        className="btn btn-warning"
                        onClick={() => renewBook(selectedBook)}
                      >
                        🔄 Renew (14 days)
                      </button>
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Grid Format */
          <div className="books-grid">
            {filteredBooks.map(book => (
              <div key={book.id} className="book-card">
                <div className="book-header">
                  <h4 className="book-title">{book.title}</h4>
                  <span 
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(book.status, book.days_remaining) }}
                  >
                    {getStatusText(book)}
                  </span>
                </div>
                
                <div className="book-details">
                  <p><strong>Author:</strong> {book.author}</p>
                  <p><strong>Genre:</strong> {book.genre}</p>
                  <p><strong>Rack:</strong> {book.rack_no}</p>
                  {book.times_taken > 0 && (
                    <p><strong>Popularity:</strong> Taken {book.times_taken} times</p>
                  )}
                </div>

                {book.taken_by && (
                  <div className="book-taken-info">
                    <p><strong>Taken by:</strong> {book.taken_by}</p>
                    <p><strong>Due:</strong> {book.due_date}</p>
                  </div>
                )}

                <div className="book-actions">
                  {book.status === 'available' && (
                    <button 
                      className="btn btn-primary"
                      onClick={() => takeBook(book)}
                    >
                      📖 Take Book
                    </button>
                  )}
                  
                  {book.status === 'taken' && book.taken_by === employee.name && (
                    <>
                      <button 
                        className="btn btn-success"
                        onClick={() => returnBook(book)}
                      >
                        ↩️ Return
                      </button>
                      <button 
                        className="btn btn-warning"
                        onClick={() => renewBook(book)}
                      >
                        🔄 Renew
                      </button>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EnhancedBookDashboard;
