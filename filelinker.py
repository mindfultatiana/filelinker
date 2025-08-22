#!/usr/bin/env python3
"""
Simple File Server - Basic Working Version
"""

import os
import socket
import urllib.parse
import mimetypes
import zipfile
import tempfile
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler


class FileHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Check for ZIP download request
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if "zip" in query_params:
            self.handle_zip_download(parsed_path.path)
            return

        # Check if this is a file request
        path = self.translate_path(self.path)
        if os.path.isfile(path):
            self._is_file_download = True
        else:
            self._is_file_download = False
        super().do_GET()

    def handle_zip_download(self, url_path):
        """Create and send ZIP file of folder"""
        # Remove query parameters and get clean path
        clean_path = url_path.split("?")[0]
        local_path = self.translate_path(clean_path)

        if not os.path.isdir(local_path):
            self.send_error(404, "Folder not found")
            return

        try:
            # Create temporary ZIP file
            temp_dir = tempfile.mkdtemp()
            folder_name = os.path.basename(local_path) or "folder"
            zip_path = os.path.join(temp_dir, f"{folder_name}.zip")

            # Create ZIP
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(local_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, local_path)
                        zipf.write(file_path, arcname)

            # Send ZIP file
            with open(zip_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header(
                "Content-Disposition", f'attachment; filename="{folder_name}.zip"'
            )
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

            # Cleanup
            shutil.rmtree(temp_dir)

        except Exception as e:
            self.send_error(500, f"Error creating ZIP: {str(e)}")

    def list_directory(self, path):
        """Custom directory listing with ZIP download links"""
        try:
            file_list = os.listdir(path)
            file_list.sort()
        except OSError:
            self.send_error(404, "Directory not found")
            return None

        # Get current directory name for title
        dir_name = os.path.basename(path) or "FileLinker"

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Files - {dir_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .header {{ background: #4CAF50; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .file-item {{ display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }}
        .file-item:hover {{ background: #f9f9f9; }}
        .file-name {{ flex-grow: 1; }}
        .download-btn {{ background: #2196F3; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; margin-left: 10px; font-size: 0.9em; }}
        .download-btn:hover {{ background: #1976D2; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 {dir_name}</h1>
        </div>
"""

        for name in file_list:
            full_path = os.path.join(path, name)
            encoded_name = urllib.parse.quote(name)

            if os.path.isdir(full_path):
                # Folder: show browse link + ZIP download
                html += f"""
                <div class="file-item">
                    <div class="file-name">📁 <a href="{encoded_name}/">{name}/</a></div>
                    <a href="{encoded_name}/?zip=1" class="download-btn">Download ZIP</a>
                </div>"""
            else:
                # File: show download link
                html += f"""
                <div class="file-item">
                    <div class="file-name">📄 {name}</div>
                    <a href="{encoded_name}" class="download-btn">Download</a>
                </div>"""

        html += """
    </div>
</body>
</html>"""

        # Return as BytesIO object
        encoded = html.encode("utf-8")
        from io import BytesIO

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return BytesIO(encoded)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def main():
    FOLDER_PATH = r"C:\Users\username\Downloads\FileLinker"
    PORT = 8000

    print(f"Starting server...")
    print(f"Target folder: {FOLDER_PATH}")

    # Create folder if it doesn't exist
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH, exist_ok=True)
        print("Created folder")

        # Create test file
        with open(os.path.join(FOLDER_PATH, "test.txt"), "w") as f:
            f.write("Hello from FileLinker!")

    # Change to the target directory
    original_dir = os.getcwd()
    os.chdir(FOLDER_PATH)
    print(f"Changed to: {os.getcwd()}")

    # List what's in the folder
    files = os.listdir(".")
    print(f"Files in folder: {files}")

    try:
        server = HTTPServer(("", PORT), FileHandler)
        local_ip = get_local_ip()

        print(f"\n🚀 SERVER STARTED!")
        print(f"📱 Tablet URL: http://{local_ip}:{PORT}")
        print(f"💻 Local URL: http://127.0.0.1:{PORT}")
        print("Press Ctrl+C to stop\n")

        server.serve_forever()

    except KeyboardInterrupt:
        print("\n\n✅ Server stopped successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        os.chdir(original_dir)
        print("Cleaned up. Server is fully stopped.")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
