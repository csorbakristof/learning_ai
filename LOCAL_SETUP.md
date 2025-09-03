# Local Development Quick Start

## Prerequisites

Before running the local site, you need to install Ruby:

1. **Download Ruby+Devkit** from: https://rubyinstaller.org/
2. **Choose version 3.0 or higher** with Devkit
3. **Run the installer** and follow the setup wizard
4. **Install MSYS2** when prompted (recommended)

## Running the Site

### Option 1: Batch File (Recommended)
Double-click `setup_local_site.bat` - this will:
- Check if Ruby and Bundler are installed
- Install Jekyll dependencies
- Start the development server

### Option 2: PowerShell Script
Right-click `setup_local_site.ps1` and select "Run with PowerShell"

### Option 3: Manual Commands
Open PowerShell/Command Prompt and run:
```bash
cd docs
bundle install
bundle exec jekyll serve --livereload
```

## After Setup

Once the server is running:
- Open your browser to: **http://localhost:4000/learning_ai/**
- The site will automatically reload when you make changes
- Press **Ctrl+C** in the terminal to stop the server

## Quick Restart

After the initial setup, you can use `run_local_site.bat` for faster startup.

## Troubleshooting

### Ruby Not Found
- Make sure Ruby is installed from rubyinstaller.org
- Restart your command prompt/PowerShell after installation
- Check that Ruby is in your PATH: `ruby --version`

### Bundle Install Fails
- Update bundler: `gem update bundler`
- Clear cache: `bundle clean --force`
- Retry: `bundle install`

### Port Already in Use
- Use a different port: `bundle exec jekyll serve --port=4001`
- Or kill the existing process and try again

### Jekyll Command Not Found
- Install Jekyll: `gem install jekyll bundler`
- Make sure gems are in your PATH

## Development Tips

- **Live Reload**: Changes to markdown files appear immediately
- **CSS Changes**: Refresh the browser after CSS modifications
- **Config Changes**: Restart the server after modifying `_config.yml`
- **New Files**: Restart server when adding new pages or layouts

## File Structure

```
docs/
├── _config.yml          # Jekyll configuration
├── _data/               # Data files (projects, team)
├── _layouts/            # Page templates
├── assets/css/          # Stylesheets
├── projects/            # Project pages
└── *.md                 # Site pages
```

## Making Changes

1. **Edit content** in markdown files
2. **Add projects** by updating `_data/projects.yml`
3. **Customize styling** in `assets/css/style.scss`
4. **Test locally** before committing
5. **Push to GitHub** for automatic deployment
