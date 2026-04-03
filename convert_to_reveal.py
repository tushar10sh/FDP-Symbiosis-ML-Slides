import os
import re

def extract_slide_data(file_path):
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract styles
    styles = re.findall(r'<style>(.*?)</style>', content, re.DOTALL)
    cleaned_styles = []
    for s in styles:
        # Remove body and html selectors as they interfere with Reveal.js
        s = re.sub(r'body\s*\{[^}]*\}', '', s, flags=re.IGNORECASE | re.DOTALL)
        s = re.sub(r'html\s*\{[^}]*\}', '', s, flags=re.IGNORECASE | re.DOTALL)
        cleaned_styles.append(s.strip())
    
    # Extract slide container content
    # Note: Using a more robust regex to find the slide-container div
    container_match = re.search(r'<div class="slide-container">(.*?)</div>\s*(?=<script|</body>|$)', content, re.DOTALL)
    if container_match:
        body = container_match.group(1)
    else:
        # Fallback to body content if container not found
        body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
        body = body_match.group(1) if body_match else ""
    
    # Extract scripts (excluding those that load libraries like Chart.js or MathJax)
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    # Clean scripts: remove potential library loads if they were inside script tags (unlikely given grep)
    
    return {
        'body': body,
        'scripts': scripts,
        'styles': cleaned_styles
    }

def main():
    slides_dir = 'slides'
    section1_dir = os.path.join(slides_dir, 'section-1')
    
    # Define the main sequence from index.html
    main_slides = [
        "slide001.html", "slide002.html", "slide003.html", "slide003-SECTION01.html", 
        "slide004.html", "slide005.html", "slide006.html", "slide007.html", "slide008.html",
        "slide009.html", "slide010.html", "slide011.html", "slide012.html",
        "slide013.html", "slide014.html"
    ]
    
    # Define section 1 slides
    section1_slides = sorted([f for f in os.listdir(section1_dir) if f.startswith('slide') and f.endswith('.html')])
    
    all_styles = set()
    output_html = []
    
    for slide_name in main_slides:
        path = os.path.join(slides_dir, slide_name)
        data = extract_slide_data(path)
        if not data:
            continue
            
        all_styles.update(data['styles'])
        
        # If it's the section trigger slide, we'll nest section 1 as vertical slides
        if slide_name == "slide003-SECTION01.html":
            output_html.append('<!-- Section 1 Start -->')
            output_html.append('<section>')
            
            # The trigger slide itself
            output_html.append('  <section>')
            output_html.append(data['body'])
            for s in data['scripts']:
                output_html.append(f'    <script>{s}</script>')
            output_html.append('  </section>')
            
            # The sub-slides
            for sub_slide in section1_slides:
                sub_path = os.path.join(section1_dir, sub_slide)
                sub_data = extract_slide_data(sub_path)
                if sub_data:
                    all_styles.update(sub_data['styles'])
                    output_html.append('  <section>')
                    output_html.append(sub_data['body'])
                    for s in sub_data['scripts']:
                        output_html.append(f'    <script>{s}</script>')
                    output_html.append('  </section>')
            
            output_html.append('</section>')
            output_html.append('<!-- Section 1 End -->')
        else:
            output_html.append('<section>')
            output_html.append(data['body'])
            for s in data['scripts']:
                output_html.append(f'    <script>{s}</script>')
            output_html.append('</section>')

    # Prepare final HTML
    template = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>ML Presentation - Reveal.js</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js/dist/theme/white.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --r-main-font: 'Inter', sans-serif;
            --r-heading-font: 'Inter', sans-serif;
        }}
        .reveal .slides section {{
            padding: 0;
            width: 1280px;
            height: 720px;
            text-align: left;
        }}
        /* Restore the slide container styling context */
        .reveal .slides section {{
            background-color: #ffffff;
            overflow: hidden;
        }}
        {" ".join(all_styles)}
        
        /* Reveal.js specific overrides to prevent conflicts */
        .reveal h1, .reveal h2, .reveal h3, .reveal h4, .reveal h5, .reveal h6 {{
            text-transform: none;
            font-family: 'Inter', sans-serif;
        }}
        .reveal p {{ margin: 0; display: block; }}
        
        /* Hide the launch button in reveal version as we navigate vertically */
        .launch-btn {{ display: none !important; }}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {"".join(output_html)}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js/plugin/math/math.js"></script>
    <script>
        Reveal.initialize({{
            width: 1280,
            height: 720,
            margin: 0,
            minScale: 0.1,
            maxScale: 2.0,
            hash: true,
            center: false,
            transition: 'slide',
            plugins: [ RevealMath.MathJax3 ]
        }});
        
        // Re-render MathJax on slide changes if needed
        Reveal.on('slidechanged', event => {{
            if (window.MathJax) {{
                MathJax.typesetPromise();
            }}
        }});
    </script>
</body>
</html>
"""
    with open('presentation.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print("Successfully generated presentation.html")

if __name__ == "__main__":
    main()
