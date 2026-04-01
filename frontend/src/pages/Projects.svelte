<script>
  import { onMount } from 'svelte'

  let projects = []
  let loading = true
  let error = null

  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8001/projects')
      if (!response.ok) throw new Error('Failed to fetch projects')
      projects = await response.json()
    } catch (err) {
      error = err.message
      console.error(err)
    } finally {
      loading = false
    }
  })
</script>

<section id="projects">
  <h2>Projects</h2>
  <p>Explore my portfolio of work. Feel free to ask questions or learn more about any project!</p>

  {#if loading}
    <p>Loading projects...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if projects.length === 0}
    <p>No projects yet. Check back soon!</p>
  {:else}
    <div class="timeline">
      {#each projects as project (project.id)}
        <div class="project">
          <h3>{project.title}</h3>
          <p>{project.description}</p>
          <p class="tech">Technologies: {project.technologies}</p>
          {#if project.github_link}
            <a href={project.github_link} target="_blank" rel="noopener">GitHub Repo</a>
          {/if}
          {#if project.live_link}
            <a href={project.live_link} target="_blank" rel="noopener">Live Demo</a>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</section>

<style>
  section {
    margin: 2rem 0;
  }

  h2 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: #475569;
  }

  section > p:first-of-type {
    font-size: 1.1rem;
    color: #64748b;
    margin-bottom: 1.5rem;
  }

  .timeline {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .project {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: box-shadow 0.3s ease;
  }

  .project:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .project h3 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: #0f172a;
  }

  .project p {
    margin-bottom: 0.75rem;
    line-height: 1.6;
  }

  .tech {
    font-size: 0.9rem;
    color: #64748b;
    font-style: italic;
    margin-bottom: 1rem !important;
  }

  .project a {
    display: inline-block;
    margin-right: 1rem;
    padding: 0.5rem 1rem;
    background-color: #0f172a;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 600;
    transition: background-color 0.3s ease;
  }

  .project a:hover {
    background-color: #1e293b;
  }

  .error {
    color: #dc2626;
    background: #fee2e2;
    padding: 1rem;
    border-radius: 4px;
    border-left: 4px solid #dc2626;
  }

  @media (max-width: 640px) {
    h2 {
      font-size: 1.5rem;
    }

    .project {
      padding: 1rem;
    }

    .project h3 {
      font-size: 1.25rem;
    }
  }
</style>
