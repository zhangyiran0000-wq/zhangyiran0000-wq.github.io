---
title: "Sitemap"
permalink: /sitemap/
layout: single
author_profile: false
---

## Main pages

<ul>
{% for item in site.data.navigation.main %}
  <li><a href="{{ item.url | relative_url }}">{{ item.title }}</a></li>
{% endfor %}
</ul>
