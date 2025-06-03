import React, { useEffect, useState } from "react";

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Use relative path for API requests when using Ingress
    // In development, you might need the full URL like http://localhost:8000/users
    // In production with Ingress, use /api/users
    fetch("/api/users")
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => {
        console.error("Error fetching users:", err);
        // Set error state to show user
        setUsers([]);
      });
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h2>User List</h2>
      <table border="1" cellPadding="10" cellSpacing="0" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Name</th><th>Email</th><th>Phone</th>
          </tr>
        </thead>
        <tbody>
          {users.length === 0 ? (
            <tr><td colSpan="3" align="center">No users found</td></tr>
          ) : (
            users.map((user, index) => (
              <tr key={index}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.phone}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default UserList;
