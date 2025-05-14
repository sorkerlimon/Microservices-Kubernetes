import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllUsers, logoutUser } from './api';
import { cleanCache } from './cacheService';
import KafkaNotifications from './KafkaNotifications';
import './App.css';

function getInitials(name) {
  return name
    ? name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
    : '?';
}

export default function Dashboard({ user, setUser }) {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('users');
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedUser, setExpandedUser] = useState(null);
  const [showKafkaStream, setShowKafkaStream] = useState(false);

  useEffect(() => {
    // Fetch users when component mounts
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setIsLoading(true);
      const userData = await getAllUsers();
      
      // Format user data to include details
      const formattedUsers = userData.map(user => ({
        id: user.id,
        name: user.details?.name || 'Unknown',
        email: user.email,
        phone: user.details?.phone || 'N/A'
      }));
      
      setUsers(formattedUsers);
      setError('');
    } catch (err) {
      console.error('Failed to fetch users:', err);
      setError('Failed to load users. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    // Clear user-specific cache on logout
    cleanCache();
    logoutUser();
    setUser(null);
    navigate('/login');
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredUsers = users.filter(user => 
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.phone.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleUserExpand = (userId) => {
    setExpandedUser(expandedUser === userId ? null : userId);
  };

  const toggleKafkaStream = () => {
    setShowKafkaStream(!showKafkaStream);
  };

  return (
    <div className="kubdash-layout">
      {/* Sidebar */}
      <aside className="kubdash-sidebar">
        <div className="kubdash-logo">
          <div className="logo-square">K</div>
          <div className="logo-text">KubDash</div>
        </div>
        
        <div className="kubdash-menu">
          <button 
            className={`menu-item ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            <span className="menu-icon">👥</span>
            <span className="menu-text">Users</span>
          </button>
          
          <button 
            className={`menu-item ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            <span className="menu-icon">⚙️</span>
            <span className="menu-text">Settings</span>
          </button>
          
          <button 
            className={`menu-item ${activeTab === 'reports' ? 'active' : ''}`}
            onClick={() => setActiveTab('reports')}
          >
            <span className="menu-icon">📊</span>
            <span className="menu-text">Reports</span>
          </button>
          
          <button 
            className={`menu-item ${activeTab === 'kafka' ? 'active' : ''}`}
            onClick={() => setActiveTab('kafka')}
          >
            <span className="menu-icon">📡</span>
            <span className="menu-text">Kafka Events</span>
          </button>
          
          <button 
            className="menu-item logout-button"
            onClick={handleLogout}
          >
            <span className="menu-icon">🚪</span>
            <span className="menu-text">Logout</span>
          </button>
        </div>
        
        <div className="kubdash-user-profile">
          <div className="user-initials">{getInitials(user?.name || "")}</div>
          <div className="user-info">
            <div className="user-name">{user?.name || "User"}</div>
            <button 
              className="logout-link" 
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="kubdash-main">
        <header className="kubdash-header">
          <h1 className="kubdash-title">
            {activeTab === 'users' && 'User Management'}
            {activeTab === 'settings' && 'Settings'}
            {activeTab === 'reports' && 'Reports'}
            {activeTab === 'kafka' && 'Kafka Event Stream'}
          </h1>
          
          <div className="header-controls">
            {activeTab === 'users' && (
              <div className="kubdash-search">
                <input 
                  type="text" 
                  placeholder="Search users..." 
                  value={searchTerm}
                  onChange={handleSearch}
                />
                <span className="search-icon">🔍</span>
              </div>
            )}
            
            {activeTab === 'kafka' && (
              <button 
                className="stream-toggle-button" 
                onClick={toggleKafkaStream}
              >
                {showKafkaStream ? 'Hide Stream' : 'Show Stream'}
              </button>
            )}
            
            <button 
              className="logout-button-header" 
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        </header>
        
        {activeTab === 'users' && (
          <div className="user-content">
            {error && <div className="error-message">{error}</div>}
            
            {isLoading ? (
              <div className="loading-message">Loading users...</div>
            ) : (
              <div className="user-table">
                <div className="table-header">
                  <div className="header-cell user-cell">User</div>
                  <div className="header-cell email-cell">Email</div>
                  <div className="header-cell phone-cell">Phone</div>
                  <div className="header-cell actions-cell">Actions</div>
                </div>
                
                <div className="table-body">
                  {filteredUsers.length > 0 ? (
                    filteredUsers.map((user) => (
                      <div key={user.id} className="user-entry">
                        <div 
                          className={`table-row ${expandedUser === user.id ? 'expanded' : ''}`} 
                          onClick={() => toggleUserExpand(user.id)}
                        >
                          <div className="cell user-cell">{user.name}</div>
                          <div className="cell email-cell">{user.email}</div>
                          <div className="cell phone-cell">{user.phone}</div>
                          <div className="cell actions-cell">
                            <button className="action-button">
                              {expandedUser === user.id ? '▲' : '▼'}
                            </button>
                          </div>
                        </div>
                        
                        {expandedUser === user.id && (
                          <div className="user-details">
                            <div className="detail-row">
                              <div className="detail-label">Name:</div>
                              <div className="detail-value">{user.name}</div>
                            </div>
                            <div className="detail-row">
                              <div className="detail-label">Email:</div>
                              <div className="detail-value">{user.email}</div>
                            </div>
                            <div className="detail-row">
                              <div className="detail-label">Phone:</div>
                              <div className="detail-value">{user.phone}</div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="no-users-message">
                      No users found. {searchTerm && 'Try adjusting your search.'}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
        
        {activeTab === 'settings' && (
          <div className="placeholder-content">
            <h2>Settings</h2>
            <p>This section is under development.</p>
          </div>
        )}
        
        {activeTab === 'reports' && (
          <div className="placeholder-content">
            <h2>Reports</h2>
            <p>This section is under development.</p>
          </div>
        )}
        
        {activeTab === 'kafka' && (
          <div className="kafka-content">
            <div className="kafka-info">
              <h2>Kafka Event Monitoring</h2>
              <p>This panel shows real-time Kafka events happening in the system.</p>
              <p>When users register or update their profiles, events are published to Kafka and processed asynchronously.</p>
              <p>The event stream below shows both the original events and their processing results.</p>
            </div>
            <KafkaNotifications />
          </div>
        )}
      </main>
    </div>
  );
}

