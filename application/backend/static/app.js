const API_BASE = '';

// bcrypt limit: 72 bytes. Truncate so backend never sees longer.
function truncatePasswordTo72Bytes(str) {
  if (!str) return str;
  const encoder = new TextEncoder();
  const bytes = encoder.encode(str);
  if (bytes.length <= 72) return str;
  return new TextDecoder('utf-8', { fatal: false }).decode(bytes.slice(0, 72));
}

const authView = document.getElementById('auth-view');
const welcomeView = document.getElementById('welcome-view');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const messageEl = document.getElementById('message');
const logoutBtn = document.getElementById('logout-btn');
const tabs = document.querySelectorAll('.tab');

function showMessage(text, type) {
  messageEl.textContent = text || '';
  messageEl.className = 'message ' + (type || '');
}

function setLoading(loading) {
  const btn = authView.querySelector('.form:not(.hidden) button[type="submit"]');
  if (btn) {
    btn.disabled = loading;
    btn.textContent = loading ? 'Please wait...' : (registerForm.classList.contains('hidden') ? 'Login' : 'Register');
  }
}

function setToken(token) {
  if (token) localStorage.setItem('token', token);
  else localStorage.removeItem('token');
}

function getToken() {
  return localStorage.getItem('token');
}

function showAuth() {
  authView.classList.remove('hidden');
  welcomeView.classList.add('hidden');
}

function showWelcome() {
  authView.classList.add('hidden');
  welcomeView.classList.remove('hidden');
}

async function checkWelcome() {
  const token = getToken();
  if (!token) {
    showAuth();
    return;
  }
  try {
    const res = await fetch(API_BASE + '/api/welcome', {
      headers: { Authorization: 'Bearer ' + token },
    });
    if (res.ok) {
      const data = await res.json();
      document.querySelector('.welcome-title').textContent = data.message || 'Welcome Kubernetes';
      showWelcome();
    } else {
      setToken(null);
      showAuth();
    }
  } catch {
    setToken(null);
    showAuth();
  }
}

tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((t) => t.classList.remove('active'));
    tab.classList.add('active');
    const which = tab.dataset.tab;
    loginForm.classList.toggle('hidden', which !== 'login');
    registerForm.classList.toggle('hidden', which !== 'register');
    showMessage('');
  });
});

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  showMessage('');
  setLoading(true);
  const fd = new FormData(loginForm);
  const email = fd.get('email');
  const password = truncatePasswordTo72Bytes(String(fd.get('password') || ''));
  try {
    const res = await fetch(API_BASE + '/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      setToken(data.access_token);
      showWelcome();
      document.querySelector('.welcome-title').textContent = 'Welcome Kubernetes';
    } else {
      showMessage(data.detail || 'Login failed', 'error');
    }
  } catch (err) {
    showMessage('Network error', 'error');
  } finally {
    setLoading(false);
  }
});

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  showMessage('');
  setLoading(true);
  const fd = new FormData(registerForm);
  const email = fd.get('email');
  const password = truncatePasswordTo72Bytes(String(fd.get('password') || ''));
  try {
    const res = await fetch(API_BASE + '/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      setToken(data.access_token);
      showWelcome();
      document.querySelector('.welcome-title').textContent = 'Welcome Kubernetes';
    } else {
      showMessage(data.detail || 'Registration failed', 'error');
    }
  } catch (err) {
    showMessage('Network error', 'error');
  } finally {
    setLoading(false);
  }
});

logoutBtn.addEventListener('click', () => {
  setToken(null);
  showAuth();
  showMessage('');
});

checkWelcome();
