# Images Directory

This folder contains images and assets for the Aura Text website.

## Required Images

### Logo and Branding
- `logo.png` - Aura Text logo (32x32px or larger, transparent background)
- `favicon.ico` - Website favicon (16x16, 32x32, 48x48)

### Screenshots
Place screenshots of Aura Text in action:

- `screenshot1.png` - Main editor view showing code
  - Recommended size: 1920x1080
  - Show syntax highlighting and UI

- `screenshot2.png` - Dark theme showcase
  - Recommended size: 1920x1080
  - Highlight customization features

- `screenshot3.png` - Git integration features
  - Recommended size: 1920x1080
  - Show commit dialog, graph, or rebase UI

### Additional Images (Optional)
- `hero-bg.png` - Background image for hero section
- `feature-*.png` - Individual feature screenshots
- `demo.gif` - Animated demo of features

## Image Guidelines

### Format
- Use PNG for screenshots and graphics
- Use SVG for icons when possible
- Use WebP for better compression (with PNG fallback)
- Use ICO for favicons

### Optimization
- Compress images before uploading
- Recommended tools:
  - TinyPNG (https://tinypng.com/)
  - Squoosh (https://squoosh.app/)
  - ImageOptim (macOS)

### Size Guidelines
- Screenshots: Max 2MB each
- Logo: Less than 100KB
- Favicon: Less than 50KB

## How to Add Images

1. Save your images in this directory
2. Use relative paths in HTML:
   ```html
   <img src="images/logo.png" alt="Aura Text Logo">
   ```

3. For optimized loading, consider using `<picture>` element:
   ```html
   <picture>
     <source srcset="images/screenshot.webp" type="image/webp">
     <img src="images/screenshot.png" alt="Description">
   </picture>
   ```

## Current Status

⚠️ **This directory is currently empty**

Please add the required images listed above to complete the website.
