import { useState } from 'react';
import axios from 'axios';
import './Login.css';

const API_BASE = import.meta.env.VITE_API_BASE;

import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPwd, setShowPwd] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);
    setError('');
    try {
      const res = await axios.post(`${API_BASE}/api/auth/login/`, {
        email,
        password,
      });
      // on success redirect
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
      finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Please login to your account</h2>
        <form onSubmit={handleSubmit}>
        
        <div className="field">
            <label>Email</label>
        <input
              type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        </div>
          <div className="field password-field">
            <label>Password</label>
        
          <input
            type={showPwd ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <span className="password-toggle" onClick={() => setShowPwd(!showPwd)}>
            {showPwd ? '🙈' : '👁️'}
          </span>
        </div>
        {error && <p className="error">{error}</p>}
        <button className="btn-primary" type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Log in'}</button>
        <div className="links">
          <a href="#">Forgot password?</a>
        </div>
      </form>
      <div className="links" style={{justifyContent:'center',gap:'6px'}}>
        <span>Don't have an account?</span>
        <a href="#">Create new</a>
      </div>
      </div>
    </div>
  );
}
