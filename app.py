from flask import Flask, request, jsonify, render_template, redirect
from datetime import datetime
import pytz
import uuid

app = Flask(__name__)
messages = []
get_members_response = "{}"  # Başlangıç değeri

@app.route('/')
def index():
    return render_template('index.html', messages=messages, get_members_response=get_members_response)

@app.route('/Api/indicatorapi/milk-delivery/<string:user_id>', methods=['POST'])
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
    try:
        return app.response_class(response=get_members_response, status=200, mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_get_members_response', methods=['POST'])
def save_get_members_response():
    global get_members_response
    get_members_response = request.form.get("get_members_response", "{}")
    return redirect("/")

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    messages.clear()
    return '', 204

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
