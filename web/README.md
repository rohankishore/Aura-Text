# Aura Text Website

Official website for Aura Text IDE - Built with vanilla HTML, CSS, and JavaScript.

## 📁 Structure

```
web/
├── index.html          # Homepage
├── features.html       # Features page (categorized by Editor, Terminal, Git, etc.)
├── docs.html           # Documentation (single page with sidebar navigation)
├── download.html       # Download page (links to GitHub releases)
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   └── main.js         # JavaScript functionality
├── images/             # Images and screenshots
├── assets/             # Other assets (fonts, icons, etc.)
└── docs/               # Legacy docs folder (can be removed)
```

## 🚀 Getting Started

### Local Development

1. **Clone the repository:**
   ```bash
   cd Aura-Text/web
   ```

2. **Open in browser:**
   - Simply open `index.html` in your browser
   - Or use a local server for better experience:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Node.js (if you have live-server)
   npx live-server
   ```

3. **Visit:** `http://localhost:8000`

### Adding Screenshots

Place screenshots in the `images/` folder:
- `screenshot1.png` - Main editor view
- `screenshot2.png` - Dark theme
- `screenshot3.png` - Git integration
- `logo.png` - Aura Text logo
- `favicon.ico` - Site favicon

## 📝 Pages

### Homepage (`index.html`)
- Hero section with CTA
- Feature highlights (6 key features)
- Screenshot gallery
- Download section
- Stats display

### Features (`features.html`)
- **Comprehensive feature list organized by category:**
  - 📝 Editor (13 features)
  - 🔍 Code Quality (5 features)
  - 🌳 Git Integration (6 features)
  - 💻 Terminal & Console (5 features)
  - 📁 Project Management (5 features)
  - 🎨 Customization & Theming (7 features)
  - ⚡ Productivity Tools (10 features)
  - 🔌 Plugin System (6 features)
  - ⚡ Performance (5 features)
- Each feature has clear title and description

### Documentation (`docs.html`)
- Single-page documentation with sidebar navigation
- Installation guide
- Quick start tutorial
- User guide (editor basics, file management, shortcuts)
- Feature guides (Git, Terminal, Linting, Plugins)
- Advanced topics (plugin development, theme creation)
- Troubleshooting & FAQ

### Download (`download.html`)
- Single download button linking to GitHub releases
- Platform information cards (Windows, Linux, macOS)
- Quick installation guide (3 steps)
- Simplified and clean design

## 🎨 Customization

### Colors

Edit CSS variables in `css/style.css`:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --accent-color: #ec4899;
    /* ... more colors */
}
```

### Content

All content is in plain HTML files - edit directly to update text, links, and structure.

## 🔧 TODO

- [x] Create download.html page
- [x] Reorganize features into clear categories
- [x] Simplify download page to single GitHub link
- [x] Move documentation to single-page structure
- [ ] Add actual screenshots
- [ ] Add logo and favicon
- [ ] Set up deployment (GitHub Pages, Netlify, or Vercel)
- [ ] Add search functionality to docs
- [ ] Create blog section (optional)
- [ ] Add language switcher for translations
- [ ] Implement dark/light theme toggle (optional)
- [ ] Add analytics

## 🌐 Deployment

### GitHub Pages

1. Push the `web` folder to your repository
2. Go to Settings → Pages
3. Set source to `main` branch, `/web` folder
4. Your site will be available at `https://rohankishore.github.io/Aura-Text/`

### Netlify

1. Create `netlify.toml` in web folder:
   ```toml
   [build]
     publish = "."
   ```
2. Connect your GitHub repo to Netlify
3. Deploy!

### Custom Domain

Update links in HTML files to use your custom domain.

## 📄 License

Same as Aura Text - MIT License

## 🤝 Contributing

Contributions to the website are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- GitHub Issues: [Report a bug](https://github.com/rohankishore/Aura-Text/issues)
- Discussions: [Ask questions](https://github.com/rohankishore/Aura-Text/discussions)
