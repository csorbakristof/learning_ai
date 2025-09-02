---
layout: default
title: "Development Workflow & Testing"
---

# Development Workflow & Testing

This guide explains how to set up, develop, and test the GitHub Pages site locally, as well as how to add new projects.

## Local Development Setup

### Prerequisites

Before you begin, ensure you have:

- **Git**: For version control
- **Ruby**: Version 2.7 or higher
- **Bundler**: Ruby dependency manager
- **Windows Subsystem for Linux (WSL)** or **Git Bash** (recommended for Windows users)

### Installation Steps

#### 1. Install Ruby and Jekyll

**On Windows:**
```powershell
# Option 1: Using Chocolatey
choco install ruby

# Option 2: Download from https://rubyinstaller.org/
# Choose Ruby+Devkit version
```

**On macOS:**
```bash
# Using Homebrew
brew install ruby
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev

# Add Ruby gems to PATH
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### 2. Install Jekyll and Bundler

```bash
gem install jekyll bundler
```

#### 3. Clone and Setup Repository

```bash
# Clone your repository
git clone https://github.com/csorbakristof/learning_ai.git
cd learning_ai

# Navigate to docs directory
cd docs

# Install dependencies
bundle install
```

### Running the Site Locally

#### Start Development Server

```bash
# In the docs/ directory
bundle exec jekyll serve

# Or with live reload
bundle exec jekyll serve --livereload
```

The site will be available at `http://localhost:4000/learning_ai/`

#### Common Jekyll Commands

```bash
# Build the site (generates _site/ directory)
bundle exec jekyll build

# Serve with drafts
bundle exec jekyll serve --drafts

# Serve with future posts
bundle exec jekyll serve --future

# Clean generated files
bundle exec jekyll clean
```

### Development Workflow

#### Making Changes

1. **Start the development server**: `bundle exec jekyll serve --livereload`
2. **Edit files**: Changes to markdown files are reflected immediately
3. **Test locally**: Preview changes at `http://localhost:4000/learning_ai/`
4. **Commit changes**: Use Git to track and commit your modifications

#### File Structure

```
docs/
├── _config.yml           # Jekyll configuration
├── _data/                # Data files (YAML)
│   ├── projects.yml      # Project information
│   └── team.yml          # Team member information
├── _layouts/             # Page templates
│   ├── default.html      # Main layout
│   └── project.html      # Project page layout
├── _templates/           # Templates for new content
├── assets/               # Static assets
│   └── images/           # Images and thumbnails
├── projects/             # Project pages
├── index.md              # Homepage
└── *.md                  # Other pages
```

## Adding New Projects

### Step-by-Step Process

#### 1. Prepare Project Information

Gather the following information:
- Project title and description
- Current status (In Development, Active, Completed, Archived)
- Repository directory name
- Key features and technical details
- Getting started instructions
- User guide information

#### 2. Create Project Thumbnail

Create a **300x200 pixel** thumbnail image:
- Use a screenshot, icon, or representative image
- Save as PNG or JPG format
- Keep file size under 100KB
- Place in `docs/assets/images/`
- Use descriptive filename (e.g., `my-project-thumb.png`)

#### 3. Update Projects Data

Edit `docs/_data/projects.yml`:

```yaml
- title: "Your Project Name"
  slug: "your-project-slug"  # Used in URL, lowercase with hyphens
  description: "Brief description of your project"
  thumbnail: "your-project-thumb.png"  # Filename in assets/images/
  status: "In Development"  # Status options listed above
  project_dir: "YourProjectDirectory"  # Actual directory name in repository
```

#### 4. Create Project Page

1. **Copy the template**:
   ```bash
   cp docs/_templates/project-template.md docs/projects/your-project-slug.md
   ```

2. **Edit the frontmatter** (between `---` lines):
   ```yaml
   ---
   layout: project
   title: "Your Project Name"
   project_dir: "YourProjectDirectory"
   status: "In Development"
   release_url: ""  # Add if you have releases
   getting_started: |
     1. Your setup instructions
     2. Installation steps
     3. Basic usage
   user_guide: |
     Brief guide on how to use the project
   ---
   ```

3. **Write the content**: Fill in the Overview, Features, Technical Details, etc.

#### 5. Test Locally

```bash
cd docs
bundle exec jekyll serve --livereload
```

Visit `http://localhost:4000/learning_ai/` to verify:
- Project appears on homepage
- Project page loads correctly
- Links work properly
- Images display correctly

#### 6. Deploy

```bash
git add .
git commit -m "Add [Project Name] to website"
git push origin main
```

GitHub Pages will automatically build and deploy your changes.

## Troubleshooting

### Common Issues

#### Bundle Install Fails
```bash
# Update bundler
gem update bundler

# Clear cache and retry
bundle clean --force
bundle install
```

#### Jekyll Serve Fails
```bash
# Check Ruby version
ruby --version  # Should be 2.7+

# Reinstall Jekyll
gem uninstall jekyll
gem install jekyll
```

#### Images Not Loading
- Check file paths in `_data/projects.yml`
- Ensure images are in `docs/assets/images/`
- Verify image filenames match exactly (case-sensitive)

#### Layout Issues
- Check YAML frontmatter syntax
- Ensure proper indentation in data files
- Validate YAML using online tools if needed

### Performance Tips

#### Faster Build Times
```bash
# Exclude unnecessary files
# Add to _config.yml exclude list

# Use incremental builds
bundle exec jekyll serve --incremental
```

#### Optimizing Images
- Keep thumbnails under 100KB
- Use appropriate compression
- Consider WebP format for better compression (with fallbacks)

## Advanced Customization

### Modifying Layouts

Edit files in `_layouts/` to customize:
- Page structure
- Navigation menus
- Styling and appearance

### Adding Custom Styles

Add CSS to `assets/css/style.scss`:
```scss
---
---

@import "{{ site.theme }}";

// Your custom styles here
.project-item {
  // Custom styling
}
```

### Custom Collections

To add new content types, modify `_config.yml`:
```yaml
collections:
  tutorials:
    output: true
    permalink: /tutorials/:name/
```

## Deployment & Hosting

### GitHub Pages Automatic Deployment

1. **Enable GitHub Pages** in repository settings
2. **Set source** to "Deploy from a branch"
3. **Select branch**: `main` or `master`
4. **Set folder**: `/docs`

### Manual Deployment

```bash
# Build site locally
bundle exec jekyll build

# Deploy _site/ contents to hosting provider
```

## Maintenance

### Regular Updates

```bash
# Update dependencies
bundle update

# Check for security vulnerabilities
bundle audit

# Update Jekyll and plugins
gem update jekyll
```

### Monitoring

- **GitHub Actions**: Set up automated testing
- **Link checking**: Regularly verify external links
- **Performance**: Monitor site speed and optimization

---

*This workflow documentation should be updated as processes evolve and new best practices are discovered.*
