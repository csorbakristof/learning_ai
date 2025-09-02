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

<style>
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2em;
  margin: 2em 0;
}

.team-member {
  text-align: center;
  padding: 1em;
  border: 1px solid #eee;
  border-radius: 8px;
}

.member-photo img {
  border-radius: 50%;
  border: 3px solid #ddd;
}

.team-member h3 {
  margin: 1em 0 0.5em 0;
}

.member-role {
  color: #666;
  font-style: italic;
  margin: 0;
}
</style>
