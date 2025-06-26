from flask import Flask, request, Response, render_template
from datetime import datetime
import pytz
import uuid
import json

app = Flask(__name__)
messages = []
custom_response_members = ""  # /get-members cevabı (string olarak)
custom_response_users = ""    # /get-users cevabı (string olarak)

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
        data = request.get_json(force=True)
    except Exception:
        return Response(
            json.dumps({'status': 'error', 'message': 'Geçerli JSON gönderiniz'}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

    if not data:
        return Response(
            json.dumps({'status': 'error', 'message': 'Geçerli JSON gönderiniz'}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

    messages.append({
        'user_id': user_id,
        'data': data
    })

    index_number = data.get("indexNumber", "UNKNOWN")
    generated_id = str(uuid.uuid4())

    response_data = {
        "Status": True,
        "Data": {
            "Id": generated_id,
            "IndexNumber": index_number
        },
        "Message": "10000",
        "MessageCode": "Başarılı",
        "CurrentDateTime": datetime.now(pytz.timezone("Europe/Istanbul")).isoformat()
    }

    return Response(
        json.dumps(response_data, separators=(",", ":"), ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/indicatorapi/get-members/<string:mac_id>', methods=['GET'])
def get_members(mac_id):
    global custom_response_members
    try:
        if not custom_response_members.strip():
            return Response(
                json.dumps({"error": "Henüz bir yanıt girilmedi"}, separators=(",", ":"), ensure_ascii=False),
                status=400,
                mimetype='application/json'
            )
        return Response(
            custom_response_members,
            status=200,
            mimetype='application/json'
        )
    except json.JSONDecodeError:
        return Response(
            json.dumps({"error": "Geçerli bir JSON değil"}, separators=(",", ":"), ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

@app.route('/api/indicatorapi/get-users/<string:mac_id>', methods=['GET'])
def get_users(mac_id):
    global custom_response_users
    try:
        if not custom_response_users.strip():
            return Response(
                json.dumps({"error": "Henüz bir yanıt girilmedi"}, separators=(",", ":"), ensure_ascii=False),
                status=400,
                mimetype='application/json'
            )
        return Response(
            custom_response_users,
            status=200,
            mimetype='application/json'
        )
    except json.JSONDecodeError:
        return Response(
            json.dumps({"error": "Geçerli bir JSON değil"}, separators=(",", ":"), ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

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
    return Response(
        json.dumps({'messages': messages}, separators=(",", ":"), ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
