import React from 'react';
import './StatusBadge.css';

const StatusBadge = ({ status, text, size = 'medium' }) => {
  const getStatusClass = () => {
    switch (status) {
      case 'available':
        return 'status-success';
      case 'taken':
        return 'status-info';
      case 'overdue':
        return 'status-danger';
      case 'pending':
        return 'status-warning';
      case 'approved':
        return 'status-success';
      case 'rejected':
        return 'status-danger';
      case 'reviewed':
        return 'status-info';
      default:
        return 'status-secondary';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'available':
        return '✓';
      case 'taken':
        return '📖';
      case 'overdue':
        return '⚠️';
      case 'pending':
        return '⏳';
      case 'approved':
        return '✅';
      case 'rejected':
        return '❌';
      case 'reviewed':
        return '👁️';
      default:
        return '●';
    }
  };

  return (
    <span className={`status-badge ${getStatusClass()} status-${size}`}>
      <span className="status-icon">{getStatusIcon()}</span>
      <span className="status-text">{text || status}</span>
    </span>
  );
};

export default StatusBadge;
