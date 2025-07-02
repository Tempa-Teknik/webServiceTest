from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pytz
import uuid
import json
import os
from collections import OrderedDict

app = Flask(__name__)
messages = []

# JSON dosyaları
MEMBERS_FILE = 'get_members.json'
USERS_FILE = 'get_users.json'

# Bellekteki veriler
custom_response_members = ''
custom_response_users = ''

# Uygulama başlarken dosyalardan yükle
if os.path.exists(MEMBERS_FILE):
    with open(MEMBERS_FILE, 'r', encoding='utf-8') as f:
        custom_response_members = f.read()

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        custom_response_users = f.read()

@app.route('/')
def index():
    return render_template(
        'index.html',
        messages=messages,
        custom_response=custom_response_members,
        custom_response_users=custom_response_users
    )

@app.route('/api/indicatorapi/milk-delivery/<string:user_id>', methods=['POST'])
def milk_delivery(user_id):
    try:
        data = request.get_data()
        print("Gelen ham veri:", data.decode('utf-8'))  # Ham veri (byte -> str)
        parsed = json.loads(data, object_pairs_hook=OrderedDict)
        print("Parse edilmiş veri:", parsed)
    except Exception:
        return jsonify({'status': 'error', 'message': 'Geçerli JSON gönderiniz'}), 400

    # Buraya ekle:
    amount_raw = parsed.get("Amount")
    weight_raw = parsed.get("Weight")

    if amount_raw is not None:
        parsed["Amount"] = "{:.3f}".format(amount_raw)
    if weight_raw is not None:
        parsed["Weight"] = "{:.3f}".format(weight_raw)

    message = {
        'user_id': user_id,
        'data': parsed
    }
    messages.append(message)

    index_number = parsed.get("indexNumber", "UNKNOWN")
    generated_id = str(uuid.uuid4())

    response = {
        "Status": True,
        "Data": {
            "Id": generated_id,
            "IndexNumber": index_number
        },
        "Message": "10000",
        "MessageCode": "Başarılı",
        "CurrentDateTime": datetime.now(pytz.timezone("Europe/Istanbul")).isoformat()
    }

    return jsonify(response), 200

@app.route('/api/indicatorapi/get-members/<string:mac_id>', methods=['GET'])
def get_members(mac_id):
    global custom_response_members
    try:
        if not custom_response_members.strip():
            return jsonify({"error": "Henüz bir yanıt girilmedi"}), 400
        return app.response_class(
            response=custom_response_members,
            status=200,
            mimetype='application/json'
        )
    except Exception:
        return jsonify({"error": "Geçerli bir JSON değil"}), 400

@app.route('/api/indicatorapi/get-users/<string:mac_id>', methods=['GET'])
def get_users(mac_id):
    global custom_response_users
    try:
        if not custom_response_users.strip():
            return jsonify({"error": "Henüz bir yanıt girilmedi"}), 400
        return app.response_class(
            response=custom_response_users,
            status=200,
            mimetype='application/json'
        )
    except Exception:
        return jsonify({"error": "Geçerli bir JSON değil"}), 400

@app.route('/set_get_response', methods=['POST'])
def set_get_response():
    global custom_response_members, custom_response_users

    if 'get_response' in request.form:
        raw_members = request.form.get('get_response', '')
        try:
            members_json = json.loads(raw_members, object_pairs_hook=OrderedDict)
            if "CurrentDateTime" in members_json:
                members_json["CurrentDateTime"] = datetime.now(pytz.timezone("Europe/Istanbul")).isoformat()
            custom_response_members = json.dumps(members_json, ensure_ascii=False, separators=(",", ":"))
        except Exception:
            custom_response_members = raw_members
        with open(MEMBERS_FILE, 'w', encoding='utf-8') as f:
            f.write(custom_response_members)

    if 'get_users_response' in request.form:
        raw_users = request.form.get('get_users_response', '')
        try:
            users_json = json.loads(raw_users, object_pairs_hook=OrderedDict)
            if "CurrentDateTime" in users_json:
                users_json["CurrentDateTime"] = datetime.now(pytz.timezone("Europe/Istanbul")).isoformat()
            custom_response_users = json.dumps(users_json, ensure_ascii=False, separators=(",", ":"))
        except Exception:
            custom_response_users = raw_users
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            f.write(custom_response_users)

    return '', 204

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    messages.clear()
    return '', 204

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
