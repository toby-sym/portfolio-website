<script>
  import Home from './pages/Home.svelte'
  import Projects from './pages/Projects.svelte'
  import AdminLogin from './pages/AdminLogin.svelte'
  import AdminDashboard from './pages/AdminDashboard.svelte'
  import Contact from './pages/Contact.svelte'
  import { writable } from 'svelte/store'

  export let page = writable('home')
  export let isAuthenticated = writable(false)

  // Check if user is already logged in
  if (localStorage.getItem('auth_token')) {
    isAuthenticated.set(true)
  }

  function handleNavigation(newPage) {
    page.set(newPage)
  }

  function handleLogout() {
    localStorage.removeItem('auth_token')
    isAuthenticated.set(false)
    page.set('home')
  }
</script>

<header>
  <h1>Toby Symons</h1>
  <p>Computer Science student passionate about software engineering, web development, and problem solving.</p>
</header>

<nav>
  <a href="#/" on:click|preventDefault={() => handleNavigation('home')}>
    Home
  </a>
  <a href="#/projects" on:click|preventDefault={() => handleNavigation('projects')}>
    Projects
  </a>
  <a href="#/contact" on:click|preventDefault={() => handleNavigation('contact')}>
    Contact
  </a>
  {#if $isAuthenticated}
    <a href="#/admin" on:click|preventDefault={() => handleNavigation('admin')}>
      Admin
    </a>
    <a href="#/" on:click|preventDefault={handleLogout}>
      Logout
    </a>
  {:else}
    <a href="#/login" on:click|preventDefault={() => handleNavigation('login')}>
      Admin Login
    </a>
  {/if}
</nav>

<main>
  {#if $page === 'home'}
    <Home />
  {:else if $page === 'projects'}
    <Projects />
  {:else if $page === 'contact'}
    <Contact />
  {:else if $page === 'login'}
    <AdminLogin on:authenticated={() => {
      isAuthenticated.set(true)
      page.set('admin')
    }} />
  {:else if $page === 'admin'}
    {#if $isAuthenticated}
      <AdminDashboard />
    {:else}
      <AdminLogin on:authenticated={() => {
        isAuthenticated.set(true)
        page.set('admin')
      }} />
    {/if}
  {/if}
</main>

<footer>
  <p>&copy; 2026 Toby Symons</p>
</footer>

<style>
  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  :global(body) {
    font-family: 'Inter', sans-serif;
    background-color: #f5f5f4;
    color: #334155;
  }

  :global(#app) {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  header {
    background-color: #f5f5f4;
    padding: 2rem 1rem 1.5rem;
    text-align: center;
    border-bottom: 1px solid #e2e8f0;
  }

  header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #475569;
  }

  header p {
    font-size: 1.1rem;
    max-width: 640px;
    margin: 0 auto;
    color: #64748b;
  }

  nav {
    display: flex;
    justify-content: center;
    gap: 3rem;
    padding: 0.75rem 0;
    background-color: #f5f5f4;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    font-weight: 600;
    font-size: 1rem;
    flex-wrap: wrap;
  }

  nav a {
    color: #334155;
    text-decoration: none;
    transition: color 0.3s ease;
    cursor: pointer;
  }

  nav a:hover {
    color: #0f172a;
  }

  main {
    flex: 1;
    max-width: 1000px;
    margin: 0 auto;
    width: 100%;
    padding: 2rem 1rem;
  }

  footer {
    text-align: center;
    background-color: #f5f5f4;
    padding: 1.5rem;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
  }

  @media (max-width: 640px) {
    header h1 {
      font-size: 1.875rem;
    }

    nav {
      gap: 1.5rem;
    }

    main {
      padding: 1rem;
    }
  }
</style>
