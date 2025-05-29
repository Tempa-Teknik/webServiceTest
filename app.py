from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pytz
import uuid

app = Flask(__name__)
messages = []

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html', messages=messages)

# POST endpoint: /Api/indicatorapi/milk-delivery/<user_id>
@app.route('/Api/indicatorapi/milk-delivery/<string:user_id>', methods=['POST'])
def milk_delivery(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Geçerli JSON gönderiniz'}), 400

    # Mesajı kaydet
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

# GET endpoint: /api/indicatorapi/get-members/<mac_id>
@app.route('/api/indicatorapi/get-members/<string:mac_id>')
def get_members(mac_id):
    # URL query parametreleri: $top ve $skip
    top = request.args.get('$top', default=10, type=int)
    skip = request.args.get('$skip', default=0, type=int)

    # Burada kendi mantığını ekleyebilirsin, örnek:
    # Gelen mac_id'ye göre bazı işlemler yap, mesaj al ya da döndür

    # Burada metin kutusundan döndürülecek örnek JSON sabit olarak:
    example_response = {
        "Status": True,
        "Data": {
            "Id": "abcdef12-3456-7890-abcd-ef1234567890",
            "IndexNumber": "999"
        },
        "Message": "10000",
        "MessageCode": "Başarılı",
        "CurrentDateTime": datetime.now(pytz.timezone("Europe/Istanbul")).isoformat()
    }

    return jsonify(example_response), 200

# Mesajları temizle
@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    messages.clear()
    return '', 204

# Mesajları listele
@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
