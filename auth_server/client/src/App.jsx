import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Login from '@routes/login/Login'
import Register from '@routes/register/Register'
import ForgotPassword from '@routes/forgot_password/ForgotPassword'
import ChangePasswordWithRecoverLink from '@routes/change_password_with_recover_link/ChangePasswordWithRecoverLink'
import 'bootstrap/dist/css/bootstrap.min.css';
import '@styles/index.css'
function App() {

  return (
    <>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot_password" element={<ForgotPassword />} />
        <Route path="/change_password_with_recover_link" element={<ChangePasswordWithRecoverLink />} />
        <Route path="/authorize" element="authorize todo"/>
      </Routes>
    </>
  )
}

export default App
