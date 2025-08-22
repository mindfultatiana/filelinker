# FileLinker
local file transfer server that allows you to download folders as zip files.

<img width="1178" height="353" alt="Screenshot 2025-08-22 021817" src="https://github.com/user-attachments/assets/2dfcfb85-646b-4b3a-9760-1ffa9d537a2b" />

## Instructions
1. Create a folder that is called FileLinker (or whatever you want your file path folder name to be)
2. Load folders or files you want downloadable in the folder
3. Update the script with the appropriate path
```
def main():
    FOLDER_PATH = r"C:\Users\username\Downloads\FileLinker"
    PORT = 8000
```
4. In the command line run the script
```
/Users/username/Downloads python.exe filelinker.py
```
5. Follow the instructions in the command line and go to the Device URL and/or network address listed.
```
🚀 SERVER STARTED!
📱 Device URL: http://{local_ip}:{PORT}
💻 Local URL: http://127.0.0.1:{PORT}
Press Ctrl+C to stop
```
6. Follow instructions to end the server session.

<img width="745" height="116" alt="Screenshot 2025-08-22 021908" src="https://github.com/user-attachments/assets/9b8c3a72-fc32-4742-a17c-848d4ba74cfb" />

### Optional
You can change the port if desired.

### Example of Files
<img width="1181" height="725" alt="Screenshot 2025-08-22 021834" src="https://github.com/user-attachments/assets/c6fdfb60-a88b-468f-85c4-c627653fc761" />


