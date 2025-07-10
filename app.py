from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json

app = Flask(__name__)

# folder to store the data (erd files)
SAVE_FOLDER = "erd-jsons-files"
os.makedirs(SAVE_FOLDER, exist_ok=True)



#home page, see list of erd
@app.route('/')
def index():
    erd_files = []
    for filename in os.listdir(SAVE_FOLDER):
        if filename.endswith('.json'):
            file_path = os.path.join(SAVE_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                erd_files.append({
                    "name": data.get("name", "???"),
                    "file": filename.replace(".json", ""),
                })
    return render_template('index.html', erds=erd_files)



@app.route('/create-erd', methods=['POST'])
def create_erd():
    erd_name = request.form.get('name')
    tables = []

    if not erd_name:
        return "Invalid ERD", 400

    safe_name = erd_name.replace(" ", "_").lower()
    #TODO:: to add datetime befroe the safefile name
    file_path = os.path.join(SAVE_FOLDER, f"{safe_name}.json")

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({'name': erd_name, 'tables': tables}, f,indent=2)

    return redirect(url_for('read_erd', erd_name=safe_name))



@app.route('/read/<erd_name>')
def read_erd(erd_name):
    return render_template('show_erd.html')



if __name__ == '__main__':
    app.run(debug=True)