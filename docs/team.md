---
layout: default
title: "Our Team"
---

# Our Team

Meet the people behind the Learning AI experiments.

{% assign team_members = site.data.team %}
{% if team_members %}
<div class="team-grid">
  {% for member in team_members %}
  <div class="team-member">
    <div class="member-photo">
      <img src="{{ site.baseurl }}/assets/images/{{ member.photo | default: 'placeholder-person.png' }}" 
           alt="{{ member.name }}" width="150" height="150">
    </div>
    <h3>{{ member.name }}</h3>
    <p class="member-role">{{ member.role }}</p>
  </div>
  {% endfor %}
</div>
{% else %}
<div class="team-grid">
  <div class="team-member">
    <div class="member-photo">
      <img src="{{ site.baseurl }}/assets/images/placeholder-person.png" 
           alt="Team Member" width="150" height="150">
    </div>
    <h3>Your Name Here</h3>
    <p class="member-role">Role/Position</p>
  </div>
</div>

<p><em>Update the team data file at <code>_data/team.yml</code> to add team members.</em></p>
{% endif %}
