<script>
  import { onMount } from 'svelte'
  import { api } from '../api'

  let projects = []
  let loading = true
  let error = ''
  let success = ''

  // Form state for new/edit project
  let showForm = false
  let editingId = null
  let formData = {
    title: '',
    description: '',
    technologies: '',
    github_link: '',
    live_link: '',
    featured: false,
  }

  onMount(async () => {
    await fetchProjects()
  })

  async function fetchProjects() {
    try {
      loading = true
      const response = await api.getProjects()
      projects = response.data
      error = ''
    } catch (err) {
      error = 'Failed to load projects'
      console.error(err)
    } finally {
      loading = false
    }
  }

  function openAddForm() {
    editingId = null
    formData = {
      title: '',
      description: '',
      technologies: '',
      github_link: '',
      live_link: '',
      featured: false,
    }
    showForm = true
  }

  function editProject(project) {
    editingId = project.id
    formData = { ...project }
    showForm = true
  }

  function closeForm() {
    showForm = false
    editingId = null
  }

  async function handleSubmit() {
    if (!formData.title || !formData.description || !formData.technologies) {
      error = 'Please fill in all required fields'
      return
    }

    try {
      success = ''
      if (editingId) {
        await api.updateProject(editingId, formData)
        success = 'Project updated successfully!'
      } else {
        await api.createProject(formData)
        success = 'Project created successfully!'
      }
      closeForm()
      await fetchProjects()
      error = ''
    } catch (err) {
      error = err.response?.data?.detail || 'Failed to save project'
      console.error(err)
    }
  }

  async function deleteProject(id) {
    if (!window.confirm('Are you sure you want to delete this project?')) {
      return
    }

    try {
      await api.deleteProject(id)
      success = 'Project deleted successfully!'
      await fetchProjects()
      error = ''
    } catch (err) {
      error = err.response?.data?.detail || 'Failed to delete project'
      console.error(err)
    }
  }
</script>

<section id="admin-dashboard">
  <h2>Admin Dashboard</h2>

  {#if error}
    <div class="alert error">{error}</div>
  {/if}

  {#if success}
    <div class="alert success">{success}</div>
  {/if}

  <button class="btn btn-primary" on:click={openAddForm} disabled={showForm}>
    + Add New Project
  </button>

  {#if showForm}
    <div class="form-container">
      <h3>{editingId ? 'Edit Project' : 'Add New Project'}</h3>

      <form on:submit|preventDefault={handleSubmit}>
        <div class="form-group">
          <label for="title">Title *</label>
          <input
            id="title"
            type="text"
            bind:value={formData.title}
            placeholder="Project title"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description *</label>
          <textarea
            id="description"
            bind:value={formData.description}
            placeholder="Project description"
            rows="4"
            required
          />
        </div>

        <div class="form-group">
          <label for="technologies">Technologies *</label>
          <input
            id="technologies"
            type="text"
            bind:value={formData.technologies}
            placeholder="e.g., Python, FastAPI, PostgreSQL"
            required
          />
        </div>

        <div class="form-group">
          <label for="github_link">GitHub Link</label>
          <input
            id="github_link"
            type="url"
            bind:value={formData.github_link}
            placeholder="https://github.com/..."
          />
        </div>

        <div class="form-group">
          <label for="live_link">Live Link</label>
          <input
            id="live_link"
            type="url"
            bind:value={formData.live_link}
            placeholder="https://..."
          />
        </div>

        <div class="form-group checkbox">
          <input
            id="featured"
            type="checkbox"
            bind:checked={formData.featured}
          />
          <label for="featured">Featured Project</label>
        </div>

        <div class="form-buttons">
          <button type="submit" class="btn btn-primary">
            {editingId ? 'Update' : 'Create'} Project
          </button>
          <button type="button" class="btn btn-secondary" on:click={closeForm}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  {/if}

  <h3>Projects ({projects.length})</h3>

  {#if loading}
    <p>Loading projects...</p>
  {:else if projects.length === 0}
    <p>No projects yet. <button class="link-btn" on:click={openAddForm}>Add your first project!</button></p>
  {:else}
    <div class="projects-list">
      {#each projects as project (project.id)}
        <div class="project-card">
          <h4>{project.title}</h4>
          {#if project.featured}
            <span class="badge featured">Featured</span>
          {/if}
          <p class="description">{project.description}</p>
          <p class="tech">Tech: {project.technologies}</p>
          <div class="project-actions">
            <button class="btn btn-small btn-primary" on:click={() => editProject(project)}>
              Edit
            </button>
            <button class="btn btn-small btn-danger" on:click={() => deleteProject(project.id)}>
              Delete
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</section>

<style>
  section {
    max-width: 800px;
    margin: 0 auto;
  }

  h2 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    color: #0f172a;
  }

  h3 {
    font-size: 1.25rem;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    color: #0f172a;
  }

  h4 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    color: #0f172a;
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

  .alert.success {
    background-color: #dcfce7;
    color: #166534;
    border-left-color: #22c55e;
  }

  .btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.3s ease;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-primary {
    background-color: #0f172a;
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    background-color: #1e293b;
  }

  .btn-secondary {
    background-color: #cbd5e1;
    color: #0f172a;
  }

  .btn-secondary:hover {
    background-color: #94a3b8;
  }

  .btn-small {
    padding: 0.35rem 0.75rem;
    font-size: 0.8rem;
  }

  .btn-danger {
    background-color: #dc2626;
    color: white;
  }

  .btn-danger:hover {
    background-color: #b91c1c;
  }

  .link-btn {
    background: none;
    border: none;
    color: #0f172a;
    text-decoration: underline;
    cursor: pointer;
    font-weight: 600;
  }

  .link-btn:hover {
    color: #1e293b;
  }

  .form-container {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .form-group.checkbox {
    flex-direction: row;
    align-items: center;
  }

  .form-group.checkbox input {
    margin: 0;
    width: auto;
  }

  .form-group.checkbox label {
    margin: 0;
  }

  label {
    font-weight: 600;
    color: #0f172a;
    font-size: 0.9rem;
  }

  input,
  textarea {
    padding: 0.5rem;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    font-size: 0.9rem;
    font-family: inherit;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: #0f172a;
    box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
  }

  .form-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
  }

  .projects-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .project-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
  }

  .project-card h4 {
    margin-bottom: 0.5rem;
  }

  .badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 12px;
    margin-bottom: 0.5rem;
    width: fit-content;
  }

  .badge.featured {
    background-color: #fef3c7;
    color: #92400e;
  }

  .description {
    color: #475569;
    margin-bottom: 0.5rem;
    flex-grow: 1;
    font-size: 0.9rem;
  }

  .tech {
    color: #64748b;
    font-size: 0.8rem;
    margin-bottom: 1rem;
  }

  .project-actions {
    display: flex;
    gap: 0.5rem;
  }

  @media (max-width: 640px) {
    .projects-list {
      grid-template-columns: 1fr;
    }

    .form-buttons {
      flex-direction: column;
    }

    .btn {
      width: 100%;
    }
  }
</style>
