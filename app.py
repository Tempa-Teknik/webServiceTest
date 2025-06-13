from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pytz
import uuid
import json

app = Flask(__name__)
messages = []
custom_response_members = ""  # /get-members cevabı
custom_response_users = ""    # /get-users cevabı

@app.before_request
def log_request_info():
    print("\n--- Yeni İstek ---")
    print("URL:", request.url)
    print("Method:", request.method)
    print("Headers:")
    for k, v in request.headers.items():
        print(f"  {k}: {v}")
    print("Body (raw data):")
    try:
        print(request.get_data().decode('utf-8'))
    except Exception as e:
        print("[Body okunamadı]", e)
    print("--- İstek Sonu ---\n")
    
@app.route('/')
def index():
    return render_template(
        'index.html',
        messages=messages,
        custom_response=custom_response_members,
        custom_response_users=custom_response_users
    )

@app.route('//api/indicatorapi/milk-delivery/<string:user_id>', methods=['POST'])
def milk_delivery_double_slash(user_id):
    return milk_delivery(user_id)

@app.route('/api/indicatorapi/milk-delivery/<string:user_id>', methods=['POST'])
def milk_delivery(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Geçerli JSON gönderiniz'}), 400

    message = {
        'user_id': user_id,
        'data': data
    }
    messages.append(message)

    index_number = data.get("indexNumber", "UNKNOWN")
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
        response_data = json.loads(custom_response_members)
        return jsonify(response_data), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Geçerli bir JSON değil"}), 400

@app.route('/api/indicatorapi/get-users/<string:mac_id>', methods=['GET'])
def get_users(mac_id):
    global custom_response_users
    try:
        if not custom_response_users.strip():
            return jsonify({"error": "Henüz bir yanıt girilmedi"}), 400
        response_data = json.loads(custom_response_users)
        return jsonify(response_data), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Geçerli bir JSON değil"}), 400

@app.route('/set_get_response', methods=['POST'])
def set_get_response():
    global custom_response_members, custom_response_users
    if 'get_response' in request.form:
        custom_response_members = request.form.get('get_response', '')
    if 'get_users_response' in request.form:
        custom_response_users = request.form.get('get_users_response', '')
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