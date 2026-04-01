# Portfolio Frontend - Svelte SPA

Modern, lightweight single-page application for portfolio website.

## Features

- 🎨 Responsive design with Tailwind CSS principles
- ⚡ Fast, reactive UI built with Svelte
- 🔐 JWT-based admin dashboard
- 📝 Project management interface
- 🚀 Optimized build with Vite

## Tech Stack

- **Framework**: Svelte 4
- **Build Tool**: Vite 5
- **Language**: JavaScript/TypeScript
- **Styling**: CSS-in-JS with Svelte
- **API Client**: Axios

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Server will start at `http://localhost:5173`

### Building

```bash
npm run build
```

Output will be in `dist/` folder.

### Environment Variables

Create a `.env.local` file:

```
VITE_API_URL=http://localhost:8001
```

For production:

```
VITE_API_URL=https://your-api-domain.com
```

## Project Structure

```
src/
├── main.js              # Entry point
├── App.svelte           # Root component
├── api.js               # API client with axios
└── pages/
    ├── Home.svelte      # About/Home page
    ├── Projects.svelte  # Public projects listing
    ├── Contact.svelte   # Contact information
    ├── AdminLogin.svelte      # Admin authentication
    └── AdminDashboard.svelte  # Project CRUD interface
```

## Key Components

### App.svelte
- Main application shell
- Navigation router (hash-based)
- Authentication state management
- Global styling

### Pages

**Home.svelte**
- About section with bio
- Skills and technologies
- Education info

**Projects.svelte**
- Fetches projects from API (`GET /projects`)
- Displays project cards
- Links to GitHub repos and live demos
- Loading and error states

**AdminLogin.svelte**
- Username/password form
- Calls `POST /auth/login`
- Stores JWT token in localStorage
- Emits `authenticated` event

**AdminDashboard.svelte**
- Lists all projects
- Create: `POST /projects`
- Update: `PUT /projects/{id}`
- Delete: `DELETE /projects/{id}`
- Form validation and error handling

### API Module (api.js)

Axios client with:
- Base URL configuration
- Automatic JWT token injection
- Methods for all CRUD operations
- Error handling

## Authentication Flow

1. User enters credentials on AdminLogin page
2. Login request made to `POST /auth/login`
3. JWT token received and stored in `localStorage`
4. Axios interceptor automatically adds token to subsequent requests
5. Admin pages can be accessed
6. Logout clears token and redirects to home

## Building & Deployment

### Static Export

```bash
npm run build
# dist/ folder is ready to deploy
```

### Deployment Options

1. **GitHub Pages**: Push `dist/` folder to `gh-pages` branch
2. **Vercel/Netlify**: Connect repository, auto-deploys to `dist/`
3. **Self-hosted**: Serve content of `dist/` folder with any web server

### For Development Use

```bash
npm run build
npm run preview
# Serves dist/ locally for testing
```

## Notes

- The app uses hash-based routing (`#/home`, `#/projects`, etc.) for simplicity
- API URL must be configured in `.env.local` for backend communication
- LocalStorage is used for JWT token persistence
- CORS must be enabled on backend for requests to work

## Next Steps

- Add project filtering/search
- Implement contact form handling
- Add project images support
- Expand admin features (edit user profiles, analytics)
- Deploy to production

