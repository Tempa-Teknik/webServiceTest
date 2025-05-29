from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pytz
import uuid  # UUID üretmek için

app = Flask(__name__)
messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

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

    # Gelen JSON’dan IndexNumber'ı al, yoksa UNKNOWN yap
    index_number = data.get("indexNumber", "UNKNOWN")
    
    # UUID oluştur
    generated_id = str(uuid.uuid4())

    # Cevap JSON'u
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

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    messages.clear()
    return '', 204

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
