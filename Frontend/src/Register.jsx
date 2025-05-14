import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from './api';
import './App.css';

export default function Register({ setUser }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !email || !phone || !password) {
      setError('Please fill in all fields');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const userData = await registerUser({
        name,
        email,
        phone,
        password
      });
      
      // Format the user data to match what the app expects
      const formattedUser = {
        id: userData.id,
        email: userData.email,
        name: userData.details?.name || name,
        phone: userData.details?.phone || phone
      };
      
      setUser(formattedUser);
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration error:', error);
      setError('Registration failed: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={e => setName(e.target.value)}
          disabled={isLoading}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          disabled={isLoading}
        />
        <input
          type="tel"
          placeholder="Phone"
          value={phone}
          onChange={e => setPhone(e.target.value)}
          disabled={isLoading}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          disabled={isLoading}
        />
        {error && <div className="error-msg">{error}</div>}
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p>
        Already have an account? <Link to="/login">Back to Login</Link>
      </p>
    </div>
  );
}
