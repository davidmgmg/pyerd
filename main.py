import threading
import webview
from app import app

def run_flask():
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    window = webview.create_window("ERD App", "http://127.0.0.1:5000")
    webview.start()  