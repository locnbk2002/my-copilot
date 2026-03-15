---
name: frontend-design
description: "Create polished frontend interfaces from designs/screenshots/videos. Use for web components, replicating UI designs, quick prototypes, immersive interfaces, avoiding AI slop."
argument-hint: "[screenshot|video|from-scratch|3d|quick]"
license: MIT
---

Create distinctive, production-grade frontend interfaces. Implement real working code with exceptional aesthetic attention.

## Workflow Selection

Choose workflow based on input type:

| Input                            | Workflow                  |
| -------------------------------- | ------------------------- |
| Screenshot                       | Replicate exactly         |
| Video                            | Replicate with animations |
| Screenshot/Video (describe only) | Document for devs         |
| 3D/WebGL request                 | Three.js immersive        |
| Quick task                       | Rapid implementation      |
| Complex/award-quality            | Full immersive            |
| From scratch                     | Design Thinking below     |

**All workflows**: Activate `ui-ux-pro-max` skill FIRST for design intelligence.

## Screenshot/Video Replication (Quick Reference)

1. **Analyze** input — extract colors, fonts, spacing, effects (use image/video analysis if multimodal available)
2. **Plan** with ui-ux-designer — create phased implementation
3. **Implement** — match source precisely
4. **Verify** — compare to original
5. **Document** — update `./docs/design-guidelines.md` if approved

## Design Thinking (From Scratch)

Before coding, commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme — brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Execute with precision. Bold maximalism and refined minimalism both work — intentionality is key.

## Aesthetics Guidelines

- **Typography**: Avoid Arial/Inter; use distinctive, characterful fonts. Pair display + body fonts.
- **Color**: Commit to cohesive palette. CSS variables. Dominant colors with sharp accents.
- **Motion**: CSS-first, anime.js for complex animations. Orchestrated page loads > scattered micro-interactions.
- **Spatial**: Unexpected layouts. Asymmetry. Overlap. Negative space OR controlled density.
- **Backgrounds**: Atmosphere over solid colors. Gradients, noise, patterns, shadows, grain.
- **Assets**: Generate or source high-quality visual assets; analyze and verify quality before use.

## Asset & Analysis Tasks

| Task               | Approach                                          |
| ------------------ | ------------------------------------------------- |
| Generate assets    | Use multimodal image generation if available      |
| Analyze quality    | Visually inspect and compare to reference         |
| Extract guidelines | Read design tokens from screenshots               |
| Optimization       | Compress, convert to WebP, lazy load              |
| Animations         | CSS transitions first, anime.js for orchestration |

## Anti-Patterns (AI Slop)

NEVER use:

- Overused fonts: Inter, Roboto, Arial, Space Grotesk
- Cliched colors: purple gradients on white
- Predictable layouts, cookie-cutter patterns

DO:

- Vary themes (light/dark), fonts, aesthetics per project
- Match complexity to vision (maximalist = elaborate; minimalist = precise)
- Make unexpected, context-specific choices

Remember: Commit fully to distinctive visions. Extraordinary creative work is possible and expected.
