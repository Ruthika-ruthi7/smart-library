import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
} from 'chart.js';
import { Line, Doughnut, Bar } from 'react-chartjs-2';
import './AdvancedAdminDashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
);

const AdvancedAdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [monthlyTrends, setMonthlyTrends] = useState(null);
  const [genreDistribution, setGenreDistribution] = useState(null);
  const [languageDistribution, setLanguageDistribution] = useState(null);
  const [dailyActivity, setDailyActivity] = useState(null);
  const [overdueBooks, setOverdueBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchAllData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchAllData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [
        statsRes,
        trendsRes,
        genreRes,
        langRes,
        activityRes,
        overdueRes
      ] = await Promise.all([
        fetch('http://localhost:5000/api/admin/real-time-stats'),
        fetch('http://localhost:5000/api/admin/charts/monthly-trends'),
        fetch('http://localhost:5000/api/admin/charts/genre-distribution'),
        fetch('http://localhost:5000/api/admin/charts/language-distribution'),
        fetch('http://localhost:5000/api/admin/charts/daily-activity'),
        fetch('http://localhost:5000/api/admin/overdue-books')
      ]);

      const [
        statsData,
        trendsData,
        genreData,
        langData,
        activityData,
        overdueData
      ] = await Promise.all([
        statsRes.json(),
        trendsRes.json(),
        genreRes.json(),
        langRes.json(),
        activityRes.json(),
        overdueRes.json()
      ]);

      setStats(statsData.stats);
      setMonthlyTrends(trendsData.data);
      setGenreDistribution(genreData.data);
      setLanguageDistribution(langData.data);
      setDailyActivity(activityData.data);
      setOverdueBooks(overdueData.overdue_books || []);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const monthlyTrendsChartData = monthlyTrends ? {
    labels: monthlyTrends.months,
    datasets: [
      {
        label: 'Books Taken',
        data: monthlyTrends.books_taken,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true
      },
      {
        label: 'Books Returned',
        data: monthlyTrends.books_returned,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  } : null;

  const genreChartData = genreDistribution ? {
    labels: genreDistribution.labels,
    datasets: [{
      data: genreDistribution.data,
      backgroundColor: [
        '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6',
        '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1'
      ],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  } : null;

  const languageChartData = languageDistribution ? {
    labels: languageDistribution.labels,
    datasets: [{
      data: languageDistribution.data,
      backgroundColor: ['#3b82f6', '#ef4444'],
      borderWidth: 3,
      borderColor: '#ffffff'
    }]
  } : null;

  const dailyActivityChartData = dailyActivity ? {
    labels: dailyActivity.days,
    datasets: [{
      label: 'Daily Activity',
      data: dailyActivity.activity,
      backgroundColor: 'rgba(59, 130, 246, 0.8)',
      borderColor: '#3b82f6',
      borderWidth: 2,
      borderRadius: 8
    }]
  } : null;

  if (loading) {
    return (
      <div className="advanced-admin-dashboard">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading Advanced Analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="advanced-admin-dashboard">
      <div className="dashboard-header">
        <h1>📊 Advanced Admin Dashboard</h1>
        <div className="header-stats">
          <div className="stat-badge">
            <span className="stat-number">{stats?.total_books || 0}</span>
            <span className="stat-label">Total Books</span>
          </div>
          <div className="stat-badge">
            <span className="stat-number">{stats?.taken_books || 0}</span>
            <span className="stat-label">Books Taken</span>
          </div>
          <div className="stat-badge">
            <span className="stat-number">{stats?.active_readers || 0}</span>
            <span className="stat-label">Active Readers</span>
          </div>
          <div className="stat-badge">
            <span className="stat-number">{overdueBooks.length}</span>
            <span className="stat-label">Overdue Books</span>
          </div>
        </div>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📈 Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📊 Analytics
        </button>
        <button 
          className={`tab-button ${activeTab === 'overdue' ? 'active' : ''}`}
          onClick={() => setActiveTab('overdue')}
        >
          ⚠️ Overdue Books
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="overview-tab">
          <div className="stats-grid">
            <div className="stat-card">
              <h3>📚 Library Collection</h3>
              <div className="stat-details">
                <div className="stat-row">
                  <span>Total Books:</span>
                  <span className="stat-value">{stats?.total_books || 0}</span>
                </div>
                <div className="stat-row">
                  <span>English Books:</span>
                  <span className="stat-value">{stats?.english_books || 0}</span>
                </div>
                <div className="stat-row">
                  <span>Tamil Books:</span>
                  <span className="stat-value">{stats?.tamil_books || 0}</span>
                </div>
                <div className="stat-row">
                  <span>Available:</span>
                  <span className="stat-value available">{stats?.available_books || 0}</span>
                </div>
                <div className="stat-row">
                  <span>Currently Taken:</span>
                  <span className="stat-value taken">{stats?.taken_books || 0}</span>
                </div>
              </div>
            </div>

            <div className="stat-card">
              <h3>👥 Employee Statistics</h3>
              <div className="stat-details">
                <div className="stat-row">
                  <span>Total Employees:</span>
                  <span className="stat-value">{stats?.total_employees || 0}</span>
                </div>
                <div className="stat-row">
                  <span>Active Readers:</span>
                  <span className="stat-value">{stats?.active_readers || 0}</span>
                </div>
                <div className="stat-row">
                  <span>Reading Rate:</span>
                  <span className="stat-value">
                    {stats?.total_employees ? 
                      ((stats.active_readers / stats.total_employees) * 100).toFixed(1) + '%' 
                      : '0%'}
                  </span>
                </div>
              </div>
            </div>

            <div className="chart-card">
              <h3>📊 Language Distribution</h3>
              {languageChartData && (
                <div className="chart-container small">
                  <Doughnut 
                    data={languageChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom'
                        }
                      }
                    }}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'analytics' && (
        <div className="analytics-tab">
          <div className="charts-grid">
            <div className="chart-card large">
              <h3>📈 Monthly Trends</h3>
              {monthlyTrendsChartData && (
                <div className="chart-container">
                  <Line 
                    data={monthlyTrendsChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'top'
                        },
                        title: {
                          display: true,
                          text: 'Book Borrowing Trends (Last 12 Months)'
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: true
                        }
                      }
                    }}
                  />
                </div>
              )}
            </div>

            <div className="chart-card">
              <h3>📚 Genre Distribution</h3>
              {genreChartData && (
                <div className="chart-container">
                  <Doughnut 
                    data={genreChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'right'
                        }
                      }
                    }}
                  />
                </div>
              )}
            </div>

            <div className="chart-card">
              <h3>📅 Daily Activity (Last 7 Days)</h3>
              {dailyActivityChartData && (
                <div className="chart-container">
                  <Bar 
                    data={dailyActivityChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          display: false
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: true
                        }
                      }
                    }}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'overdue' && (
        <div className="overdue-tab">
          <div className="overdue-header">
            <h3>⚠️ Overdue Books ({overdueBooks.length})</h3>
            <button className="refresh-btn" onClick={fetchAllData}>
              🔄 Refresh
            </button>
          </div>
          
          {overdueBooks.length === 0 ? (
            <div className="no-overdue">
              <p>🎉 No overdue books! All books are returned on time.</p>
            </div>
          ) : (
            <div className="overdue-table">
              <table>
                <thead>
                  <tr>
                    <th>Book</th>
                    <th>Employee</th>
                    <th>Department</th>
                    <th>Taken Date</th>
                    <th>Days Overdue</th>
                    <th>Contact</th>
                  </tr>
                </thead>
                <tbody>
                  {overdueBooks.map((item, index) => (
                    <tr key={index}>
                      <td>
                        <div className="book-info">
                          <strong>{item.title}</strong>
                          <small>by {item.author}</small>
                        </div>
                      </td>
                      <td>
                        <div className="employee-info">
                          <strong>{item.employee.name}</strong>
                          <small>ID: {item.employee.emp_id}</small>
                        </div>
                      </td>
                      <td>{item.employee.department}</td>
                      <td>{new Date(item.taken_date).toLocaleDateString()}</td>
                      <td>
                        <span className="overdue-days">
                          {item.days_overdue} days
                        </span>
                      </td>
                      <td>
                        <a href={`mailto:${item.employee.email}`} className="contact-btn">
                          📧 Email
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AdvancedAdminDashboard;
