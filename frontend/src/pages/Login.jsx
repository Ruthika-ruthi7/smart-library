import React from 'react'
import { useNavigate } from 'react-router-dom'
import ProfessionalLogin from '../components/ProfessionalLogin'

const Login = () => {
  const navigate = useNavigate()

  const handleLogin = (employee) => {
    // Store employee data in localStorage
    localStorage.setItem('employee', JSON.stringify(employee))

    // Navigate based on role
    if (employee.role === 'admin') {
      navigate('/admin')
    } else {
      navigate('/employee')
    }
  }

  return <ProfessionalLogin onLogin={handleLogin} />
}

export default Login
