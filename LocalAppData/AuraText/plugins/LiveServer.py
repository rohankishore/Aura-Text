import os
import sys
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from PyQt6.QtCore import QFileSystemWatcher, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QPushButton, QMessageBox

from auratext import Plugin
from auratext.Core.window import Window


class LiveReloadHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler that injects live reload script into HTML files"""
    
    reload_script = """
    <script>
    (function() {
        let lastCheck = Date.now();
        setInterval(async () => {
            try {
                const response = await fetch('/__livereload__?t=' + lastCheck);
                const data = await response.text();
                if (data === 'reload') {
                    location.reload();
                }
                lastCheck = Date.now();
            } catch(e) {}
        }, 500);
    })();
    </script>
    """
    
    should_reload = False
    
    def do_GET(self):
        # Special endpoint for live reload polling
        if self.path.startswith('/__livereload__'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            if LiveReloadHandler.should_reload:
                self.wfile.write(b'reload')
                LiveReloadHandler.should_reload = False
            else:
                self.wfile.write(b'ok')
            return
        
        # Serve files normally
        super().do_GET()
    
    def end_headers(self):
        # Inject reload script into HTML files
        if hasattr(self, 'path') and self.path.endswith(('.html', '.htm')):
            content_type = self.headers.get('Content-Type', '')
            if 'text/html' in content_type or not content_type:
                # Will inject script after body is sent
                self._inject_script = True
        super().end_headers()
    
    def do_GET(self):
        if self.path.startswith('/__livereload__'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            if LiveReloadHandler.should_reload:
                self.wfile.write(b'reload')
                LiveReloadHandler.should_reload = False
            else:
                self.wfile.write(b'ok')
            return
        
        # For HTML files, inject the reload script
        if self.path.endswith(('.html', '.htm')) or self.path == '/':
            try:
                # Determine the file path
                path = self.translate_path(self.path)
                
                # If it's a directory, look for index.html
                if os.path.isdir(path):
                    for index in ('index.html', 'index.htm'):
                        index_path = os.path.join(path, index)
                        if os.path.exists(index_path):
                            path = index_path
                            break
                
                if os.path.isfile(path) and path.endswith(('.html', '.htm')):
                    with open(path, 'rb') as f:
                        content = f.read().decode('utf-8', errors='ignore')
                    
                    # Inject script before </body> or at end
                    if '</body>' in content:
                        content = content.replace('</body>', self.reload_script + '</body>')
                    else:
                        content += self.reload_script
                    
                    content_bytes = content.encode('utf-8')
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(content_bytes)))
                    self.send_header('Cache-Control', 'no-cache')
                    self.end_headers()
                    self.wfile.write(content_bytes)
                    return
            except Exception:
                pass
        
        # For non-HTML files or errors, use default handler
        super().do_GET()
    
    def log_message(self, format, *args):
        # Suppress console logging
        pass


class LiveServer(Plugin):
    def __init__(self, window: Window) -> None:
        super().__init__(window)
        
        self.window = window
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.port = 5500
        self.watcher = None
        
        # Create "Go Live" button in status bar
        self.live_button = QPushButton("🔴 Go Live")
        self.live_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #858585;
                padding: 2px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
        """)
        self.live_button.clicked.connect(self.toggle_server)
        self.live_button.setCursor(self.window.cursor())
        
        # Add button to status bar
        if hasattr(self.window, 'statusBar'):
            self.window.statusBar.addPermanentWidget(self.live_button)
    
    def toggle_server(self):
        if self.is_running:
            self.stop_server()
        else:
            self.start_server()
    
    def start_server(self):
        # Get current file's directory
        current_file = self.window.tab_file_paths.get(self.window.tab_widget.currentIndex())
        
        if not current_file:
            QMessageBox.warning(
                self.window,
                "No File Open",
                "Please open or save a file first to start the live server."
            )
            return
        
        # Set server directory to file's parent folder
        self.server_dir = str(Path(current_file).parent)
        
        def run_server():
            os.chdir(self.server_dir)
            self.server = HTTPServer(('localhost', self.port), LiveReloadHandler)
            self.server.serve_forever()
        
        try:
            # Start server in background thread
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
            # Setup file watcher
            self.setup_file_watcher()
            
            # Update UI
            self.is_running = True
            self.live_button.setText(f"🟢 Port: {self.port}")
            self.live_button.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    color: #4EC9B0;
                    padding: 2px 8px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(78, 201, 176, 0.2);
                    border-radius: 3px;
                }
            """)
            
            # Open browser
            url = f"http://localhost:{self.port}"
            if current_file.endswith(('.html', '.htm')):
                filename = os.path.basename(current_file)
                url = f"http://localhost:{self.port}/{filename}"
            
            webbrowser.open(url)
            
        except Exception as e:
            QMessageBox.critical(
                self.window,
                "Server Error",
                f"Failed to start server: {str(e)}"
            )
    
    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server = None
        
        if self.watcher:
            self.watcher.deleteLater()
            self.watcher = None
        
        self.is_running = False
        self.live_button.setText("🔴 Go Live")
        self.live_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #858585;
                padding: 2px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
        """)
    
    def setup_file_watcher(self):
        """Watch for file changes in the server directory"""
        self.watcher = QFileSystemWatcher()
        
        # Watch all HTML, CSS, JS files in directory
        for ext in ['*.html', '*.htm', '*.css', '*.js']:
            for file_path in Path(self.server_dir).rglob(ext):
                self.watcher.addPath(str(file_path))
        
        # Also watch the directory itself for new files
        self.watcher.addPath(self.server_dir)
        
        # Connect file change signal
        self.watcher.fileChanged.connect(self.on_file_changed)
        
        # Also trigger reload when saving in the editor
        if hasattr(self.window, 'current_editor'):
            # Use a timer to debounce rapid changes
            self.reload_timer = QTimer()
            self.reload_timer.setSingleShot(True)
            self.reload_timer.timeout.connect(self.trigger_reload)
    
    def on_file_changed(self, path):
        """Called when a watched file changes"""
        if self.is_running:
            # Debounce: wait 200ms before reloading
            if hasattr(self, 'reload_timer'):
                self.reload_timer.start(200)
            else:
                self.trigger_reload()
    
    def trigger_reload(self):
        """Signal browsers to reload"""
        LiveReloadHandler.should_reload = True
    
    def __del__(self):
        """Cleanup when plugin is destroyed"""
        if self.is_running:
            self.stop_server()
