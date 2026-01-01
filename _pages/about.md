---
permalink: /
title: "About"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I’m a Ph.D. researcher at Nanyang Technological University working on **trustworthy AI for robotic and autonomous systems**. I care about making learning-based systems **reliable in the real world**: exposing failure modes, detecting them at runtime, and designing policies that handle uncertainty safely.
- robust perception & decision-making
- uncertainty estimation and monitoring
- safety evaluation, testing, and simulation
- ML systems that must work under real-world constraints

_I am actively seeking AI or robotics roles, with a focus on autonomous systems and trustworthy AI. I am open to both industry and research opportunities—please feel free to contact me if my experience is a good fit._

## Research focus
My work sits at the intersection of:

- **Adversarial / stress testing**: generate rare, hard cases to reveal weaknesses
- **Online monitoring**: detect distribution shift, uncertainty, and anomalies at runtime
- **Decision-making under uncertainty**: safer planning/control when information is imperfect

## Design philosophy: failure-aware AI
I treat “trustworthy” as a lifecycle:
**find failures → measure them → reduce them → monitor them in deployment**.
This mindset applies to many robotics settings (mobile robots, manipulation, drones, and other safety-critical autonomy), not just one domain.

## Experience (engineering mindset)
Before my Ph.D., I worked as a software engineer at ZTE, developing **high-frequency algorithms (up to 240kHz)** for 5G systems. That experience pushed me toward building systems that are **deployable, efficient, and testable**—not just good in a paper.

## An Approach to Trustworthy AI
My research is centered on **adversarial design**. Trustworthy AI is not achieved by average-case performance, but by continuously exposing and managing failure modes. Illustrated here using autonomous driving as a safety-critical testbed, but applicable to broader AI and robotic systems.
<p align="center"> <img src="/images/Philo.jpg"
     alt="Adversarial design philosophy illustration"
     width="600" /> </p>
     
-**Adversary** actively generates rare, risky, and adversarial scenarios to expose system weaknesses, using passive and active testing as well as objective and subjective evaluations. 

-**Adaptor** continuously improves perception, decision-making, and control to mitigate the failures revealed by adversarial exposure. 

-**Collaborator (Human-in-the-loop)** provides human assistance when uncertainty, ambiguity, or risk exceeds the autonomous system’s capability.
