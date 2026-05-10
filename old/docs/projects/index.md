---
layout: default
title: "Projects Overview"
---

# Projects Overview

Explore our collection of generative AI experiments and tools for IT engineering tasks.

{% assign projects = site.data.projects %}
<div class="projects-list">
  {% for project in projects %}
  <div class="project-item">
    <div class="project-thumbnail">
      <img src="{{ site.baseurl }}/assets/images/{{ project.thumbnail | default: 'placeholder-300x200.png' }}" 
           alt="{{ project.title }}" width="300" height="200">
    </div>
    <div class="project-content">
      <h3><a href="{{ site.baseurl }}/projects/{{ project.slug }}/">{{ project.title }}</a></h3>
      <p>{{ project.description }}</p>
      <p><small><strong>Status:</strong> {{ project.status | default: "In Development" }}</small></p>
      <p><small><strong>Repository:</strong> <a href="{{ site.github.repository_url }}/tree/master/{{ project.project_dir }}">{{ project.project_dir }}</a></small></p>
    </div>
  </div>
  {% endfor %}
</div>

## Project Categories

Our projects span several key areas of AI-assisted development:

### Administrative Automation
Tools that streamline routine administrative tasks using AI assistance.

### Document Processing
Solutions for extracting, processing, and transforming various document formats.

### Educational Technology
AI-enhanced tools for learning, assessment, and educational content management.

### Development Assistance
Utilities and frameworks that incorporate AI to improve software development workflows.

### Data Analysis & Visualization
Tools for processing, analyzing, and visualizing data with AI assistance.

## Contributing to Projects

Each project welcomes contributions! Here's how you can get involved:

1. **Explore the Code**: Visit the project's repository directory
2. **Read the Documentation**: Each project has its own README and documentation
3. **Try the Tools**: Follow the getting started instructions
4. **Report Issues**: Found a bug or have a suggestion? Create an issue
5. **Submit Improvements**: Fork, modify, and submit pull requests

## Adding New Projects

Interested in starting a new AI experiment? Follow these steps:

1. **Create Project Directory**: Set up your project in the repository
2. **Add Project Documentation**: Include README and usage instructions
3. **Update Project Data**: Add your project to `_data/projects.yml`
4. **Create Project Page**: Use our project template (see workflow documentation)
5. **Add Thumbnail**: Create a 300x200 pixel thumbnail image

For detailed instructions, see our [workflow documentation]({{ site.baseurl }}/workflow/).
