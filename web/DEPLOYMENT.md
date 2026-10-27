# Deployment Guide

This guide covers different ways to deploy the Aura Text website.

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All images are added and optimized
- [ ] All links are working and point to correct URLs
- [ ] Content is proofread and accurate
- [ ] Website tested on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsiveness checked
- [ ] No console errors
- [ ] Analytics/tracking added (if desired)
- [ ] Custom domain configured (if applicable)

## 🚀 Deployment Options

### 1. GitHub Pages (Recommended - Free)

**Setup:**

1. **Create gh-pages branch:**
   ```bash
   git checkout -b gh-pages
   ```

2. **Move web files to root** (GitHub Pages serves from root):
   ```bash
   # Option A: Serve from /web folder (preferred)
   # Keep files in web/ and configure in repo settings
   
   # Option B: Move to root
   cp -r web/* .
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

4. **Configure in GitHub:**
   - Go to repository Settings → Pages
   - Source: `gh-pages` branch
   - Folder: `/root` or `/web` (depending on structure)
   - Save

5. **Access your site:**
   - URL: `https://rohankishore.github.io/Aura-Text/`
   - Or `https://yourusername.github.io/Aura-Text/`

**Custom Domain:**

1. Add `CNAME` file in web directory:
   ```
   auratext.example.com
   ```

2. Configure DNS:
   - Add A records pointing to GitHub IPs:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - Or add CNAME record pointing to `username.github.io`

3. Enable HTTPS in repository settings

---

### 2. Netlify (Free)

**Manual Deploy:**

1. Go to [netlify.com](https://netlify.com)
2. Sign up/login
3. Drag and drop the `web` folder
4. Done! Your site is live

**Continuous Deployment:**

1. **Create `netlify.toml` in web folder:**
   ```toml
   [build]
     publish = "."
     
   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

2. **Connect to GitHub:**
   - New site from Git
   - Authorize Netlify
   - Select Aura-Text repository
   - Base directory: `web`
   - Build command: (leave empty)
   - Publish directory: `.` or `web`

3. **Deploy:**
   - Every push to main triggers deploy
   - Get free `*.netlify.app` subdomain
   - Add custom domain in settings

**Custom Domain on Netlify:**
- Go to Domain Settings
- Add custom domain
- Follow DNS configuration steps
- SSL is automatic and free

---

### 3. Vercel (Free)

**Setup:**

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   cd web
   vercel
   ```

**Or use Web Interface:**

1. Go to [vercel.com](https://vercel.com)
2. Import Git repository
3. Configure:
   - Root directory: `web`
   - No build command needed
4. Deploy!

**Custom Domain:**
- Add in project settings
- Configure DNS
- SSL automatic

---

### 4. Cloudflare Pages (Free)

1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Connect to GitHub
3. Select repository
4. Configure:
   - Build command: (none)
   - Build output directory: `web`
5. Deploy

---

### 5. Self-Hosted (VPS/Dedicated Server)

**Using Nginx:**

1. **Install Nginx:**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Copy files:**
   ```bash
   sudo cp -r web/* /var/www/html/
   ```

3. **Configure Nginx:**
   ```nginx
   server {
       listen 80;
       server_name auratext.example.com;
       root /var/www/html;
       index index.html;
       
       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

4. **Enable HTTPS with Let's Encrypt:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d auratext.example.com
   ```

**Using Apache:**

1. **Install Apache:**
   ```bash
   sudo apt install apache2
   ```

2. **Copy files:**
   ```bash
   sudo cp -r web/* /var/www/html/
   ```

3. **Configure virtual host:**
   ```apache
   <VirtualHost *:80>
       ServerName auratext.example.com
       DocumentRoot /var/www/html
       
       <Directory /var/www/html>
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>
   </VirtualHost>
   ```

---

## 🔧 Post-Deployment

### Analytics

**Google Analytics:**

Add before `</head>` in all HTML files:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

**Alternatives:**
- Plausible Analytics (privacy-focused)
- Fathom Analytics
- Simple Analytics

### Performance Optimization

1. **Enable compression:**
   - Gzip/Brotli (most hosts enable by default)

2. **Add caching headers:**
   ```nginx
   location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

3. **Use CDN:**
   - Cloudflare (free tier)
   - jsDelivr for assets

4. **Optimize images:**
   - Use WebP format
   - Lazy loading
   - Responsive images

### SEO

**Add to each page `<head>`:**

```html
<!-- SEO Meta Tags -->
<meta name="description" content="Page-specific description">
<meta name="keywords" content="IDE, Python, Code Editor, Aura Text">
<meta name="author" content="Rohan Kishore">

<!-- Open Graph -->
<meta property="og:title" content="Aura Text - Python IDE">
<meta property="og:description" content="A powerful IDE made with Python">
<meta property="og:image" content="https://yoursite.com/images/og-image.png">
<meta property="og:url" content="https://yoursite.com/">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Aura Text - Python IDE">
<meta name="twitter:description" content="A powerful IDE made with Python">
<meta name="twitter:image" content="https://yoursite.com/images/twitter-card.png">
```

**Create `sitemap.xml`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yoursite.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://yoursite.com/features.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- Add all pages -->
</urlset>
```

**Create `robots.txt`:**

```
User-agent: *
Allow: /
Sitemap: https://yoursite.com/sitemap.xml
```

### Monitoring

Set up uptime monitoring:
- UptimeRobot (free)
- Pingdom
- StatusCake

---

## 🔄 Updating the Site

### GitHub Pages
```bash
# Make changes
git add .
git commit -m "Update: description"
git push origin gh-pages
```

### Netlify/Vercel/Cloudflare
```bash
# Just push to main branch
git add .
git commit -m "Update: description"
git push origin main
# Automatic deployment!
```

### Self-Hosted
```bash
# Pull changes on server
ssh user@yourserver
cd /var/www/html
git pull origin main
```

---

## 🆘 Troubleshooting

**Site not updating:**
- Clear browser cache (Ctrl+Shift+R)
- Check deployment logs
- Wait a few minutes (CDN propagation)

**404 errors:**
- Check file paths are correct
- Ensure file names match (case-sensitive on Linux)
- Verify base directory configuration

**Images not loading:**
- Check image paths
- Ensure images are committed to repo
- Verify file permissions (self-hosted)

**Custom domain not working:**
- DNS propagation can take 24-48 hours
- Verify DNS records are correct
- Check SSL certificate status

---

## 📚 Resources

- [GitHub Pages Documentation](https://docs.github.com/pages)
- [Netlify Documentation](https://docs.netlify.com/)
- [Vercel Documentation](https://vercel.com/docs)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)

---

**Need help?** Open an issue on GitHub!
