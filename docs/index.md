---
layout: default
title: "Learning AI - Generative AI Experiments"
---

# Welcome to Learning AI

We are experimenting with generative AI technologies in many areas of everyday IT engineering tasks. Our projects cover administrative task automation, workflow automation, scripting, learning, vibe coding, and software development at larger scales with heavy involvement of generative AI.

## Our Projects

{% assign projects = site.data.projects %}
{% if projects %}
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
    </div>
  </div>
  {% endfor %}
</div>
{% else %}
<div class="projects-list">
  <div class="project-item">
    <div class="project-thumbnail">
      <img src="{{ site.baseurl }}/assets/images/placeholder-300x200.png" 
           alt="Sample Project" width="300" height="200">
    </div>
    <div class="project-content">
      <h3><a href="{{ site.baseurl }}/projects/sample-project/">Sample Project</a></h3>
      <p>This is a placeholder for your first project. Update the projects data file to add your real projects.</p>
      <p><small><strong>Status:</strong> Template</small></p>
    </div>
  </div>
</div>
{% endif %}

## Get Involved

Interested in joining our experiments with generative AI? Check out our [onboarding guide]({{ site.baseurl }}/onboarding/) to learn how you can contribute to our projects.

## Latest Updates

Stay tuned for updates on our ongoing experiments and findings. Follow our progress on [GitHub]({{ site.github.repository_url }}) and check out our [events page]({{ site.baseurl }}/events/) for upcoming activities.

<style>
.projects-list {
  margin: 2em 0;
}

.project-item {
  display: flex;
  margin-bottom: 2em;
  padding-bottom: 2em;
  border-bottom: 1px solid #eee;
  align-items: flex-start;
}

.project-thumbnail {
  flex-shrink: 0;
  margin-right: 1.5em;
}

.project-thumbnail img {
  border: 1px solid #ddd;
  border-radius: 4px;
}

.project-content {
  flex: 1;
}

.project-content h3 {
  margin-top: 0;
  margin-bottom: 0.5em;
}

.project-content h3 a {
  text-decoration: none;
  color: #333;
}

.project-content h3 a:hover {
  color: #0366d6;
}

@media (max-width: 768px) {
  .project-item {
    flex-direction: column;
  }
  
  .project-thumbnail {
    margin-right: 0;
    margin-bottom: 1em;
    align-self: center;
  }
}
</style>
