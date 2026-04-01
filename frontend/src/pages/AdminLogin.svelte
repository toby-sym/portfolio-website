<script>
  import { createEventDispatcher } from 'svelte'
  import { api } from '../api'

  const dispatch = createEventDispatcher()

  let username = ''
  let password = ''
  let error = ''
  let loading = false

  async function handleLogin() {
    if (!username || !password) {
      error = 'Please fill in all fields'
      return
    }

    loading = true
    error = ''

    try {
      const response = await api.login({ username, password })
      localStorage.setItem('auth_token', response.data.access_token)
      dispatch('authenticated')
    } catch (err) {
      error = err.response?.data?.detail || 'Login failed. Please check your credentials.'
    } finally {
      loading = false
    }
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter') {
      handleLogin()
    }
  }
</script>

<section id="admin-login">
  <h2>Admin Login</h2>

  {#if error}
    <div class="alert error">{error}</div>
  {/if}

  <form on:submit|preventDefault={handleLogin}>
    <div class="form-group">
      <label for="username">Username</label>
      <input
        id="username"
        type="text"
        bind:value={username}
        on:keypress={handleKeyPress}
        disabled={loading}
        placeholder="Enter your username"
      />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input
        id="password"
        type="password"
        bind:value={password}
        on:keypress={handleKeyPress}
        disabled={loading}
        placeholder="Enter your password"
      />
    </div>

    <button type="submit" disabled={loading}>
      {loading ? 'Logging in...' : 'Login'}
    </button>
  </form>
</section>

<style>
  section {
    max-width: 400px;
    margin: 3rem auto;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  h2 {
    text-align: center;
    margin-bottom: 2rem;
    color: #0f172a;
    font-size: 1.5rem;
  }

  .alert {
    padding: 0.75rem 1rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    border-left: 4px solid;
  }

  .alert.error {
    background-color: #fee2e2;
    color: #991b1b;
    border-left-color: #dc2626;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  label {
    font-weight: 600;
    color: #0f172a;
    font-size: 0.9rem;
  }

  input {
    padding: 0.75rem;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.3s ease;
  }

  input:focus {
    outline: none;
    border-color: #0f172a;
    box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
  }

  input:disabled {
    background-color: #f1f5f9;
    cursor: not-allowed;
  }

  button {
    padding: 0.75rem 1.5rem;
    background-color: #0f172a;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  button:hover:not(:disabled) {
    background-color: #1e293b;
  }

  button:disabled {
    background-color: #cbd5e1;
    cursor: not-allowed;
  }
</style>
