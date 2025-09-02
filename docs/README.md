# Learning AI - GitHub Pages Website

This directory contains the Jekyll-based website for the Learning AI project, hosted on GitHub Pages.

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   cd docs
   bundle install
   ```

2. **Start development server**:
   ```bash
   bundle exec jekyll serve --livereload
   ```

3. **Open in browser**: `http://localhost:4000/learning_ai/`

### Adding a New Project

1. **Update project data**: Edit `_data/projects.yml`
2. **Add thumbnail**: Place 300x200px image in `assets/images/`
3. **Create project page**: Copy `_templates/project-template.md` to `projects/`
4. **Test locally**: Verify everything works before committing

## Site Structure

- **Homepage** (`index.md`): Project overview with thumbnails
- **Projects** (`projects/`): Individual project pages
- **Team** (`team.md`): Team member profiles
- **Onboarding** (`onboarding.md`): Contributor guide
- **Events** (`events.md`): Activities and workshops
- **Publications** (`publications.md`): Research and papers
- **Contact** (`contact.md`): Contact info and legal notices

## Configuration

- **Theme**: Leap Day (GitHub Pages theme)
- **Jekyll Configuration**: `_config.yml`
- **Dependencies**: `Gemfile`
- **Data Files**: `_data/` directory
- **Templates**: `_layouts/` and `_templates/`

## Development Workflow

Detailed instructions are available in [workflow.md](workflow.md), including:
- Local Jekyll setup
- Adding projects and content
- Testing and deployment
- Troubleshooting common issues

## Customization

### Updating Site Information

Edit `_config.yml` to modify:
- Site title and description
- Repository URLs
- Navigation menu
- Build settings

### Adding Team Members

Edit `_data/team.yml`:
```yaml
- name: "Member Name"
  role: "Role/Position"
  photo: "member-photo.jpg"
```

### Modifying Navigation

Update the `navigation` section in `_config.yml`:
```yaml
navigation:
  - title: "Page Title"
    url: "/page-url/"
```

## Assets

### Images

- **Project Thumbnails**: 300x200px, saved in `assets/images/`
- **Team Photos**: 150x150px (square), saved in `assets/images/`
- **Placeholders**: Available for new projects and team members

### Styling

The site uses the Leap Day theme with custom CSS additions. Modify layouts in `_layouts/` or add custom styles to page frontmatter.

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment source is set to the `/docs` folder.

**Live Site**: https://csorbakristof.github.io/learning_ai/

## Support

For issues with the website:
1. Check the [workflow documentation](workflow.md)
2. Review Jekyll and GitHub Pages documentation
3. Create an issue in the main repository

## Contributing

See the main project's [onboarding guide](onboarding.md) for general contribution guidelines. For website-specific contributions:
- Follow the project template format
- Test changes locally before submitting
- Update documentation when adding new features
- Maintain consistency with existing design and structure

---

*For detailed development instructions, see [workflow.md](workflow.md)*
