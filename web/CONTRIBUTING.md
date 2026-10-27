# Contributing to Aura Text Website

Thank you for your interest in contributing to the Aura Text website! This guide will help you get started.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
- [Style Guide](#style-guide)
- [Submitting Changes](#submitting-changes)

## 🚀 Getting Started

### Prerequisites

- A text editor (VS Code, Sublime Text, etc.)
- Basic knowledge of HTML, CSS, and JavaScript
- A web browser for testing
- (Optional) A local web server

### Setup

1. Fork the Aura Text repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Aura-Text.git
   cd Aura-Text/web
   ```

3. Open `index.html` in your browser, or run a local server:
   ```bash
   # Python
   python -m http.server 8000
   
   # Node.js
   npx live-server
   ```

## 📁 Project Structure

```
web/
├── index.html          # Homepage
├── features.html       # Features showcase
├── download.html       # Download page
├── docs/
│   └── index.html      # Documentation
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   └── main.js         # JavaScript functionality
├── images/             # Images and screenshots
└── assets/             # Other assets
```

## 🤝 How to Contribute

### Content Updates

**Updating Text Content:**
1. Find the relevant HTML file
2. Edit the text directly in the HTML
3. Test your changes locally
4. Submit a pull request

**Adding New Pages:**
1. Create a new `.html` file
2. Copy the structure from existing pages
3. Update navigation links in all pages
4. Add appropriate CSS if needed
5. Test thoroughly

### Design Improvements

**CSS Changes:**
- All styles are in `css/style.css`
- Use CSS variables for colors (defined in `:root`)
- Follow the existing naming conventions
- Test responsive design (mobile, tablet, desktop)

**Adding Features:**
- JavaScript goes in `js/main.js`
- Keep it vanilla JS (no frameworks)
- Comment your code clearly
- Ensure it works across browsers

### Screenshots and Images

1. Add images to `images/` folder
2. Optimize before committing (use TinyPNG or similar)
3. Use descriptive names (e.g., `feature-git-integration.png`)
4. Update `images/README.md` if needed

## 🎨 Style Guide

### HTML

```html
<!-- Use semantic HTML -->
<section class="features">
  <div class="container">
    <h2 class="section-title">Features</h2>
    <!-- content -->
  </div>
</section>

<!-- Proper indentation (2 spaces) -->
<div class="card">
  <h3>Title</h3>
  <p>Description</p>
</div>
```

### CSS

```css
/* Follow BEM-like naming */
.feature-card { }
.feature-card__title { }
.feature-card--highlighted { }

/* Use CSS variables */
color: var(--primary-color);
background: var(--bg-dark);

/* Group related properties */
.element {
    /* Positioning */
    position: relative;
    
    /* Display & Box Model */
    display: flex;
    padding: 1rem;
    
    /* Visual */
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    
    /* Typography */
    font-size: 1rem;
    color: var(--text-primary);
    
    /* Other */
    transition: all 0.3s ease;
}
```

### JavaScript

```javascript
// Use clear function names
function updateActiveSidebarLink() {
  // Implementation
}

// Comment complex logic
// This calculates the scroll position and updates active links
const sections = document.querySelectorAll('.doc-section');

// Use modern ES6+ syntax
const elements = document.querySelectorAll('.feature');
elements.forEach(el => {
  // Do something
});
```

### Accessibility

- Always include `alt` text for images
- Use semantic HTML elements
- Ensure sufficient color contrast
- Make interactive elements keyboard accessible
- Test with screen readers when possible

```html
<!-- Good -->
<button aria-label="Close menu" onclick="closeMenu()">×</button>
<img src="logo.png" alt="Aura Text Logo">

<!-- Bad -->
<div onclick="closeMenu()">×</div>
<img src="logo.png">
```

## 📝 Submitting Changes

### Before Submitting

- [ ] Test all changes locally
- [ ] Check responsive design (mobile, tablet, desktop)
- [ ] Verify all links work
- [ ] Ensure no console errors
- [ ] Validate HTML (https://validator.w3.org/)
- [ ] Check browser compatibility
- [ ] Optimize any new images

### Pull Request Process

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```
   
   Use conventional commits:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for content changes
   - `Style:` for CSS/design changes
   - `Docs:` for documentation

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request:**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Describe your changes clearly

### PR Description Template

```markdown
## Description
Brief description of your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Content update
- [ ] Design improvement
- [ ] Documentation

## Screenshots (if applicable)
Add screenshots showing your changes

## Checklist
- [ ] Tested locally
- [ ] Responsive design checked
- [ ] All links work
- [ ] No console errors
- [ ] Images optimized
```

## 🐛 Reporting Issues

Found a bug or have a suggestion? Please:

1. Check if it's already reported
2. Create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Screenshots if relevant
   - Browser/OS information

## 💡 Suggestions

Have ideas for the website? We'd love to hear them!

- Create an issue with the `enhancement` label
- Describe the feature/improvement
- Explain why it would be valuable
- Include mockups if you have them

## 📞 Questions?

- Open an issue with the `question` label
- Join discussions on GitHub
- Check existing documentation

## ⭐ Recognition

All contributors will be recognized in the project. Significant contributions may be highlighted on the website!

---

Thank you for helping make the Aura Text website better! 🎉
