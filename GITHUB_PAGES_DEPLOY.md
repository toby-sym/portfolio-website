# Deploy Frontend to GitHub Pages

Your Svelte frontend is ready to deploy! Here's how:

## Step 1: Build Frontend for Production

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized static files ready for GitHub Pages.

## Step 2: Deploy to GitHub Pages

### Option A: Using GitHub CLI (Quickest - 2 minutes)

1. First commit and push your code:
```bash
cd /Users/tobys/portfolio-website
git add frontend/src/api.js RENDER_*.md
git commit -m "feat: Connect frontend to deployed Render backend and update docs"
git push origin main
```

2. Build the frontend:
```bash
cd frontend
npm run build
```

3. Deploy `dist/` folder to GitHub Pages using GitHub CLI:
```bash
# Make sure gh CLI is installed: https://cli.github.com/
gh auth login  # Only needed first time
npx gh-pages -d dist --branch gh-pages
```

Your site will be live at: `https://toby-sym.github.io/portfolio-website`

---

### Option B: Manual GitHub Pages Setup

1. Build frontend:
```bash
cd frontend
npm run build
```

2. Copy contents of `dist/` to `gh-pages` branch:
```bash
cd ..
git checkout -b gh-pages
cp -r frontend/dist/* .
git add .
git commit -m "Deploy frontend to GitHub Pages"
git push origin gh-pages
```

3. Configure GitHub Pages:
   - Go to repo Settings → Pages
   - Set "Branch" to `gh-pages` → Save

---

## Step 3: Verify Deployment

Once deployed, verify your site:
1. Visit: `https://toby-sym.github.io/portfolio-website`
2. Click "Projects" → Should load from deployed backend ✅
3. Click "Admin" → Login with `admin` / `changeme123`
4. Try creating a test project → Should appear in public portfolio

---

## Next: Update Admin Credentials (IMPORTANT)

After first successful login:

1. Change your admin password on Render:
   - Go to Render dashboard
   - Select your service
   - Settings → Environment → ADMIN_PASSWORD
   - Change to a strong password
   - Restart service

2. Change SECRET_KEY for extra security:
```bash
# Generate new key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Update in Render environment
# Then restart service
```

---

## Troubleshooting Frontend

**Admin login fails:** Verify ADMIN_PASSWORD in Render environment matches what you're typing

**Projects don't appear:** Check browser console (F12) for CORS or network errors

**API calls fail:** Ensure `https://portfolio-website-3a8v.onrender.com` is reachable

**Site shows old content:** Clear browser cache (Cmd+Shift+R on Mac)

---

## Your Live Portfolio

| Component | URL | Status |
|-----------|-----|--------|
| **Backend API** | `https://portfolio-website-3a8v.onrender.com` | ✅ Running |
| **Public Portfolio** | `https://toby-sym.github.io/portfolio-website` | ⏳ Deploy now |
| **Admin Panel** | `.../portfolio-website#/admin` | ⏳ Available after frontend deploy |

---

## Final Checklist

- [ ] `npm run build` completes without errors
- [ ] `dist/` folder created with files
- [ ] GitHub Pages deployed (`gh-pages` branch pushed)
- [ ] Portfolio site loads at GitHub Pages URL
- [ ] Projects endpoint works (you should see empty array initially)
- [ ] Admin login works
- [ ] Can create/edit/delete projects via admin panel
- [ ] Projects appear on public portfolio page

---

**Total Time: ~10 minutes to full production deployment!**

Questions? Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for more details on backend setup.
