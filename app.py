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
    elements = []

    if not erd_name:
        return "Invalid ERD", 400

    safe_name = erd_name.replace(" ", "_").lower()
    #TODO:: to add datetime befroe the safefile name
    file_path = os.path.join(SAVE_FOLDER, f"{safe_name}.json")

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({'name': erd_name, 'elements': elements}, f,indent=2)

    return redirect(url_for('read_erd', erd=safe_name))



@app.route('/read/<erd>')
def read_erd(erd):
    file_path = os.path.join(SAVE_FOLDER, f"{erd}.json")
    with open(file_path, 'r', encoding="utf-8") as f:
        erd_data = json.load(f)
    return render_template('show_erd.html', erd_name=erd_data.get("name", "???") ,erd_data=json.dumps(erd_data))



@app.route('/create/text/<erd_name>', methods=['POST'])
def create_text(erd_name):
    data = request.get_json()
    file_path = os.path.join(SAVE_FOLDER, f"{erd_name}.json")

    if not os.path.exists(file_path):
        return jsonify({"error": "ERD file not found"}), 404
    
    with open(file_path, 'r', encoding='utf-8') as f:
        erd_data = json.load(f)
    
    erd_data.setdefault("elements", []).append(data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(erd_data, f, indent=2)
    
    return jsonify({"status": "success", "element": data})



# @app.route('/create/table/<erd>', methods=['POST'])
# def create_table(erd):
    






# editng the er diagrams
@app.route('/update-position/<erd>', methods=['POST'])
def update_position(erd):
    data = request.get_json()
    element_id = data.get("id")
    new_pos = data.get("position")

    file_path = os.path.join(SAVE_FOLDER, f"{erd}.json")
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    with open(file_path, 'r', encoding='utf-8') as f:
        erd_data = json.load(f)

    updated = False
    for el in erd_data.get("elements", []):
        if el["id"] == element_id:
            el["position"] = new_pos
            updated = True
            break

    if not updated:
        return jsonify({"error": "Element not found"}), 404

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(erd_data, f, indent=2)

    return jsonify({"status": "success", "updated_id": element_id})




if __name__ == '__main__':
    app.run(debug=True)




    # IMPORTANT : erd_name: the erd name and file name should be differentiated in the future