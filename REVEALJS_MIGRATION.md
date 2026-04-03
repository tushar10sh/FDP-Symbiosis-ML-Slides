# Reveal.js Migration Knowledge Document

## 1. Understanding the Current Slide Architecture
The existing slides are built using a "fixed-canvas" approach:
- **Dimensions:** Every slide is designed for exactly **1280x720 pixels**.
- **Positioning:** Elements use `position: absolute` with pixel-based `left`, `top`, `width`, and `height`.
- **Containers:** Content is wrapped in a `.slide-container` div which is then displayed via an `<iframe>`.
- **Scaling Issue:** Because the dimensions are fixed in pixels, the slides do not naturally scale to fill larger 4K monitors or smaller laptop screens without manual browser zooming or complex CSS hacks.

## 2. Why Reveal.js?
Reveal.js is an industry-standard HTML presentation framework that solves the scaling problem perfectly:
- **Automatic Scaling:** It uses CSS `transform: scale()` to fit the 1280x720 canvas into any viewport while maintaining aspect ratio and internal coordinate systems.
- **Responsive Layouts:** While it supports fixed dimensions, it also allows for more fluid layouts if needed.
- **Rich Ecosystem:** Built-in support for MathJax, fragments (animations), speaker notes, and PDF export.
- **Vertical Slides:** Allows grouping related content (like "Section 1") into vertical stacks, keeping the main horizontal flow clean.

## 3. Conversion Strategy

### A. Global Configuration
The Reveal.js initialization will be configured to match your design intent:
```javascript
Reveal.initialize({
    width: 1280,
    height: 720,
    margin: 0.04,
    minScale: 0.2,
    maxScale: 2.0,
    plugins: [ RevealMath.MathJax3 ] // Essential for your ML formulas
});
```

### B. Mapping Content
- **Horizontal Slides:** Each `slides/slide*.html` file becomes a top-level `<section>`.
- **Vertical Slides:** Content in `slides/section-1/` will be nested inside a parent `<section>` to allow vertical navigation. This keeps the sub-section contained within the main presentation flow.
- **Styles:** Common styles (fonts, colors, `.slide-container` logic) will be moved to a global `<style>` block in the main Reveal.js file.
- **Scripts:** Individual slide scripts (for Chart.js) will be embedded near their respective sections.

### C. Dependency Management
Instead of every slide loading its own copies of Chart.js and MathJax, they will be loaded **once** in the main Reveal.js index file. This improves performance and prevents initialization conflicts.

### D. Special Elements
- **Links:** Internal links to `section-1/index.html` will be replaced with internal Reveal.js navigation (e.g., jumping to the next slide).
- **Charts:** Canvas IDs will be checked for collisions and handled during the conversion process.

## 4. Automation
Since there are 30+ slides, a manual conversion is error-prone. A Python-based conversion script (`convert_to_reveal.py`) will be used to:
1. Parse each slide file.
2. Extract the inner HTML of `.slide-container`.
3. Collect and deduplicate CSS/Scripts.
4. Generate a single, portable `presentation.html`.
