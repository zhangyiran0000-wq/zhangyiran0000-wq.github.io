---
title: "Project Demos"
permalink: /projects/
layout: single
author_profile: false
---

## Adversarial Design Framework (PhD Research)

<p align="center">
  <img src="/images/Framework.jpg"
       alt="Adversarial design framework illustration"
       width="500" />
</p>

**Overview.**  
Rather than optimizing average-case performance, it emphasizes **adversarial stress testing**, **system adaptation**, and **human collaboration** to improve reliability under real-world uncertainty.

Although illustrated here using **autonomous driving as a representative safety-critical domain**, the framework is intended to be **general** and has informed my work in human–machine interaction and embodied robotic systems.
 


## Demo 1 — Natural Scene Generation (2022)

<div style="display: flex; gap: 24px; align-items: center; flex-wrap: wrap;">

  <!-- Video (LEFT) -->
  <div style="flex: 1; min-width: 260px; text-align: center;">
    <iframe
      width="100%"
      height="315"
      src="https://www.youtube.com/embed/5tDlAgcQ_GA/edit"
      title="Adversarial scene generation demo"
      frameborder="0"
      allowfullscreen>
    </iframe>
  </div>

  <!-- Description (RIGHT) -->
  <div style="flex: 1; min-width: 260px;" class="desc">

  **Problem.**  
  Autonomous driving systems often perform well on average but fail under rare or adversarial conditions.

  **Approach.**  
  I developed an adversarial scene generation algorithm that actively constructs challenging traffic scenarios, coupled with a human-style *Turing test* to assess whether failures are realistic and meaningful.

  **Framework connection.**  
  This demo illustrates the **Adversary** component of the framework by systematically exposing failure modes that are unlikely to appear in standard datasets.

  </div>

</div>
