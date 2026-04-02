import os
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# CONFIGURATION
SLIDES_DIR = 'slides'

@app.route('/')
def index():
    slides = sorted([f for f in os.listdir(SLIDES_DIR) if f.startswith('slide') and f.endswith('.html')])
    
    if not slides:
        return "<h1>No slides found!</h1><p>Check your 'slides' folder.</p>"

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTML Slide Viewer</title>
        <style>
            body, html { 
                margin: 0; padding: 0; height: 100%; width: 100%;
                overflow: hidden; background: #000; 
            }

            #viewer { 
                width: 100vw; height: 100vh; border: none; display: block;
            }

            /* Overlay Controls */
            .controls-wrapper {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 9999; /* Ensure it is on top of everything */
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                gap: 10px;
                opacity: 0.1; 
                transition: opacity 0.3s ease;
                pointer-events: none; /* Allow clicking through the wrapper... */
            }

            .controls-wrapper:hover {
                opacity: 1;
            }

            .btn-group {
                display: flex;
                gap: 5px;
                pointer-events: auto; /* ...but make buttons clickable */
            }

            button { 
                padding: 12px 24px; 
                cursor: pointer; 
                border-radius: 8px; 
                border: 1px solid rgba(255,255,255,0.3); 
                background: rgba(30, 30, 30, 0.9); 
                color: white; 
                font-weight: bold;
                backdrop-filter: blur(10px);
            }

            button:hover { background: #444; }

            .counter { 
                color: #fff; 
                font-size: 12px; 
                background: rgba(0,0,0,0.6);
                padding: 5px 12px;
                border-radius: 20px;
                font-family: monospace;
                pointer-events: auto;
            }
        </style>
    </head>
    <body>

        <iframe id="viewer" src=""></iframe>

        <div class="controls-wrapper">
            <div class="counter" id="counter">01 / 00</div>
            <div class="btn-group">
                <button onclick="prevSlide()">PREV</button>
                <button onclick="nextSlide()">NEXT</button>
            </div>
        </div>

        <script>
            const slides = {{ slides | tojson }};
            let currentIndex = 0;
            const viewer = document.getElementById('viewer');
            const counter = document.getElementById('counter');

            function updateSlide() {
                viewer.src = `/slides/${slides[currentIndex]}`;
                const current = (currentIndex + 1).toString().padStart(2, '0');
                const total = slides.length.toString().padStart(2, '0');
                counter.innerText = `${current} / ${total}`;
                window.location.hash = currentIndex + 1;
            }

            function nextSlide() {
                if (currentIndex < slides.length - 1) {
                    currentIndex++;
                    updateSlide();
                }
            }

            function prevSlide() {
                if (currentIndex > 0) {
                    currentIndex--;
                    updateSlide();
                }
            }

            // Keyboard Logic Function
            const handleKeydown = (e) => {
                if (e.key === "ArrowRight" || e.key === " ") nextSlide();
                if (e.key === "ArrowLeft") prevSlide();
            };

            // Listen on the main window
            document.addEventListener('keydown', handleKeydown);

            // MAGIC FIX: Listen on the iframe content once it loads
            viewer.onload = function() {
                try {
                    viewer.contentWindow.document.removeEventListener('keydown', handleKeydown);
                    viewer.contentWindow.document.addEventListener('keydown', handleKeydown);
                } catch (e) {
                    console.log("Cross-origin restriction prevented iframe listener, but since we are on same server, this shouldn't happen.");
                }
            };

            // Init
            const hash = parseInt(window.location.hash.substring(1));
            if (hash && hash <= slides.length) currentIndex = hash - 1;
            updateSlide();
        </script>
    </body>
    </html>
    ''', slides=slides)

@app.route('/slides/<path:filename>')
def serve_slide(filename):
    return send_from_directory(SLIDES_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)