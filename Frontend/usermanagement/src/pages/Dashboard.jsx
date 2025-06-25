import { useState, useEffect } from 'react';
import axios from 'axios';
const API_BASE = import.meta.env.VITE_API_BASE;
import './Dashboard.css';

export default function Dashboard() {
  const [active, setActive] = useState('Dashboard');
  const menu = ['Dashboard', 'Users', 'User Details'];
  const [users, setUsers] = useState([]);
  const [details, setDetails] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const [uRes, dRes] = await Promise.all([
          axios.get(`${API_BASE}/api/users/`),
          axios.get(`${API_BASE}/api/user-details/`),
        ]);
        setUsers(uRes.data);
        setDetails(dRes.data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <h1>Control Panel</h1>
        {menu.map((item) => (
          <div
            key={item}
            className={`nav-item ${active === item ? 'active' : ''}`}
            onClick={() => setActive(item)}
          >
            {item}
          </div>
        ))}
      </aside>

      {/* Main */}
      <main className="main">
        {/* Top metrics */}
        <div className="top-cards">
          <div className="card">
            <span className="label">Bookings</span>
            <span className="value">281</span>
            <span className="label">+55% than last week</span>
          </div>
          <div className="card">
            <span className="label">Today&#39;s Users</span>
            <span className="value">2,300</span>
            <span className="label">+3% than last month</span>
          </div>
          <div className="card">
            <span className="label">Revenue</span>
            <span className="value">$34k</span>
            <span className="label">+11% yesterday</span>
          </div>
          <div className="card">
            <span className="label">Followers</span>
            <span className="value">+91</span>
            <span className="label">just updated</span>
          </div>
        </div>

        {/* Top metrics */}
        <div className="top-cards">
          <div className="card">
            <span className="label">Total Users</span>
            <span className="value">{users.length}</span>
          </div>
          <div className="card">
            <span className="label">Total User Details</span>
            <span className="value">{details.length}</span>
          </div>
        </div>

        {/* Tables */}
        <h3>Users</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Active</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.email}</td>
                <td>{u.is_active ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <h3>User Details</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Phone</th>
            </tr>
          </thead>
          <tbody>
            {details.map((d) => (
              <tr key={d.id}>
                <td>{d.id}</td>
                <td>{d.user}</td>
                <td>{d.first_name}</td>
                <td>{d.last_name}</td>
                <td>{d.phone}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
