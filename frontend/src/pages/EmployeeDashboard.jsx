import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import EnhancedAdminDashboard from '../components/EnhancedAdminDashboard.jsx'
import AdvancedEmployeeDashboard from '../components/AdvancedEmployeeDashboard.jsx'

const EmployeeDashboard = () => {
  const [employee, setEmployee] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const employeeData = localStorage.getItem('employee')
    
    if (!employeeData) {
      navigate('/login')
      return
    }

    try {
      const parsedEmployee = JSON.parse(employeeData)
      setEmployee(parsedEmployee)
    } catch (err) {
      navigate('/login')
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('employee')
    navigate('/login')
  }

  if (!employee) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  // Check if user is admin (System Administrator)
  const isAdmin = employee && (
    employee.role === 'admin' ||
    employee.name === 'System Administrator' ||
    employee.employee_id === 'ADMIN001'
  );

  // If admin, show enhanced admin dashboard
  if (isAdmin) {
    return <EnhancedAdminDashboard employee={employee} onLogout={handleLogout} />
  }

  // For employees, show the advanced employee dashboard with Tamil support
  return <AdvancedEmployeeDashboard employee={employee} onLogout={handleLogout} />
}

export default EmployeeDashboard
