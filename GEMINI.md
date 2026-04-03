# GEMINI.md - FDP-Symbiosis-ML-Slides

## Project Overview
This project is a web-based presentation platform for a **Faculty Development Programme (FDP) on Machine Learning at Symbiosis**. It provides a collection of interactive, high-fidelity HTML slides covering various ML topics, including foundations, metrics, and deep learning.

### Main Technologies
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript (Vanilla).
- **Backend (Development/Serving):** Python with **Flask**.
- **External Libraries:** FontAwesome (icons), Google Fonts (Inter, Roboto Mono).

---

## Directory Structure
- `slides/`: Contains the primary HTML slide files (e.g., `slide001.html`, `slide002.html`).
- `slides/section-1/`: A sub-directory containing a specific section of the presentation with its own static viewer.
- `app.py`: A Flask application that dynamically discovers slides and provides a viewer interface with navigation controls.
- `index.html`: A static viewer page that manually lists slides, suitable for hosting on static site providers like GitHub Pages.

---

## Building and Running

### Running the Dynamic Viewer (Flask)
The Flask app automatically detects all `slide*.html` files in the `slides/` directory.

1. **Install Dependencies:**
   ```bash
   pip install flask
   ```
2. **Start the Server:**
   ```bash
   python app.py
   ```
3. **Access the Slides:**
   Open `http://localhost:5000` in your browser.

### Using the Static Viewer
For environments without Python/Flask:
1. Open `index.html` directly in any modern web browser.
2. Note: The static viewer requires manual updates to the `slides` array in the `<script>` tag when new slides are added.

---

## Development Conventions

### Slide Creation
- **File Naming:** New slides should be placed in the `slides/` directory and follow the naming convention `slideXXX.html` (e.g., `slide015.html`).
- **Layout:** Slides use a fixed aspect ratio container (`.slide-container`) with absolute positioning for elements to ensure consistent rendering across different screens.
- **Styling:** Inline styles are frequently used within slide files for specific element positioning, while global styles are defined in the `<head>`.

### Navigation
- The viewer (both in `app.py` and `index.html`) supports:
  - **On-screen buttons:** PREV / NEXT.
  - **Keyboard:** `ArrowRight` or `Space` for next slide, `ArrowLeft` for previous slide.
  - **URL Hashes:** You can jump to a specific slide using the hash (e.g., `index.html#5`).

### Static Viewer Updates
When adding or removing slides, ensure the `const slides` array in `index.html` (and `slides/section-1/index.html` if applicable) is updated to reflect the changes, as it does not auto-discover files like the Flask app.
