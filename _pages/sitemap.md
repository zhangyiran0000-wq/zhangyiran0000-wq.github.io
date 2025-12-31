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

## Other pages (optional)

<ul>
{% assign nav_urls = site.data.navigation.main | map: "url" %}
{% for p in site.pages %}
  {% if p.title and p.permalink %}
    {% unless p.sitemap == false or p.published == false %}
      {% unless nav_urls contains p.permalink %}
        <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
      {% endunless %}
    {% endunless %}
  {% endif %}
{% endfor %}
</ul>
