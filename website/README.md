# Development Skills Laboratory Website

This is the documentation website for the Development Skills Laboratory: From Zero to Hero (via Epic Failures). Built with [Docusaurus](https://docusaurus.io/).

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run start
```

The site will open at `http://localhost:3000`.

## 📁 Project Structure

```
website/
├── docs/           # Course content (Markdown files)
├── src/            # Custom React components
├── static/         # Static assets (images, files)
├── docusaurus.config.js  # Main configuration
├── sidebars.js     # Sidebar navigation
└── package.json    # Dependencies and scripts
```

## 🛠️ Development

### Available Scripts

- `npm run start` - Start development server
- `npm run build` - Build for production
- `npm run serve` - Serve production build locally
- `npm run deploy` - Deploy to GitHub Pages

### Content Editing

Course content is in the `docs/` directory:

- `docs/intro.md` - Homepage content
- `docs/chapters/` - Course chapters
- `docs/debugging-journey.md` - Debugging stories
- `docs/exercises.md` - Practice exercises

### Styling

Custom CSS is in `src/css/custom.css`. The theme includes:

- Custom color scheme
- Failure/success story callouts
- Exercise boxes
- Debugging step styling

## 🚀 Deployment

### GitHub Pages

1. Update `docusaurus.config.js` with your GitHub details:
   ```js
   url: 'https://your-username.github.io',
   baseUrl: '/your-repo-name/',
   organizationName: 'your-username',
   projectName: 'your-repo-name',
   ```

2. Deploy:
   ```bash
   npm run deploy
   ```

### Other Platforms

The build output is in the `build/` directory and can be deployed to:
- Netlify
- Vercel
- AWS S3
- Any static hosting service

## 🎨 Customization

### Theme Colors

Edit `src/css/custom.css` to change colors:

```css
:root {
  --ifm-color-primary: #2e8b57;  /* Main theme color */
  --ifm-color-primary-dark: #29784c;
  /* ... */
}
```

### Navigation

Edit `sidebars.js` to modify navigation structure.

### Components

Custom React components go in `src/components/`.

## 📚 Course Philosophy

This documentation site embraces the **Failure-Driven Development** methodology:

- Real debugging stories with actual error messages
- Step-by-step problem-solving processes
- Honest accounts of development challenges
- Learning through systematic failure analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the build: `npm run build`
5. Submit a pull request

## 📖 Learn More

- [Docusaurus Documentation](https://docusaurus.io/)
- [Markdown Guide](https://www.markdownguide.org/)
- [React Documentation](https://reactjs.org/)

---

*"The expert has failed more times than the beginner has even tried. Let's fail faster so we can succeed sooner."*
