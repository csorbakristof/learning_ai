# Overview

This project is a GitHub Pages website which is used to publish the results in this repository. Our goal is to experiment with generative AI technologies in many areas of the everyday life of an IT engineer: administrative task automation, workflow automation, scripting, learning, vibe coding, software development of larget scales with heavy involvement of generative AI etc.

The github pages webpage should have
- A nice landing page with short introduction and an overview list of our projects (each of them with a title, thumbnail image and a few lines of description)
- Some general subpages containing
    - Members of the team
    - General onboarding guidelines for those who want to join
    - Summary of current and past events
    - List of related publications and how to cite us.
    - Impressum
- An individual page group for every single project (subdirectory inside the repository). Usually, a project has a single page, but more complex ones may have multiple ones.
- Once a project is ready for publishing, it should be easy for AI tools to generate the corresponding page for it. The repository should have a template for the project webpage which always contains the followings:
    - Overview of the project and link to its root directory on github.com
    - How to download (link to the last release if available on github.com) and getting started
    - Short user guide on how to use it. (More detailed descriptions will be available inside the projects source code which will we available on github.com as the project is open source.)

# Answers on questions from the AI

## Structure & Navigation Questions

### Repository structure

Question: Should the GitHub Pages site be set up in the root of your repository, or do you want it in a separate docs/ folder or a separate gh-pages branch?

Answer: I want to have a separate docs/ folder, but no separate gh-pages branch.

### Project discovery

Question: Since you want individual pages for each project (subdirectory), should I create an automated way to discover projects, or do you prefer a manual configuration file listing the projects to include?

Answer: I want to do that manually.

### Navigation structure

Question: For the project pages, would you prefer:
Flat navigation (all project pages at the same level)
Categorized navigation (grouping projects by type/topic)
Both overview and detail pages for complex projects

Answer: I want a flat navigation.

## Design & Layout Questions:
### Homepage layout

Question: For the project overview on the landing page, would you prefer:
A grid layout with thumbnail cards
A list view with thumbnails on the side
An accordion-style expandable list

Answer: A list view with thumbnails.

### Project thumbnails

Question: Should I create placeholder thumbnail images for now?
Do you have a preferred image format/size for thumbnails?
Should thumbnails be auto-generated from project content or manually specified?

Answer: create a placeholder, I will create the thumbnails manually. Suggest a format/size, I do not have preferences for that.

### Team members page

Question: What information should be displayed for each team member? (Name, role, bio, photo, contact info, etc.)

Answer: name, role, photo

## Technical Setup Questions:
### Content management

Question: Would you like me to set up:
A Jekyll-based site with markdown files
Simple HTML pages
A hybrid approach with templates and data files

Answer: I want a Jekyll-based site.

### Project page generation

Question: For the AI-assisted project page creation, should I create:
A standardized markdown template
A script/workflow for generating pages
Documentation on the expected format

Answer: yes, please create a template and a workflow description. The workflow description should also contain testing the site by locally running Jekyll (and installing it if needed).
