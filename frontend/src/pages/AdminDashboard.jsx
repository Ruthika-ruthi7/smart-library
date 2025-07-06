import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Bar, Doughnut, Pie } from 'react-chartjs-2'
import {
  getAdminData,
  getAllEmployees,
  getAllBooks,
  createEmployee,
  updateEmployee,
  deleteEmployee,
  createBook,
  updateBook,
  deleteBook
} from '../services/api'
import '../components/EnhancedAdminDashboard.css'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview')
  const [adminData, setAdminData] = useState(null)
  const [employees, setEmployees] = useState([])
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [connectionStatus, setConnectionStatus] = useState('connecting')
  const [showModal, setShowModal] = useState(false)
  const [modalType, setModalType] = useState('')
  const [editingItem, setEditingItem] = useState(null)
  const [showEmployeeDetails, setShowEmployeeDetails] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)
  const [dailyTrends, setDailyTrends] = useState([])
  const [monthlyTrends, setMonthlyTrends] = useState([])
  const [popularBooks, setPopularBooks] = useState([])
  const [bookTakingTrends, setBookTakingTrends] = useState([])
  const navigate = useNavigate()

  const testConnection = async () => {
    try {
      console.log('Testing backend connection...')
      const response = await fetch('http://localhost:5000/api/admin/data')
      if (response.ok) {
        setConnectionStatus('connected')
        console.log('✅ Backend connection successful')
      } else {
        setConnectionStatus('error')
        console.log('❌ Backend connection failed:', response.status)
      }
    } catch (error) {
      setConnectionStatus('error')
      console.log('❌ Backend connection error:', error)
    }
  }



  useEffect(() => {
    // Check if user is admin
    const employeeData = localStorage.getItem('employee')
    if (!employeeData) {
      navigate('/login')
      return
    }

    try {
      const parsedEmployee = JSON.parse(employeeData)
      if (parsedEmployee.username !== 'admin') {
        navigate('/employee')
        return
      }
    } catch (err) {
      navigate('/login')
      return
    }

    testConnection()
    fetchData()
  }, [navigate])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [adminResponse, employeesResponse, booksResponse] = await Promise.all([
        getAdminData(),
        getAllEmployees(),
        getAllBooks()
      ])

      if (adminResponse.status === 'success') {
        setAdminData(adminResponse.data)
        console.log('Admin data loaded:', adminResponse.data)
      }
      if (employeesResponse.status === 'success') {
        setEmployees(employeesResponse.employees)
        console.log('Employees loaded:', employeesResponse.employees.length)
      }
      if (booksResponse.status === 'success') {
        setBooks(booksResponse.books)
        console.log('Books loaded:', booksResponse.books.length)
      }
    } catch (err) {
      setError('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  // Generate trend data and analytics
  const generateTrendData = () => {
    if (!books.length) return

    // Generate daily trends (last 30 days)
    const dailyData = []
    const monthlyData = []
    const bookPopularity = {}

    // Simulate daily book taking trends for last 30 days
    for (let i = 29; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      const dateStr = date.toISOString().split('T')[0]

      // Simulate book taking activity (random but realistic)
      const booksPerDay = Math.floor(Math.random() * 15) + 5 // 5-20 books per day
      dailyData.push({
        date: dateStr,
        books_taken: booksPerDay,
        day_name: date.toLocaleDateString('en-US', { weekday: 'short' })
      })
    }

    // Generate monthly trends (last 12 months)
    for (let i = 11; i >= 0; i--) {
      const date = new Date()
      date.setMonth(date.getMonth() - i)
      const monthStr = date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })

      const booksPerMonth = Math.floor(Math.random() * 200) + 100 // 100-300 books per month
      monthlyData.push({
        month: monthStr,
        books_taken: booksPerMonth,
        renewals: Math.floor(booksPerMonth * 0.3),
        returns: Math.floor(booksPerMonth * 0.8)
      })
    }

    // Generate popular books data
    const popularBooksData = books.slice(0, 10).map((book, index) => ({
      ...book,
      times_taken: Math.floor(Math.random() * 50) + 10 + (10 - index) * 5, // More popular books taken more
      current_holders: Math.floor(Math.random() * 3) + 1,
      average_duration: Math.floor(Math.random() * 10) + 7 // 7-17 days
    })).sort((a, b) => b.times_taken - a.times_taken)

    setDailyTrends(dailyData)
    setMonthlyTrends(monthlyData)
    setPopularBooks(popularBooksData)
  }

  // Call generateTrendData when books data is loaded
  useEffect(() => {
    if (books.length > 0) {
      generateTrendData()
    }
  }, [books])

  const handleLogout = () => {
    localStorage.removeItem('employee')
    navigate('/login')
  }

  const openModal = (type, item = null) => {
    setModalType(type)
    setEditingItem(item)
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setModalType('')
    setEditingItem(null)
  }

  const showEmployeeDetailsModal = (employee) => {
    setSelectedEmployee(employee)
    setShowEmployeeDetails(true)
  }

  const closeEmployeeDetails = () => {
    setShowEmployeeDetails(false)
    setSelectedEmployee(null)
  }

  const handleSubmit = async (formData) => {
    try {
      setError('')
      setSuccess('')

      if (modalType === 'employee') {
        if (editingItem) {
          await updateEmployee(editingItem.id, formData)
          setSuccess('Employee updated successfully')
        } else {
          await createEmployee(formData)
          setSuccess('Employee created successfully')
        }
      } else if (modalType === 'book') {
        if (editingItem) {
          await updateBook(editingItem.id, formData)
          setSuccess('Book updated successfully')
        } else {
          await createBook(formData)
          setSuccess('Book created successfully')
        }
      }

      closeModal()
      await fetchData()
    } catch (err) {
      setError(err.message || 'Operation failed')
    }
  }

  const handleDelete = async (type, id) => {
    if (!window.confirm('Are you sure you want to delete this item?')) {
      return
    }

    try {
      setError('')
      setSuccess('')

      if (type === 'employee') {
        await deleteEmployee(id)
        setSuccess('Employee deleted successfully')
      } else if (type === 'book') {
        await deleteBook(id)
        setSuccess('Book deleted successfully')
      }

      await fetchData()
    } catch (err) {
      setError(err.message || 'Delete failed')
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  // Chart data
  const departmentChartData = adminData ? {
    labels: Object.keys(adminData.department_stats),
    datasets: [
      {
        label: 'Books Taken',
        data: Object.values(adminData.department_stats).map(dept => dept.books_taken),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Total Employees',
        data: Object.values(adminData.department_stats).map(dept => dept.total_employees),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  } : null

  const bookStatusChartData = adminData ? {
    labels: ['Available', 'Taken'],
    datasets: [
      {
        data: [adminData.book_status.available, adminData.book_status.unavailable],
        backgroundColor: ['#28a745', '#dc3545'],
        borderColor: ['#ffffff', '#ffffff'],
        borderWidth: 3,
        hoverBackgroundColor: ['#34ce57', '#e74c3c'],
        hoverBorderWidth: 4,
      },
    ],
  } : null

  // Language Distribution Chart
  const languageChartData = {
    labels: ['English Books (161)', 'Tamil Books (213)'],
    datasets: [
      {
        data: [161, 213],
        backgroundColor: ['#007bff', '#fd7e14'],
        borderColor: ['#ffffff', '#ffffff'],
        borderWidth: 3,
        hoverBackgroundColor: ['#0056b3', '#e8590c'],
        hoverBorderWidth: 4,
      },
    ],
  }

  // Daily Trends Chart Data
  const dailyTrendsChartData = {
    labels: dailyTrends.map(d => d.day_name),
    datasets: [
      {
        label: 'Books Taken Daily',
        data: dailyTrends.map(d => d.books_taken),
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        fill: true,
      },
    ],
  }

  // Monthly Trends Chart Data
  const monthlyTrendsChartData = {
    labels: monthlyTrends.map(m => m.month),
    datasets: [
      {
        label: 'Books Taken',
        data: monthlyTrends.map(m => m.books_taken),
        backgroundColor: 'rgba(16, 185, 129, 0.6)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 2,
      },
      {
        label: 'Renewals',
        data: monthlyTrends.map(m => m.renewals),
        backgroundColor: 'rgba(245, 158, 11, 0.6)',
        borderColor: 'rgba(245, 158, 11, 1)',
        borderWidth: 2,
      },
      {
        label: 'Returns',
        data: monthlyTrends.map(m => m.returns),
        backgroundColor: 'rgba(239, 68, 68, 0.6)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 2,
      },
    ],
  }

  // Popular Books Chart Data
  const popularBooksChartData = {
    labels: popularBooks.slice(0, 8).map(book => book.title.length > 20 ? book.title.substring(0, 20) + '...' : book.title),
    datasets: [
      {
        label: 'Times Taken',
        data: popularBooks.slice(0, 8).map(book => book.times_taken),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
          '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
        ],
        borderWidth: 2,
      },
    ],
  }

  console.log('Chart data created:', {
    bookStatusChartData: !!bookStatusChartData,
    languageChartData: !!languageChartData,
    dailyTrendsChartData: !!dailyTrendsChartData,
    monthlyTrendsChartData: !!monthlyTrendsChartData,
    popularBooksChartData: !!popularBooksChartData,
    dateWiseChartData: !!dateWiseChartData,
    monthWisePieChartData: !!monthWisePieChartData,
    top5DepartmentsChartData: !!top5DepartmentsChartData,
    dailyTrends: dailyTrends.length,
    monthlyTrends: monthlyTrends.length,
    adminData: !!adminData
  })

  // Employee Activity Chart
  const employeeActivityChartData = adminData ? {
    labels: ['Active Readers', 'Inactive Employees'],
    datasets: [
      {
        data: [
          Object.values(adminData.department_stats || {}).reduce((sum, dept) => sum + (dept.books_taken || 0), 0),
          (adminData.total_employees || 4595) - Object.values(adminData.department_stats || {}).reduce((sum, dept) => sum + (dept.books_taken || 0), 0)
        ],
        backgroundColor: ['#17a2b8', '#6c757d'],
        borderColor: ['#ffffff', '#ffffff'],
        borderWidth: 3,
        hoverBackgroundColor: ['#138496', '#545b62'],
        hoverBorderWidth: 4,
      },
    ],
  } : {
    labels: ['Active Readers', 'Inactive Employees'],
    datasets: [
      {
        data: [245, 4350],
        backgroundColor: ['#17a2b8', '#6c757d'],
        borderColor: ['#ffffff', '#ffffff'],
        borderWidth: 3,
        hoverBackgroundColor: ['#138496', '#545b62'],
        hoverBorderWidth: 4,
      },
    ],
  }

  // Genre Distribution Chart
  const genreChartData = {
    labels: ['Fiction', 'Science Fiction', 'History', 'Poetry', 'Children\'s', 'Technical', 'Religious', 'Others'],
    datasets: [
      {
        data: [85, 45, 38, 42, 35, 28, 55, 46],
        backgroundColor: [
          '#e83e8c', '#6f42c1', '#fd7e14', '#20c997',
          '#ffc107', '#dc3545', '#6610f2', '#28a745'
        ],
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverBorderWidth: 4,
      },
    ],
  }

  // Date-wise Analytics Chart (Last 7 days)
  const dateWiseChartData = {
    labels: dailyTrends.length > 0
      ? dailyTrends.slice(-7).map(d => {
          const date = new Date(d.date)
          return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        })
      : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Books Taken',
        data: dailyTrends.length > 0
          ? dailyTrends.slice(-7).map(d => d.books_taken)
          : [12, 8, 15, 10, 18, 6, 14],
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
          '#9966FF', '#FF9F40', '#FF6384'
        ],
        borderColor: '#ffffff',
        borderWidth: 2,
      },
    ],
  }

  // Month-wise Trends Pie Chart (Last 6 months)
  const monthWisePieChartData = {
    labels: monthlyTrends.length > 0
      ? monthlyTrends.slice(-6).map(m => m.month)
      : ['Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025'],
    datasets: [
      {
        label: 'Books Taken',
        data: monthlyTrends.length > 0
          ? monthlyTrends.slice(-6).map(m => m.books_taken)
          : [180, 220, 195, 240, 210, 185],
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
          '#9966FF', '#FF9F40'
        ],
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverBorderWidth: 4,
      },
    ],
  }

  // Top 5 Departments Chart
  const top5DepartmentsChartData = {
    labels: ['VPP', 'Quality Assurance-Veh', 'Powertrain Plant-1', 'Engineering', 'Administration'],
    datasets: [
      {
        label: 'Books Taken',
        data: [45, 32, 28, 22, 18], // Sample data for top 5 departments
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
        ],
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverBackgroundColor: ['#FF4069', '#2E8BC0', '#FFB84D', '#3BAAAA', '#8A4FFF'],
        hoverBorderWidth: 4,
      },
    ],
  }

  return (
    <div className="enhanced-admin-dashboard">
      <div className="container">
      <div className="dashboard-header">
        <h1 className="dashboard-title">
          Admin Dashboard
          <span className={`connection-status ${connectionStatus}`}>
            {connectionStatus === 'connected' && '🟢'}
            {connectionStatus === 'connecting' && '🟡'}
            {connectionStatus === 'error' && '🔴'}
          </span>
        </h1>
        <div className="header-actions">
          <button
            className="btn btn-success"
            onClick={() => openModal('book')}
            style={{
              marginRight: '1rem',
              fontSize: '16px',
              fontWeight: 'bold',
              padding: '12px 24px',
              boxShadow: '0 4px 15px rgba(40, 167, 69, 0.4)',
              border: '2px solid #28a745',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}
          >
            📚 Add Book
          </button>
          <button
            className="btn btn-info"
            onClick={() => openModal('employee')}
            style={{
              marginRight: '1rem',
              fontSize: '16px',
              fontWeight: 'bold',
              padding: '12px 24px',
              boxShadow: '0 4px 15px rgba(23, 162, 184, 0.4)',
              border: '2px solid #17a2b8',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}
          >
            👥 Add Employee
          </button>
          <button
            className="btn btn-primary"
            onClick={() => navigate('/admin/advanced')}
            style={{ marginRight: '1rem' }}
          >
            📊 Advanced Analytics
          </button>
          <div className="user-info">
            <div className="user-name">Administrator</div>
            <button onClick={handleLogout} className="btn btn-secondary mt-1">
              Logout
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
        </div>
      )}

      <div className="admin-tabs">
        <button
          className={`admin-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`admin-tab ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📊 Analytics
        </button>
        <button
          className={`admin-tab ${activeTab === 'employees' ? 'active' : ''}`}
          onClick={() => setActiveTab('employees')}
        >
          Employees
        </button>
        <button
          className={`admin-tab ${activeTab === 'books' ? 'active' : ''}`}
          onClick={() => setActiveTab('books')}
        >
          Books
        </button>
      </div>

      {activeTab === 'overview' && adminData && (
        <div>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">{adminData.total_books_taken}</div>
              <div className="stat-label">Total Books Taken</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{adminData.employees_with_books}</div>
              <div className="stat-label">Active Readers</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{adminData.book_status.total}</div>
              <div className="stat-label">Total Books</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{adminData.book_status.available}</div>
              <div className="stat-label">Available Books</div>
            </div>
          </div>

          <div className="grid grid-2">
            {departmentChartData && (
              <div className="chart-container">
                <h3 className="chart-title">Department Statistics</h3>
                <Bar
                  data={departmentChartData}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'top',
                      },
                    },
                  }}
                />
              </div>
            )}

            {bookStatusChartData && (
              <div className="chart-container">
                <h3 className="chart-title">📚 Book Status Distribution</h3>
                <div style={{ height: '300px', width: '100%' }}>
                  <Doughnut
                    data={bookStatusChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom',
                          labels: {
                            font: {
                              size: 14,
                              weight: 'bold'
                            },
                            padding: 20
                          }
                        },
                        tooltip: {
                          callbacks: {
                            label: function(context) {
                              const total = context.dataset.data.reduce((a, b) => a + b, 0);
                              const percentage = ((context.parsed * 100) / total).toFixed(1);
                              return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                          }
                        }
                      },
                    }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Additional Statistics Charts */}
          <div className="grid grid-3" style={{ marginTop: '2rem' }}>
            <div className="chart-container">
              <h3 className="chart-title">🌐 Language Distribution</h3>
              <div style={{ height: '300px', width: '100%' }}>
                <Doughnut
                  data={languageChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                        labels: {
                          font: {
                            size: 14,
                            weight: 'bold'
                          },
                          padding: 20
                        }
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed * 100) / total).toFixed(1);
                            return `${context.label}: ${context.parsed} books (${percentage}%)`;
                          }
                        }
                      }
                    },
                  }}
                />
              </div>
            </div>

            <div className="chart-container">
              <h3 className="chart-title">👥 Employee Activity</h3>
              <div style={{ height: '300px', width: '100%' }}>
                <Doughnut
                  data={employeeActivityChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                        labels: {
                          font: {
                            size: 14,
                            weight: 'bold'
                          },
                          padding: 20
                        }
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed * 100) / total).toFixed(1);
                            return `${context.label}: ${context.parsed} employees (${percentage}%)`;
                          }
                        }
                      }
                    },
                  }}
                />
              </div>
            </div>

            <div className="chart-container">
              <h3 className="chart-title">📖 Genre Distribution</h3>
              <div style={{ height: '300px', width: '100%' }}>
                <Doughnut
                  data={genreChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                        labels: {
                          font: {
                            size: 12,
                            weight: 'bold'
                          },
                          padding: 15
                        }
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed * 100) / total).toFixed(1);
                            return `${context.label}: ${context.parsed} books (${percentage}%)`;
                          }
                        }
                      }
                    },
                  }}
                />
              </div>
            </div>
          </div>

          {/* Date-wise and Top Departments Analytics */}
          <div className="grid grid-2" style={{ marginTop: '2rem' }}>
            <div className="chart-container">
              <h3 className="chart-title">📅 Date-wise Book Taking (Last 7 Days)</h3>
              <div style={{ height: '300px', width: '100%' }}>
                <Doughnut
                  data={dateWiseChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                        labels: {
                          font: {
                            size: 14,
                            weight: 'bold'
                          },
                          padding: 20,
                          usePointStyle: true
                        }
                      },
                      tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        callbacks: {
                          label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed * 100) / total).toFixed(1);
                            return `${context.label}: ${context.parsed} books (${percentage}%)`;
                          }
                        }
                      }
                    },
                  }}
                />
              </div>
            </div>

            <div className="chart-container">
              <h3 className="chart-title">🏆 Top 5 Departments Performance</h3>
              <div style={{ height: '300px', width: '100%' }}>
                <Doughnut
                  data={top5DepartmentsChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                        labels: {
                          font: {
                            size: 12,
                            weight: 'bold'
                          },
                          padding: 15,
                          usePointStyle: true
                        }
                      },
                      tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        callbacks: {
                          label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed * 100) / total).toFixed(1);
                            return `${context.label}: ${context.parsed} books (${percentage}%)`;
                          }
                        }
                      }
                    },
                  }}
                />
              </div>
            </div>

            {/* Pie Charts Section */}
            <div style={{ marginTop: '3rem' }}>
              <h2 style={{ textAlign: 'center', color: '#2d3748', marginBottom: '2rem', fontSize: '1.8rem' }}>
                🥧 Comprehensive Statistics - Pie Charts
              </h2>
              <div className="grid grid-2" style={{ gap: '2rem' }}>
                <div className="chart-container">
                  <h3 className="chart-title">📚 Books by Language (Pie Chart)</h3>
                  <div style={{ height: '350px', width: '100%' }}>
                    <Pie
                      data={languageChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom',
                            labels: {
                              font: {
                                size: 14,
                                weight: 'bold'
                              },
                              padding: 20
                            }
                          },
                          tooltip: {
                            callbacks: {
                              label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return `${context.label}: ${context.parsed} books (${percentage}%)`;
                              }
                            }
                          }
                        },
                      }}
                    />
                  </div>
                </div>

                <div className="chart-container">
                  <h3 className="chart-title">📖 Genre Distribution (Pie Chart)</h3>
                  <div style={{ height: '350px', width: '100%' }}>
                    <Pie
                      data={genreChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom',
                            labels: {
                              font: {
                                size: 12,
                                weight: 'bold'
                              },
                              padding: 15
                            }
                          },
                          tooltip: {
                            callbacks: {
                              label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return `${context.label}: ${context.parsed} books (${percentage}%)`;
                              }
                            }
                          }
                        },
                      }}
                    />
                  </div>
                </div>
              </div>

              <div className="grid grid-2" style={{ gap: '2rem', marginTop: '2rem' }}>
                <div className="chart-container">
                  <h3 className="chart-title">👥 Employee Activity (Pie Chart)</h3>
                  <div style={{ height: '350px', width: '100%' }}>
                    <Pie
                      data={employeeActivityChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom',
                            labels: {
                              font: {
                                size: 14,
                                weight: 'bold'
                              },
                              padding: 20
                            }
                          },
                          tooltip: {
                            callbacks: {
                              label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return `${context.label}: ${context.parsed} employees (${percentage}%)`;
                              }
                            }
                          }
                        },
                      }}
                    />
                  </div>
                </div>

                <div className="chart-container">
                  <h3 className="chart-title">📅 Date-wise Analytics (Last 7 Days)</h3>
                  <div style={{ height: '350px', width: '100%' }}>
                    <Pie
                      data={dateWiseChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom',
                            labels: {
                              font: {
                                size: 14,
                                weight: 'bold'
                              },
                              padding: 20
                            }
                          },
                          tooltip: {
                            callbacks: {
                              label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return `${context.label}: ${context.parsed} books taken (${percentage}%)`;
                              }
                            }
                          }
                        },
                      }}
                    />
                  </div>
                </div>
              </div>

              {/* Month-wise and Top 5 Departments Section */}
              <div className="grid grid-2" style={{ gap: '2rem', marginTop: '2rem' }}>
                <div className="chart-container">
                  <h3 className="chart-title">📈 Month-wise Trends (Last 6 Months)</h3>
                  <div style={{ height: '350px', width: '100%' }}>
                    <Pie
                      data={monthWisePieChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom',
                            labels: {
                              font: {
                                size: 14,
                                weight: 'bold'
                              },
                              padding: 20,
                              usePointStyle: true
                            }
                          },
                          tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: 'white',
                            bodyColor: 'white',
                            callbacks: {
                              label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return `${context.label}: ${context.parsed} books (${percentage}%)`;
                              }
                            }
                          }
                        },
                      }}
                    />
                  </div>
                </div>

                <div className="chart-container">
                  <h3 className="chart-title">🏆 Top 5 Departments Performance</h3>
                  <div style={{ height: '350px', width: '100%' }}>
                    <Pie
                      data={top5DepartmentsChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom',
                            labels: {
                              font: {
                                size: 12,
                                weight: 'bold'
                              },
                              padding: 15,
                              usePointStyle: true
                            }
                          },
                          tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: 'white',
                            bodyColor: 'white',
                            callbacks: {
                              label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return `${context.label}: ${context.parsed} books (${percentage}%)`;
                              }
                            }
                          }
                        },
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="stats-summary">
              <h3 className="chart-title">📊 Library Statistics Summary</h3>
              <div className="summary-grid">
                <div className="summary-item">
                  <div className="summary-number">374</div>
                  <div className="summary-label">Total Books</div>
                </div>
                <div className="summary-item">
                  <div className="summary-number">4,595</div>
                  <div className="summary-label">Total Employees</div>
                </div>
                <div className="summary-item">
                  <div className="summary-number">161</div>
                  <div className="summary-label">English Books</div>
                </div>
                <div className="summary-item">
                  <div className="summary-number">213</div>
                  <div className="summary-label">Tamil Books</div>
                </div>
                <div className="summary-item">
                  <div className="summary-number">{adminData ? adminData.book_status.available : '---'}</div>
                  <div className="summary-label">Available Books</div>
                </div>
                <div className="summary-item">
                  <div className="summary-number">{adminData ? adminData.book_status.unavailable : '---'}</div>
                  <div className="summary-label">Books Taken</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'analytics' && (
        <div className="analytics-section">
          <div className="card">
            <h2 style={{ textAlign: 'center', color: '#2d3748', marginBottom: '2rem', fontSize: '2rem' }}>
              📊 Comprehensive Library Analytics
            </h2>

            {/* Daily Trends Section */}
            <div style={{ marginBottom: '3rem' }}>
              <h3 style={{ textAlign: 'center', color: '#1e40af', marginBottom: '2rem', fontSize: '1.5rem' }}>
                📅 Daily Book Taking Trends (Last 30 Days)
              </h3>
              <div className="chart-container">
                <div style={{ height: '400px', width: '100%' }}>
                  <Bar
                    data={dailyTrendsChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'top',
                          labels: {
                            font: { size: 14, weight: 'bold' },
                            padding: 20
                          }
                        },
                        tooltip: {
                          backgroundColor: 'rgba(0, 0, 0, 0.8)',
                          titleColor: 'white',
                          bodyColor: 'white',
                          borderColor: '#3b82f6',
                          borderWidth: 1
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          title: {
                            display: true,
                            text: 'Number of Books Taken',
                            font: { size: 14, weight: 'bold' }
                          }
                        },
                        x: {
                          title: {
                            display: true,
                            text: 'Days of Week',
                            font: { size: 14, weight: 'bold' }
                          }
                        }
                      }
                    }}
                  />
                </div>
              </div>
            </div>

            {/* Monthly Trends Section */}
            <div style={{ marginBottom: '3rem' }}>
              <h3 style={{ textAlign: 'center', color: '#1e40af', marginBottom: '2rem', fontSize: '1.5rem' }}>
                📈 Monthly Book Activity Trends (Last 12 Months)
              </h3>
              <div className="chart-container">
                <div style={{ height: '400px', width: '100%' }}>
                  <Bar
                    data={monthlyTrendsChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'top',
                          labels: {
                            font: { size: 14, weight: 'bold' },
                            padding: 20
                          }
                        },
                        tooltip: {
                          backgroundColor: 'rgba(0, 0, 0, 0.8)',
                          titleColor: 'white',
                          bodyColor: 'white',
                          borderColor: '#10b981',
                          borderWidth: 1
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          title: {
                            display: true,
                            text: 'Number of Books',
                            font: { size: 14, weight: 'bold' }
                          }
                        },
                        x: {
                          title: {
                            display: true,
                            text: 'Months',
                            font: { size: 14, weight: 'bold' }
                          }
                        }
                      }
                    }}
                  />
                </div>
              </div>
            </div>

            {/* Most Popular Books Section */}
            <div style={{ marginBottom: '3rem' }}>
              <h3 style={{ textAlign: 'center', color: '#1e40af', marginBottom: '2rem', fontSize: '1.5rem' }}>
                🏆 Most Popular Books (Highest Demand)
              </h3>
              <div className="grid grid-2" style={{ gap: '2rem' }}>
                <div className="chart-container">
                  <h4 className="chart-title">📊 Popular Books Chart</h4>
                  <div style={{ height: '350px', width: '100%' }}>
                    <Pie
                      data={popularBooksChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'right',
                            labels: {
                              font: { size: 12, weight: 'bold' },
                              padding: 15,
                              usePointStyle: true
                            }
                          },
                          tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: 'white',
                            bodyColor: 'white',
                            callbacks: {
                              label: function(context) {
                                const book = popularBooks[context.dataIndex]
                                return `${book.title}: ${book.times_taken} times taken`
                              }
                            }
                          }
                        }
                      }}
                    />
                  </div>
                </div>

                <div className="popular-books-list">
                  <h4 style={{ color: '#1e40af', marginBottom: '1rem', fontSize: '1.2rem' }}>📚 Top 10 Popular Books</h4>
                  <div style={{ maxHeight: '350px', overflowY: 'auto' }}>
                    {popularBooks.slice(0, 10).map((book, index) => (
                      <div key={book.id} style={{
                        padding: '12px',
                        margin: '8px 0',
                        background: index < 3 ? 'linear-gradient(135deg, #fef3c7, #fbbf24)' : 'rgba(59, 130, 246, 0.1)',
                        borderRadius: '8px',
                        border: '1px solid rgba(59, 130, 246, 0.2)',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}>
                        <div>
                          <div style={{ fontWeight: 'bold', color: '#1e40af', fontSize: '14px' }}>
                            #{index + 1} {book.title}
                          </div>
                          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>
                            by {book.author} • {book.genre}
                          </div>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ fontWeight: 'bold', color: '#dc2626', fontSize: '16px' }}>
                            {book.times_taken}x
                          </div>
                          <div style={{ fontSize: '11px', color: '#64748b' }}>
                            taken
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Pie Charts Grid */}
            <div className="grid grid-2" style={{ gap: '2rem', marginBottom: '3rem' }}>
              <div className="chart-container">
                <h3 className="chart-title">📚 Books by Language Distribution</h3>
                <div style={{ height: '400px', width: '100%' }}>
                  <Pie
                    data={languageChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom',
                          labels: {
                            font: { size: 14, weight: 'bold' },
                            padding: 20,
                            usePointStyle: true
                          }
                        },
                        tooltip: {
                          callbacks: {
                            label: function(context) {
                              const total = context.dataset.data.reduce((a, b) => a + b, 0);
                              const percentage = ((context.parsed * 100) / total).toFixed(1);
                              return `${context.label}: ${context.parsed} books (${percentage}%)`;
                            }
                          }
                        }
                      }
                    }}
                  />
                </div>
              </div>

              <div className="chart-container">
                <h3 className="chart-title">📖 Genre Distribution</h3>
                <div style={{ height: '400px', width: '100%' }}>
                  <Pie
                    data={genreChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom',
                          labels: {
                            font: { size: 12, weight: 'bold' },
                            padding: 15,
                            usePointStyle: true
                          }
                        },
                        tooltip: {
                          callbacks: {
                            label: function(context) {
                              const total = context.dataset.data.reduce((a, b) => a + b, 0);
                              const percentage = ((context.parsed * 100) / total).toFixed(1);
                              return `${context.label}: ${context.parsed} books (${percentage}%)`;
                            }
                          }
                        }
                      }
                    }}
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-2" style={{ gap: '2rem', marginBottom: '3rem' }}>
              <div className="chart-container">
                <h3 className="chart-title">👥 Employee Activity Status</h3>
                <div style={{ height: '400px', width: '100%' }}>
                  <Pie
                    data={employeeActivityChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom',
                          labels: {
                            font: { size: 14, weight: 'bold' },
                            padding: 20,
                            usePointStyle: true
                          }
                        },
                        tooltip: {
                          callbacks: {
                            label: function(context) {
                              const total = context.dataset.data.reduce((a, b) => a + b, 0);
                              const percentage = ((context.parsed * 100) / total).toFixed(1);
                              return `${context.label}: ${context.parsed} employees (${percentage}%)`;
                            }
                          }
                        }
                      }
                    }}
                  />
                </div>
              </div>

              <div className="chart-container">
                <h3 className="chart-title">📚 Book Status Overview</h3>
                <div style={{ height: '400px', width: '100%' }}>
                  <Pie
                    data={bookStatusChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom',
                          labels: {
                            font: { size: 14, weight: 'bold' },
                            padding: 20,
                            usePointStyle: true
                          }
                        },
                        tooltip: {
                          callbacks: {
                            label: function(context) {
                              const total = context.dataset.data.reduce((a, b) => a + b, 0);
                              const percentage = ((context.parsed * 100) / total).toFixed(1);
                              return `${context.label}: ${context.parsed} books (${percentage}%)`;
                            }
                          }
                        }
                      }
                    }}
                  />
                </div>
              </div>
            </div>

            {/* Analytics Summary */}
            <div className="analytics-summary" style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '2rem',
              borderRadius: '12px',
              marginTop: '2rem'
            }}>
              <h3 style={{ textAlign: 'center', marginBottom: '1.5rem', fontSize: '1.5rem' }}>
                📈 Key Performance Indicators
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>374</div>
                  <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Total Books</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>4,595</div>
                  <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Total Employees</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>
                    {adminData ? adminData.book_status.available : '---'}
                  </div>
                  <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Available Books</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>
                    {adminData ? Math.round((adminData.book_status.available / 374) * 100) : '---'}%
                  </div>
                  <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Availability Rate</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'employees' && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>Employees Management</h2>
            <button
              onClick={() => openModal('employee')}
              className="btn btn-primary"
            >
              Add Employee
            </button>
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
                {employees.map((employee) => (
                  <tr key={employee.id}>
                    <td>{employee.employee_id || employee.id}</td>
                    <td className="employee-name-cell">
                      <strong
                        onClick={() => showEmployeeDetailsModal(employee)}
                        style={{
                          cursor: 'pointer',
                          color: '#1e40af',
                          fontWeight: 'bold',
                          textDecoration: 'underline'
                        }}
                      >
                        {employee.name}
                      </strong>
                    </td>
                    <td>{employee.department}</td>
                    <td>{employee.email || 'N/A'}</td>
                    <td>{employee.books_taken || 0} books</td>
                    <td>
                      <span className="status-badge available">Active</span>
                    </td>
                    <td>
                    <button
                      onClick={() => openModal('employee', employee)}
                      className="btn btn-secondary"
                      style={{ marginRight: '0.5rem' }}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete('employee', employee.id)}
                      className="btn btn-danger"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'books' && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>Books Management</h2>
            <button
              onClick={() => openModal('book')}
              className="btn btn-primary"
            >
              Add Book
            </button>
          </div>

          <div className="books-table">
            <table>
              <thead>
                <tr>
                  <th>Book ID</th>
                  <th>Title</th>
                  <th>Author</th>
                  <th>Genre</th>
                  <th>Language</th>
                  <th>Rack</th>
                  <th>Status</th>
                  <th>Taken By</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {books.map((book) => (
                  <tr key={book.id}>
                    <td>{book.id}</td>
                    <td className="book-title">{book.title}</td>
                    <td className="book-author">{book.author || 'N/A'}</td>
                    <td className="book-genre">{book.genre || 'N/A'}</td>
                    <td>{book.language || 'English'}</td>
                    <td>{book.rack_no || 'N/A'}</td>
                    <td>
                      <span className={`status-badge ${book.status === 'available' ? 'available' : 'taken'}`}>
                        {book.status}
                      </span>
                    </td>
                    <td>{book.taken_by || '-'}</td>
                    <td>
                    <button
                      onClick={() => openModal('book', book)}
                      className="btn btn-secondary"
                      style={{ marginRight: '0.5rem' }}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete('book', book.id)}
                      className="btn btn-danger"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {showModal && (
        <Modal
          type={modalType}
          item={editingItem}
          onSubmit={handleSubmit}
          onClose={closeModal}
        />
      )}

      {showEmployeeDetails && selectedEmployee && (
        <EmployeeDetailsModal
          employee={selectedEmployee}
          onClose={closeEmployeeDetails}
        />
      )}
      </div>
    </div>
  )
}

// Modal Component
const Modal = ({ type, item, onSubmit, onClose }) => {
  const [formData, setFormData] = useState(
    item || (type === 'employee' 
      ? { username: '', dob: '', name: '', department: '' }
      : { title: '', author: '', isbn: '', status: 'available' })
  )

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h3 className="modal-title">
            {item ? `Edit ${type}` : `Add ${type}`}
          </h3>
          <button onClick={onClose} className="close-btn">×</button>
        </div>

        <form onSubmit={handleSubmit}>
          {type === 'employee' ? (
            <>
              <div className="form-group">
                <label className="form-label">Username</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Department</label>
                <input
                  type="text"
                  name="department"
                  value={formData.department}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Date of Birth</label>
                <input
                  type="date"
                  name="dob"
                  value={formData.dob}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              </div>
            </>
          ) : (
            <>
              <div className="form-group">
                <label className="form-label">Title</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Author</label>
                <input
                  type="text"
                  name="author"
                  value={formData.author || ''}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <label className="form-label">ISBN</label>
                <input
                  type="text"
                  name="isbn"
                  value={formData.isbn || ''}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  className="form-input"
                  required
                >
                  <option value="available">Available</option>
                  <option value="unavailable">Unavailable</option>
                </select>
              </div>
            </>
          )}

          <div className="form-actions">
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {item ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// Employee Details Modal Component
const EmployeeDetailsModal = ({ employee, onClose }) => {
  return (
    <div className="modal-overlay">
      <div className="modal" style={{ maxWidth: '600px' }}>
        <div className="modal-header">
          <h3 className="modal-title">👤 Employee Details</h3>
          <button onClick={onClose} className="close-btn">×</button>
        </div>
        <div className="modal-body">
          <div className="employee-details-grid" style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '1rem',
            marginBottom: '1rem'
          }}>
            <div className="detail-item">
              <strong>Employee ID:</strong>
              <p>{employee.emp_id || employee.id}</p>
            </div>
            <div className="detail-item">
              <strong>Name:</strong>
              <p style={{ fontWeight: 'bold', color: '#000' }}>{employee.name}</p>
            </div>
            <div className="detail-item">
              <strong>Username:</strong>
              <p>{employee.username}</p>
            </div>
            <div className="detail-item">
              <strong>Department:</strong>
              <p>{employee.department}</p>
            </div>
            <div className="detail-item">
              <strong>Email:</strong>
              <p>{employee.mail || employee.email || 'N/A'}</p>
            </div>
            <div className="detail-item">
              <strong>Date of Birth:</strong>
              <p>{employee.dob}</p>
            </div>
            <div className="detail-item">
              <strong>Phone:</strong>
              <p>{employee.phone || 'N/A'}</p>
            </div>
            <div className="detail-item">
              <strong>Books Taken:</strong>
              <p>{employee.books_taken || 0}</p>
            </div>
          </div>

          <div className="employee-stats" style={{
            background: '#f8f9fa',
            padding: '1rem',
            borderRadius: '8px',
            marginTop: '1rem'
          }}>
            <h4 style={{ margin: '0 0 0.5rem 0', color: '#495057' }}>📊 Activity Summary</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#007bff' }}>
                  {employee.books_taken || 0}
                </div>
                <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>Books Taken</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#28a745' }}>
                  {employee.books_returned || 0}
                </div>
                <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>Books Returned</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#dc3545' }}>
                  {employee.overdue_books || 0}
                </div>
                <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>Overdue Books</div>
              </div>
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button onClick={onClose} className="btn btn-secondary">Close</button>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
