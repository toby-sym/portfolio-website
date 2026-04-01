<section id="contact">
  <h2>Get In Touch</h2>
  <p>Have a question or want to work together? Feel free to reach out!</p>

  <div class="contact-methods">
    <div class="method">
      <h3>Email</h3>
      <a href="mailto:contact@example.com">contact@example.com</a>
    </div>

    <div class="method">
      <h3>LinkedIn</h3>
      <a href="https://linkedin.com/in/toby-symons" target="_blank" rel="noopener">
        linkedin.com/in/toby-symons
      </a>
    </div>

    <div class="method">
      <h3>GitHub</h3>
      <a href="https://github.com/toby-sym" target="_blank" rel="noopener">
        github.com/toby-sym
      </a>
    </div>
  </div>
</section>

<style>
  section {
    margin: 2rem 0;
  }

  h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #475569;
  }

  section > p {
    font-size: 1.1rem;
    color: #64748b;
    margin-bottom: 2rem;
  }

  .contact-methods {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
  }

  .method {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
  }

  .method h3 {
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
    color: #0f172a;
  }

  .method a {
    color: #0f172a;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s ease;
  }

  .method a:hover {
    color: #475569;
  }

  @media (max-width: 640px) {
    h2 {
      font-size: 1.5rem;
    }

    .contact-methods {
      grid-template-columns: 1fr;
    }
  }
</style>
